#!/usr/bin/env python3
"""Run a small cross-language sutra embedding pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

import numpy as np
from lxml import html


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[1]
DATA_DIR = ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = ROOT / "outputs"
CACHE_DIR = OUTPUT_DIR / "embedding_cache"
MANIFEST_PATH = ROOT / "manifest.json"


def ensure_dirs() -> None:
    for path in [PROCESSED_DIR, OUTPUT_DIR, CACHE_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def load_project_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def clean_84000_text(value: str) -> str:
    value = value.replace("\u00ad", "")
    value = value.replace("\u200d", "")
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"(?<=\s)\d{1,3}(?=\s)", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def extract_84000_translation(path: Path) -> tuple[str, list[dict[str, str]]]:
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    seen: set[tuple[str, str]] = set()
    sections: list[dict[str, str]] = []
    label_pattern = re.compile(r"^(?:p\.\d+|\d+\.\d+)$")

    for section in doc.xpath('//*[@label and contains(@class,"scroll-mt-20")]'):
        label = section.get("label") or ""
        if not label_pattern.match(label):
            continue
        text = " ".join(section.xpath('.//div[contains(@class,"passage")]//p//text()'))
        text = clean_84000_text(text)
        if len(text) < 50:
            continue
        key = (label, text)
        if key in seen:
            continue
        seen.add(key)
        sections.append({"label": label, "text": text})

    if not sections:
        raise ValueError(f"No 84000 translation sections extracted from {path}")

    body = "\n\n".join(section["text"] for section in sections)
    return body, sections


def read_body(item: dict[str, Any]) -> tuple[str, list[dict[str, str]]]:
    path = PROJECT_ROOT / item["source_path"]
    if item["source_kind"] == "84000_html":
        return extract_84000_translation(path)
    body = path.read_text(encoding="utf-8").strip()
    return body, []


def build_corpus(manifest: list[dict[str, Any]]) -> dict[str, Any]:
    texts = []
    for item in manifest:
        body, sections = read_body(item)
        if not body.strip():
            raise ValueError(f"Empty body for {item['id']}")

        body_path = PROCESSED_DIR / f"{item['id']}_body.txt"
        body_path.write_text(body + "\n", encoding="utf-8")

        section_path = None
        if sections:
            section_path = PROCESSED_DIR / f"{item['id']}_sections.tsv"
            section_path.write_text(
                "label\ttext\n" + "\n".join(f"{row['label']}\t{row['text']}" for row in sections) + "\n",
                encoding="utf-8",
            )

        text_record = {
            **item,
            "body_path": str(body_path.relative_to(PROJECT_ROOT)),
            "char_count": len(body),
            "body_sha256": sha256_text(body),
        }
        if section_path:
            text_record["section_path"] = str(section_path.relative_to(PROJECT_ROOT))
            text_record["section_count"] = len(sections)
        texts.append(text_record)

    corpus = {"texts": texts}
    write_json(PROCESSED_DIR / "corpus_index.json", corpus)
    return corpus


def token_chunks(text: str, max_tokens: int, overlap: int) -> list[str]:
    import tiktoken

    if max_tokens <= overlap:
        raise ValueError("max_tokens must be larger than overlap.")
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    if not tokens:
        return []
    chunks = []
    step = max_tokens - overlap
    for start in range(0, len(tokens), step):
        chunk_tokens = tokens[start : start + max_tokens]
        if len(chunk_tokens) < max_tokens // 4 and chunks:
            break
        chunks.append(encoder.decode(chunk_tokens))
    return chunks


def cache_path(model: str, chunk: str) -> Path:
    safe_model = model.replace("/", "_")
    key = sha256_text(f"{model}\n{chunk}")
    return CACHE_DIR / f"{safe_model}_{key}.json"


def read_cache(model: str, chunk: str) -> list[float] | None:
    path = cache_path(model, chunk)
    if not path.exists():
        return None
    return load_json(path)["embedding"]


def write_cache(model: str, chunk: str, embedding: list[float]) -> None:
    write_json(
        cache_path(model, chunk),
        {
            "model": model,
            "chunk_sha256": sha256_text(chunk),
            "embedding": embedding,
        },
    )


def embed_missing(model: str, chunks: list[str]) -> tuple[list[list[float]], int]:
    from openai import OpenAI

    response = OpenAI().embeddings.create(model=model, input=chunks)
    total_tokens = getattr(getattr(response, "usage", None), "total_tokens", 0) or 0
    return [item.embedding for item in response.data], total_tokens


def average_embedding(embeddings: list[list[float]]) -> list[float]:
    return np.array(embeddings, dtype=np.float32).mean(axis=0).astype(float).tolist()


def cosine(left: list[float], right: list[float]) -> float:
    left_array = np.array(left, dtype=float)
    right_array = np.array(right, dtype=float)
    denom = np.linalg.norm(left_array) * np.linalg.norm(right_array)
    if denom == 0:
        return 0.0
    return float(np.dot(left_array, right_array) / denom)


def embed_corpus(corpus: dict[str, Any], model: str, max_tokens: int, overlap: int, no_api: bool) -> dict[str, Any]:
    chunk_records: list[dict[str, Any]] = []
    missing: list[tuple[int, str]] = []
    cache_hits = 0

    for text in corpus["texts"]:
        body = (PROJECT_ROOT / text["body_path"]).read_text(encoding="utf-8").strip()
        chunks = token_chunks(body, max_tokens=max_tokens, overlap=overlap)
        if not chunks:
            raise ValueError(f"No chunks generated for {text['id']}")
        for index, chunk in enumerate(chunks):
            embedding = read_cache(model, chunk)
            if embedding is None:
                missing.append((len(chunk_records), chunk))
            else:
                cache_hits += 1
            chunk_records.append(
                {
                    "chunk_id": f"{text['id']}::chunk_{index:04d}",
                    "text_id": text["id"],
                    "chunk_index": index,
                    "char_count": len(chunk),
                    "chunk_sha256": sha256_text(chunk),
                    "embedding": embedding,
                }
            )

    api_tokens = 0
    if missing:
        if no_api:
            raise SystemExit(f"{len(missing)} chunks are missing from cache.")
        if not os.getenv("OPENAI_API_KEY"):
            raise SystemExit("OPENAI_API_KEY is required for missing embeddings.")
        embeddings, api_tokens = embed_missing(model, [chunk for _, chunk in missing])
        for (record_index, chunk), embedding in zip(missing, embeddings):
            write_cache(model, chunk, embedding)
            chunk_records[record_index]["embedding"] = embedding

    text_records = []
    for text in corpus["texts"]:
        embeddings = [
            record["embedding"]
            for record in chunk_records
            if record["text_id"] == text["id"]
        ]
        text_records.append(
            {
                **text,
                "model": model,
                "chunk_count": len(embeddings),
                "embedding": average_embedding(embeddings),
            }
        )

    return {
        "model": model,
        "max_tokens": max_tokens,
        "overlap": overlap,
        "texts": text_records,
        "chunks": chunk_records,
        "cache_hits": cache_hits,
        "cache_misses": len(missing),
        "api_tokens": api_tokens,
    }


def summarize(embeddings: dict[str, Any]) -> dict[str, Any]:
    texts = embeddings["texts"]
    similarities = []
    nearest: dict[str, list[dict[str, Any]]] = {}
    for source in texts:
        rows = []
        for target in texts:
            if source["id"] == target["id"]:
                continue
            score = cosine(source["embedding"], target["embedding"])
            row = {
                "source_id": source["id"],
                "target_id": target["id"],
                "score": score,
                "same_work": source["work_id"] == target["work_id"],
                "same_language": source["language"] == target["language"],
            }
            similarities.append(row)
            rows.append(row)
        nearest[source["id"]] = sorted(rows, key=lambda item: item["score"], reverse=True)

    target_id = "toh106_samdhinirmocana_en"
    target_rows = nearest[target_id]
    same_work = [row for row in target_rows if row["same_work"]]
    best_same_work = same_work[0] if same_work else None
    best_rank = None
    if best_same_work:
        best_rank = target_rows.index(best_same_work) + 1

    return {
        "similarities": sorted(similarities, key=lambda item: item["score"], reverse=True),
        "nearest_texts": nearest,
        "cross_language_target": {
            "source_id": target_id,
            "best_same_work": best_same_work,
            "rank": best_rank,
            "top_neighbors": target_rows[:5],
        },
    }


def stripped_embeddings(embeddings: dict[str, Any]) -> dict[str, Any]:
    output = {key: value for key, value in embeddings.items() if key != "chunks"}
    output["texts"] = [
        {key: value for key, value in text.items() if key != "embedding"}
        for text in embeddings["texts"]
    ]
    return output


def main() -> None:
    load_project_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="text-embedding-3-large")
    parser.add_argument("--max-tokens", type=int, default=700)
    parser.add_argument("--overlap", type=int, default=100)
    parser.add_argument("--no-api", action="store_true")
    args = parser.parse_args()

    ensure_dirs()
    manifest = load_json(MANIFEST_PATH)
    corpus = build_corpus(manifest)
    embeddings = embed_corpus(corpus, args.model, args.max_tokens, args.overlap, args.no_api)
    summary = summarize(embeddings)
    result = {
        **stripped_embeddings(embeddings),
        **summary,
    }
    write_json(OUTPUT_DIR / "pilot_results.json", result)

    target = summary["cross_language_target"]
    print(f"Texts: {len(embeddings['texts'])}")
    print(f"Chunks: {len(embeddings['chunks'])}")
    print(f"Cache hits: {embeddings['cache_hits']}")
    print(f"Cache misses: {embeddings['cache_misses']}")
    print(f"API tokens: {embeddings['api_tokens']}")
    if target["best_same_work"]:
        best = target["best_same_work"]
        print(
            "Cross-language target: "
            f"{target['source_id']} -> {best['target_id']} "
            f"rank {target['rank']} score {best['score']:.4f}"
        )
    print(f"Wrote {(OUTPUT_DIR / 'pilot_results.json').relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
