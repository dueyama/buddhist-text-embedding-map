#!/usr/bin/env python3
"""Embed processed sect sutra corpus chunks with a cache."""

from __future__ import annotations

import argparse
import os
from typing import Any

import numpy as np

from common import (
    EMBEDDING_CACHE_DIR,
    OUTPUT_DIR,
    PROCESSED_DIR,
    PROJECT_ROOT,
    ensure_dirs,
    load_json,
    load_project_env,
    sha256_text,
    token_chunks,
    write_json,
)


def cache_path(model: str, chunk: str):
    key = sha256_text(f"{model}\n{chunk}")
    safe_model = model.replace("/", "_")
    return EMBEDDING_CACHE_DIR / f"{safe_model}_{key}.json"


def read_cache(model: str, chunk: str) -> list[float] | None:
    path = cache_path(model, chunk)
    if not path.exists():
        return None
    return load_json(path)["embedding"]


def write_cache(model: str, chunk: str, embedding: list[float]) -> None:
    path = cache_path(model, chunk)
    write_json(
        path,
        {
            "model": model,
            "chunk_sha256": sha256_text(chunk),
            "embedding": embedding,
        },
    )


def embed_missing(model: str, chunks: list[str]) -> tuple[list[list[float]], int]:
    from openai import OpenAI

    client = OpenAI()
    response = client.embeddings.create(model=model, input=chunks)
    embeddings = [item.embedding for item in response.data]
    total_tokens = getattr(getattr(response, "usage", None), "total_tokens", 0) or 0
    return embeddings, total_tokens


def average_embedding(embeddings: list[list[float]]) -> list[float]:
    array = np.array(embeddings, dtype=np.float32)
    return array.mean(axis=0).astype(float).tolist()


def main() -> None:
    load_project_env()

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="text-embedding-3-large")
    parser.add_argument("--max-tokens", type=int, default=700)
    parser.add_argument("--overlap", type=int, default=100)
    parser.add_argument(
        "--no-api",
        action="store_true",
        help="Only use cached embeddings; fail if anything is missing.",
    )
    args = parser.parse_args()

    ensure_dirs()
    corpus_index_path = PROCESSED_DIR / "corpus_index.json"
    if not corpus_index_path.exists():
        raise SystemExit("Run build_corpus.py before embed_texts.py.")

    corpus = load_json(corpus_index_path)
    chunk_records: list[dict[str, Any]] = []
    missing: list[tuple[int, str]] = []
    total_cache_hits = 0

    for text in corpus["texts"]:
        body = (PROJECT_ROOT / text["body_path"]).read_text(encoding="utf-8").strip()
        chunks = token_chunks(body, max_tokens=args.max_tokens, overlap=args.overlap)
        if not chunks:
            raise ValueError(f"No chunks generated for {text['id']}")
        for index, chunk in enumerate(chunks):
            embedding = read_cache(args.model, chunk)
            if embedding is None:
                missing.append((len(chunk_records), chunk))
            else:
                total_cache_hits += 1
            chunk_records.append(
                {
                    "chunk_id": f"{text['id']}::chunk_{index:04d}",
                    "text_id": text["id"],
                    "chunk_index": index,
                    "char_count": len(chunk),
                    "chunk_sha256": sha256_text(chunk),
                    "preview": chunk[:160],
                    "embedding": embedding,
                }
            )

    total_api_tokens = 0
    if missing:
        if args.no_api:
            raise SystemExit(f"{len(missing)} chunks are missing from cache.")
        if not os.getenv("OPENAI_API_KEY"):
            raise SystemExit("OPENAI_API_KEY is required for missing embeddings.")
        missing_embeddings, total_api_tokens = embed_missing(
            args.model, [chunk for _, chunk in missing]
        )
        for (record_index, chunk), embedding in zip(missing, missing_embeddings):
            write_cache(args.model, chunk, embedding)
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
                "model": args.model,
                "chunk_count": len(embeddings),
                "embedding": average_embedding(embeddings),
            }
        )

    output = {
        "model": args.model,
        "max_tokens": args.max_tokens,
        "overlap": args.overlap,
        "texts": text_records,
        "chunks": chunk_records,
        "cache_hits": total_cache_hits,
        "cache_misses": len(missing),
        "api_tokens": total_api_tokens,
    }
    write_json(OUTPUT_DIR / "embeddings.json", output)

    print(f"Texts: {len(text_records)}")
    print(f"Chunks: {len(chunk_records)}")
    print(f"Cache hits: {total_cache_hits}")
    print(f"Cache misses: {len(missing)}")
    print(f"API tokens: {total_api_tokens}")
    print(f"Wrote {(OUTPUT_DIR / 'embeddings.json').relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
