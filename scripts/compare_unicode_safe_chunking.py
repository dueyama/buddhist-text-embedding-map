#!/usr/bin/env python3
"""Compare v1 token-slice decoding with Unicode-safe chunk boundaries.

This script uses the sect-sutra corpus for the published paper only. It does not write raw
or chunk text to public outputs. Embedding cache and detailed JSON outputs
remain under experiments/sect_sutra_map/outputs/, which is ignored by git.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import tiktoken

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "okyou-matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "okyou-cache"))

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ROOT = PROJECT_ROOT / "experiments" / "sect_sutra_map"
sys.path.insert(0, str(EXPERIMENT_ROOT))

from common import (  # noqa: E402
    OUTPUT_DIR,
    PROCESSED_DIR,
    load_json,
    load_project_env,
    normalize_text,
    sha256_text,
    write_json,
)


MODEL = os.getenv("OKYOU_EMBEDDING_MODEL", "text-embedding-3-large")
MAX_TOKENS = int(os.getenv("OKYOU_MAX_TOKENS", "700"))
OVERLAP = int(os.getenv("OKYOU_OVERLAP", "100"))
BATCH_SIZE = int(os.getenv("OKYOU_EMBEDDING_BATCH_SIZE", "64"))
API_URL = os.getenv("OPENAI_EMBEDDINGS_URL", "https://api.openai.com/v1/embeddings")
SAFE_CACHE_PATH = OUTPUT_DIR / f"unicode_safe_embedding_cache_{MODEL}_{MAX_TOKENS}_{OVERLAP}.json"
META_PATH = OUTPUT_DIR / f"unicode_safe_chunking_comparison_{MODEL}_{MAX_TOKENS}_{OVERLAP}.json"
PUBLIC_PNG_PATH = PROJECT_ROOT / "docs" / "figures" / "unicode-safe-chunking-centroids.png"
PUBLIC_EN_PNG_PATH = PROJECT_ROOT / "docs" / "figures" / "en" / "unicode-safe-chunking-centroids.png"
FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc"

SECT_COLORS = {
    "浄土宗": "#2563eb",
    "浄土真宗": "#1d4ed8",
    "時宗": "#60a5fa",
    "天台宗": "#7c3aed",
    "日蓮宗": "#a855f7",
    "真言宗": "#dc2626",
    "曹洞宗": "#15803d",
    "臨済宗": "#16a34a",
    "黄檗宗": "#65a30d",
    "華厳宗": "#ca8a04",
    "法相宗": "#0891b2",
}

SHORT_LABELS = {
    "t0360_larger_sukhavati": "無量寿経",
    "t0365_meditation_sutra": "観無量寿経",
    "t0366_amida_sutra": "阿弥陀経",
    "t0367_praise_pure_land": "稱讃淨土経",
    "kyogyoshinsho": "教行信証",
    "t0262_lotus_sutra": "法華経",
    "t0262_kannon_chapter": "観音経",
    "t0848_maha_vairocana": "大日経",
    "t0865_vajrasekhara": "金剛頂経",
    "t0243_rishu_kyo": "理趣経",
    "t0251_heart_sutra": "般若心経",
    "t0676_samdhinirmocana": "解深密経",
    "t0235_diamond_sutra": "金剛経",
    "t0475_vimalakirti": "維摩経",
    "t0279_flower_garland": "華厳経",
}

SHORT_LABELS_EN = {
    "t0360_larger_sukhavati": "Larger Sutra",
    "t0365_meditation_sutra": "Contemplation",
    "t0366_amida_sutra": "Amitabha",
    "t0367_praise_pure_land": "Praise Pure Land",
    "kyogyoshinsho": "Kyogyoshinsho",
    "t0262_lotus_sutra": "Lotus",
    "t0262_kannon_chapter": "Kannon chapter",
    "t0848_maha_vairocana": "Mahavairocana",
    "t0865_vajrasekhara": "Vajrasekhara",
    "t0243_rishu_kyo": "Rishukyo",
    "t0251_heart_sutra": "Heart Sutra",
    "t0676_samdhinirmocana": "Samdhinirmocana",
    "t0235_diamond_sutra": "Diamond",
    "t0475_vimalakirti": "Vimalakirti",
    "t0279_flower_garland": "Huayan",
}


@dataclass
class TextLine:
    line_ref: str
    char_start: int
    char_end: int


@dataclass
class WorkText:
    meta: dict[str, Any]
    body: str
    lines: list[TextLine]
    token_offsets: list[int]


@dataclass
class Chunk:
    strategy: str
    chunk_id: str
    text_id: str
    chunk_index: int
    text: str
    token_start: int
    token_end: int
    char_start: int
    char_end: int
    line_start: str
    line_end: str
    source_token_count: int
    actual_token_count: int


def rounded(value: float | None, digits: int = 6) -> float | None:
    if value is None:
        return None
    return round(float(value), digits)


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    return float(np.quantile(np.array(values, dtype=float), q))


def distribution(values: list[int]) -> dict[str, Any]:
    if not values:
        return {"count": 0}
    arr = np.array(values, dtype=float)
    return {
        "count": len(values),
        "min": int(arr.min()),
        "p10": rounded(percentile(values, 0.1), 3),
        "median": rounded(percentile(values, 0.5), 3),
        "mean": rounded(float(arr.mean()), 3),
        "p90": rounded(percentile(values, 0.9), 3),
        "max": int(arr.max()),
    }


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def normalize_rows(matrix: np.ndarray) -> np.ndarray:
    denom = np.linalg.norm(matrix, axis=1, keepdims=True)
    denom[denom == 0] = 1.0
    return matrix / denom


def pca_2d(matrix: np.ndarray) -> tuple[np.ndarray, list[float]]:
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    u, s, _ = np.linalg.svd(centered, full_matrices=False)
    coords = u[:, :2] * s[:2]
    variances = s**2
    total = float(np.sum(variances)) or 1.0
    return coords, [float(variances[0] / total), float(variances[1] / total)]


def setup_plot_style() -> font_manager.FontProperties:
    font = font_manager.FontProperties(fname=FONT_PATH)
    plt.rcParams["font.family"] = font.get_name()
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 160
    return font


def axis_label(label: str, ratio: float) -> str:
    return f"{label} ({ratio * 100:.1f}%)"


def short_label(text_id: str, lang: str) -> str:
    labels = SHORT_LABELS_EN if lang == "en" else SHORT_LABELS
    return labels.get(text_id, text_id)


def first_sect(text: dict[str, Any]) -> str:
    sects = text.get("sects") or []
    return sects[0] if sects else ""


def char_ngrams(text: str, min_n: int = 2, max_n: int = 4) -> Counter[str]:
    compact = "".join(text.split())
    counts: Counter[str] = Counter()
    for n in range(min_n, max_n + 1):
        for index in range(0, max(0, len(compact) - n + 1)):
            counts[compact[index : index + n]] += 1
    return counts


def build_tfidf_vectors(chunks: list[Chunk], vocab_size: int = 8000) -> np.ndarray:
    doc_counts = [char_ngrams(chunk.text) for chunk in chunks]
    df: Counter[str] = Counter()
    for counts in doc_counts:
        df.update(counts.keys())
    max_df = int(len(chunks) * 0.96)
    candidates = {term: freq for term, freq in df.items() if 2 <= freq <= max_df}
    vocab = [term for term, _ in Counter(candidates).most_common(vocab_size)]
    index = {term: col for col, term in enumerate(vocab)}
    matrix = np.zeros((len(chunks), len(vocab)), dtype=float)
    for row, counts in enumerate(doc_counts):
        total = sum(counts.values()) or 1
        for term, count in counts.items():
            col = index.get(term)
            if col is None:
                continue
            tf = count / total
            idf = math.log((1 + len(chunks)) / (1 + df[term])) + 1
            matrix[row, col] = tf * idf
    return normalize_rows(matrix)


def line_for_char(lines: list[TextLine], char_pos: int) -> str:
    if not lines:
        return ""
    if char_pos <= 0:
        return lines[0].line_ref
    if char_pos >= lines[-1].char_end:
        return lines[-1].line_ref
    lo = 0
    hi = len(lines) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        line = lines[mid]
        if line.char_start <= char_pos < line.char_end:
            return line.line_ref
        if char_pos < line.char_start:
            hi = mid - 1
        else:
            lo = mid + 1
    return lines[max(0, min(lo, len(lines) - 1))].line_ref


def load_lines(path: Path) -> tuple[str, list[TextLine]]:
    rows: list[TextLine] = []
    body_parts: list[str] = []
    cursor = 0
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        try:
            ref, line_body = raw_line.split("\t", 1)
        except ValueError:
            ref, line_body = "", raw_line
        normalized = normalize_text([line_body])
        if not normalized:
            continue
        start = cursor
        end = start + len(normalized)
        rows.append(TextLine(line_ref=ref, char_start=start, char_end=end))
        body_parts.append(normalized)
        cursor = end
    return "".join(body_parts), rows


def load_works(encoder: tiktoken.Encoding) -> list[WorkText]:
    corpus_path = PROCESSED_DIR / "corpus_index.json"
    if not corpus_path.exists():
        raise SystemExit("Run experiments/sect_sutra_map/build_corpus.py first.")
    corpus = load_json(corpus_path)
    works: list[WorkText] = []
    for meta in corpus["texts"]:
        body_path = PROJECT_ROOT / meta["body_path"]
        line_path = PROJECT_ROOT / meta["line_path"]
        body = body_path.read_text(encoding="utf-8").strip()
        line_body, lines = load_lines(line_path)
        if body != line_body:
            raise ValueError(f"{meta['id']}: body and line TSV normalization do not match")
        if "\ufffd" in body:
            raise ValueError(f"{meta['id']}: prepared body already contains U+FFFD")
        tokens = encoder.encode(body)
        decoded, offsets = encoder.decode_with_offsets(tokens)
        if decoded != body:
            raise ValueError(f"{meta['id']}: decode_with_offsets did not round-trip body")
        works.append(WorkText(meta=meta, body=body, lines=lines, token_offsets=offsets))
    return works


def make_unsafe_chunks(work: WorkText, encoder: tiktoken.Encoding) -> list[Chunk]:
    tokens = encoder.encode(work.body)
    step = MAX_TOKENS - OVERLAP
    chunks: list[Chunk] = []
    for chunk_index, token_start in enumerate(range(0, len(tokens), step)):
        token_end = min(token_start + MAX_TOKENS, len(tokens))
        if token_end - token_start < MAX_TOKENS // 4 and chunks:
            break
        text = encoder.decode(tokens[token_start:token_end])
        char_start = work.token_offsets[token_start] if token_start < len(tokens) else len(work.body)
        char_end = work.token_offsets[token_end] if token_end < len(tokens) else len(work.body)
        line_start = line_for_char(work.lines, char_start)
        line_end = line_for_char(work.lines, max(char_start, char_end - 1))
        chunks.append(
            Chunk(
                strategy="unsafe_token_decode",
                chunk_id=f"{work.meta['id']}::chunk_{chunk_index:04d}",
                text_id=work.meta["id"],
                chunk_index=chunk_index,
                text=text,
                token_start=token_start,
                token_end=token_end,
                char_start=char_start,
                char_end=char_end,
                line_start=line_start,
                line_end=line_end,
                source_token_count=token_end - token_start,
                actual_token_count=len(encoder.encode(text)),
            )
        )
    return chunks


def make_safe_chunks(work: WorkText, encoder: tiktoken.Encoding) -> list[Chunk]:
    tokens = encoder.encode(work.body)
    step = MAX_TOKENS - OVERLAP
    chunks: list[Chunk] = []
    for chunk_index, token_start in enumerate(range(0, len(tokens), step)):
        token_end = min(token_start + MAX_TOKENS, len(tokens))
        char_start = work.token_offsets[token_start] if token_start < len(tokens) else len(work.body)
        char_end = work.token_offsets[token_end] if token_end < len(tokens) else len(work.body)
        text = work.body[char_start:char_end]
        actual_token_count = len(encoder.encode(text))
        while actual_token_count > MAX_TOKENS and token_end > token_start:
            token_end -= 1
            char_end = work.token_offsets[token_end] if token_end < len(tokens) else len(work.body)
            text = work.body[char_start:char_end]
            actual_token_count = len(encoder.encode(text))
        if actual_token_count < MAX_TOKENS // 4 and chunks:
            break
        if "\ufffd" in text:
            raise ValueError(f"{work.meta['id']} safe chunk {chunk_index} contains U+FFFD")
        line_start = line_for_char(work.lines, char_start)
        line_end = line_for_char(work.lines, max(char_start, char_end - 1))
        chunks.append(
            Chunk(
                strategy="safe_unicode_700",
                chunk_id=f"{work.meta['id']}::chunk_{chunk_index:04d}",
                text_id=work.meta["id"],
                chunk_index=chunk_index,
                text=text,
                token_start=token_start,
                token_end=token_end,
                char_start=char_start,
                char_end=char_end,
                line_start=line_start,
                line_end=line_end,
                source_token_count=token_end - token_start,
                actual_token_count=actual_token_count,
            )
        )
    return chunks


def chunk_stats(chunks: list[Chunk]) -> dict[str, Any]:
    return {
        "chunk_count": len(chunks),
        "affected_chunks": sum(1 for chunk in chunks if "\ufffd" in chunk.text),
        "replacement_chars": sum(chunk.text.count("\ufffd") for chunk in chunks),
        "source_token_count": distribution([chunk.source_token_count for chunk in chunks]),
        "actual_token_count": distribution([chunk.actual_token_count for chunk in chunks]),
        "char_count": distribution([len(chunk.text) for chunk in chunks]),
    }


def load_existing_unsafe_vectors(chunks: list[Chunk]) -> np.ndarray:
    embeddings_path = OUTPUT_DIR / "embeddings.json"
    if not embeddings_path.exists():
        raise SystemExit("Existing v1 embeddings are missing: experiments/sect_sutra_map/outputs/embeddings.json")
    data = load_json(embeddings_path)
    if data.get("model") != MODEL:
        raise ValueError(f"Existing embeddings model is {data.get('model')!r}, expected {MODEL!r}")
    by_id = {record["chunk_id"]: record for record in data["chunks"]}
    vectors: list[list[float]] = []
    for chunk in chunks:
        record = by_id.get(chunk.chunk_id)
        if record is None:
            raise ValueError(f"Missing existing embedding for {chunk.chunk_id}")
        if record.get("chunk_sha256") != sha256_text(chunk.text):
            raise ValueError(f"Existing embedding hash mismatch for {chunk.chunk_id}")
        vectors.append(record["embedding"])
    return np.array(vectors, dtype=float)


def load_safe_cache() -> dict[str, Any]:
    if SAFE_CACHE_PATH.exists():
        cache = load_json(SAFE_CACHE_PATH)
        if cache.get("model") == MODEL and cache.get("max_tokens") == MAX_TOKENS and cache.get("overlap") == OVERLAP:
            cache.setdefault("embeddings", {})
            return cache
    return {"model": MODEL, "max_tokens": MAX_TOKENS, "overlap": OVERLAP, "embeddings": {}}


def save_safe_cache(cache: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = SAFE_CACHE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    tmp.replace(SAFE_CACHE_PATH)


def request_embeddings(inputs: list[str]) -> list[list[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    payload = json.dumps({"model": MODEL, "input": inputs}).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI embeddings HTTP {exc.code}: {detail[:600]}") from exc
    data = json.loads(body)
    return [item["embedding"] for item in sorted(data["data"], key=lambda item: item["index"])]


def get_safe_vectors(chunks: list[Chunk], allow_api: bool) -> np.ndarray:
    cache = load_safe_cache()
    embeddings: dict[str, Any] = cache["embeddings"]
    missing: list[Chunk] = []
    for chunk in chunks:
        key = f"{chunk.strategy}:{chunk.chunk_id}"
        text_sha = sha256_text(chunk.text)
        record = embeddings.get(key)
        if record and record.get("text_sha256") == text_sha:
            continue
        missing.append(chunk)

    if missing and not allow_api:
        raise SystemExit(f"{len(missing)} safe chunks are missing from cache. Re-run with --embeddings after API approval.")

    for start in range(0, len(missing), BATCH_SIZE):
        batch = missing[start : start + BATCH_SIZE]
        vectors = request_embeddings([chunk.text for chunk in batch])
        for chunk, vector in zip(batch, vectors):
            embeddings[f"{chunk.strategy}:{chunk.chunk_id}"] = {
                "text_sha256": sha256_text(chunk.text),
                "strategy": chunk.strategy,
                "text_id": chunk.text_id,
                "chunk_index": chunk.chunk_index,
                "line_start": chunk.line_start,
                "line_end": chunk.line_end,
                "source_token_count": chunk.source_token_count,
                "actual_token_count": chunk.actual_token_count,
                "embedding": vector,
            }
        save_safe_cache(cache)
        done = min(start + len(batch), len(missing))
        print(f"embedded safe chunks {done}/{len(missing)}")
        if done < len(missing):
            time.sleep(0.3)

    return np.array(
        [embeddings[f"{chunk.strategy}:{chunk.chunk_id}"]["embedding"] for chunk in chunks],
        dtype=float,
    )


def vector_summary(values: list[float]) -> dict[str, Any]:
    return {
        "count": len(values),
        "min": rounded(min(values) if values else None),
        "p10": rounded(percentile(values, 0.1)),
        "median": rounded(percentile(values, 0.5)),
        "mean": rounded(float(np.mean(values)) if values else None),
        "p90": rounded(percentile(values, 0.9)),
        "max": rounded(max(values) if values else None),
    }


def text_centroids(chunks: list[Chunk], vectors: np.ndarray) -> dict[str, np.ndarray]:
    by_text: dict[str, list[int]] = defaultdict(list)
    for index, chunk in enumerate(chunks):
        by_text[chunk.text_id].append(index)
    return {text_id: vectors[indices].mean(axis=0) for text_id, indices in by_text.items()}


def build_sect_centroids(texts: list[dict[str, Any]], centroids: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    by_sect: dict[str, list[np.ndarray]] = defaultdict(list)
    for text in texts:
        if text.get("layer") not in {"core_sutra", "founder_text"}:
            continue
        vector = centroids.get(text["id"])
        if vector is None:
            continue
        for sect in text["sects"]:
            by_sect[sect].append(vector)
    return {sect: np.array(vectors, dtype=float).mean(axis=0) for sect, vectors in by_sect.items() if vectors}


def embedding_summary(
    texts: list[dict[str, Any]],
    unsafe_chunks: list[Chunk],
    safe_chunks: list[Chunk],
    unsafe_vectors: np.ndarray,
    safe_vectors: np.ndarray,
) -> dict[str, Any]:
    unsafe_norm = normalize_rows(unsafe_vectors)
    safe_norm = normalize_rows(safe_vectors)
    paired_by_text: dict[str, list[float]] = defaultdict(list)
    for index, (unsafe_chunk, safe_chunk) in enumerate(zip(unsafe_chunks, safe_chunks)):
        if unsafe_chunk.text_id != safe_chunk.text_id or unsafe_chunk.chunk_index != safe_chunk.chunk_index:
            raise ValueError("Unsafe/safe chunk order mismatch")
        paired_by_text[unsafe_chunk.text_id].append(cosine(unsafe_norm[index], safe_norm[index]))

    old_text = text_centroids(unsafe_chunks, unsafe_vectors)
    new_text = text_centroids(safe_chunks, safe_vectors)
    text_cosines = {
        text["id"]: rounded(cosine(old_text[text["id"]], new_text[text["id"]]))
        for text in texts
        if text["id"] in old_text and text["id"] in new_text
    }
    old_sect = build_sect_centroids(texts, old_text)
    new_sect = build_sect_centroids(texts, new_text)
    sect_cosines = {
        sect: rounded(cosine(old_sect[sect], new_sect[sect]))
        for sect in sorted(old_sect)
        if sect in new_sect
    }
    return {
        "same_index_chunk_cosine_by_text": {
            text_id: vector_summary(values) for text_id, values in sorted(paired_by_text.items())
        },
        "same_index_chunk_cosine_overall": vector_summary(
            [value for values in paired_by_text.values() for value in values]
        ),
        "text_centroid_old_safe_cosine": text_cosines,
        "text_centroid_old_safe_cosine_summary": vector_summary(list(text_cosines.values())),
        "sect_centroid_old_safe_cosine": sect_cosines,
        "sect_centroid_old_safe_cosine_summary": vector_summary(list(sect_cosines.values())),
    }


def local_text_summary(
    texts: list[dict[str, Any]],
    unsafe_chunks: list[Chunk],
    safe_chunks: list[Chunk],
) -> tuple[dict[str, Any], np.ndarray, np.ndarray]:
    vectors = build_tfidf_vectors(unsafe_chunks + safe_chunks)
    unsafe_vectors = vectors[: len(unsafe_chunks)]
    safe_vectors = vectors[len(unsafe_chunks) :]
    paired_by_text: dict[str, list[float]] = defaultdict(list)
    for index, (unsafe_chunk, safe_chunk) in enumerate(zip(unsafe_chunks, safe_chunks)):
        if unsafe_chunk.text_id != safe_chunk.text_id or unsafe_chunk.chunk_index != safe_chunk.chunk_index:
            raise ValueError("Unsafe/safe chunk order mismatch")
        paired_by_text[unsafe_chunk.text_id].append(cosine(unsafe_vectors[index], safe_vectors[index]))
    old_text = text_centroids(unsafe_chunks, unsafe_vectors)
    new_text = text_centroids(safe_chunks, safe_vectors)
    text_cosines = {
        text["id"]: rounded(cosine(old_text[text["id"]], new_text[text["id"]]))
        for text in texts
        if text["id"] in old_text and text["id"] in new_text
    }
    return (
        {
            "method": "supplemental character 2-4 gram TF-IDF on local old and safe chunks; this is not an embedding-model comparison",
            "same_index_chunk_cosine_by_text": {
                text_id: vector_summary(values) for text_id, values in sorted(paired_by_text.items())
            },
            "same_index_chunk_cosine_overall": vector_summary(
                [value for values in paired_by_text.values() for value in values]
            ),
            "text_centroid_old_safe_cosine": text_cosines,
            "text_centroid_old_safe_cosine_summary": vector_summary(list(text_cosines.values())),
        },
        unsafe_vectors,
        safe_vectors,
    )


def render_centroid_png(
    texts: list[dict[str, Any]],
    old_centroids: dict[str, np.ndarray],
    new_centroids: dict[str, np.ndarray],
    output_path: Path,
    *,
    lang: str,
) -> dict[str, Any]:
    ordered = [text for text in texts if text["id"] in old_centroids and text["id"] in new_centroids]
    vectors = [old_centroids[text["id"]] for text in ordered] + [new_centroids[text["id"]] for text in ordered]
    coords, ratio = pca_2d(normalize_rows(np.array(vectors, dtype=float)))
    old_coords = coords[: len(ordered)]
    new_coords = coords[len(ordered) :]
    shifts = np.linalg.norm(new_coords - old_coords, axis=1)
    font = setup_plot_style()

    fig, ax = plt.subplots(figsize=(9.8, 7.2))
    for text, old, new in zip(ordered, old_coords, new_coords):
        color = SECT_COLORS.get(first_sect(text), "#64748b")
        ax.plot(
            [old[0], new[0]],
            [old[1], new[1]],
            color="#94a3b8",
            linewidth=0.9,
            alpha=0.75,
            zorder=2,
        )
        ax.scatter(
            old[0],
            old[1],
            s=58,
            marker="o",
            facecolor="white",
            edgecolor=color,
            linewidth=1.4,
            zorder=3,
        )
        ax.scatter(
            new[0],
            new[1],
            s=64,
            marker="o",
            color=color,
            edgecolor="white",
            linewidth=0.8,
            zorder=4,
        )
        ax.text(
            new[0] + 0.003,
            new[1] + 0.003,
            short_label(text["id"], lang),
            fontsize=8.5,
            fontproperties=font,
            color="#0f172a",
            zorder=5,
        )

    ax.axhline(0, color="#cbd5e1", linewidth=0.8, zorder=1)
    ax.axvline(0, color="#cbd5e1", linewidth=0.8, zorder=1)
    ax.grid(color="#e2e8f0", linewidth=0.7)
    if lang == "en":
        title = "Text Centroids Before and After Unicode-Aware Boundary Adjustment"
        pc1 = "PCA axis 1"
        pc2 = "PCA axis 2"
        old_label = "old method"
        revised_label = "revised method"
    else:
        title = "文字境界調整前後の本文重心比較"
        pc1 = "PCA 第1軸"
        pc2 = "PCA 第2軸"
        old_label = "旧方式"
        revised_label = "改訂方式"
    ax.set_title(title, fontproperties=font, fontsize=15, pad=12)
    ax.set_xlabel(axis_label(pc1, ratio[0]), fontproperties=font)
    ax.set_ylabel(axis_label(pc2, ratio[1]), fontproperties=font)
    handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor="white",
            markeredgecolor="#334155",
            markeredgewidth=1.3,
            markersize=7,
        ),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#334155", markersize=7),
        plt.Line2D([0], [0], color="#94a3b8", linewidth=1),
    ]
    labels = [old_label, revised_label, "same text" if lang == "en" else "同一本文"]
    ax.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=3,
        fontsize=8,
        prop=font,
        frameon=False,
        columnspacing=1.6,
        handletextpad=0.5,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    return {
        "method": "PCA via centered NumPy SVD on old and revised text centroids after L2 normalization",
        "pca_explained_variance_ratio": [rounded(value) for value in ratio],
        "shift_distance_summary": vector_summary([float(value) for value in shifts]),
        "png_path": str(output_path.relative_to(PROJECT_ROOT)),
    }


def build_summary(
    works: list[WorkText],
    unsafe_chunks: list[Chunk],
    safe_chunks: list[Chunk],
    unsafe_vectors: np.ndarray | None,
    safe_vectors: np.ndarray | None,
    *,
    include_local_text: bool,
) -> dict[str, Any]:
    texts = [work.meta for work in works]
    chunks = unsafe_chunks + safe_chunks
    by_strategy: dict[str, list[Chunk]] = defaultdict(list)
    by_strategy_text: dict[tuple[str, str], list[Chunk]] = defaultdict(list)
    for chunk in chunks:
        by_strategy[chunk.strategy].append(chunk)
        by_strategy_text[(chunk.strategy, chunk.text_id)].append(chunk)

    summary: dict[str, Any] = {
        "title": "Unicode-safe chunking comparison for the sect-sutra corpus",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "method": {
            "model": MODEL,
            "tokenizer": "tiktoken cl100k_base",
            "max_tokens": MAX_TOKENS,
            "overlap": OVERLAP,
            "unsafe_token_decode": "encode full processed body, slice token ids, decode each slice with encoder.decode",
            "safe_unicode_700": "use the same token grid, then use tiktoken.decode_with_offsets offsets to cut Python Unicode string boundaries",
            "raw_text_policy": "metadata excludes raw/chunk text; local cache stores hashes and embeddings only",
        },
        "sources": [
            {
                "id": text["id"],
                "title": text["title"],
                "source": text["source"],
                "source_url": text.get("source_url", ""),
                "sects": text["sects"],
                "layer": text["layer"],
                "line_count": text["line_count"],
                "char_count": text["char_count"],
                "body_sha256": text["body_sha256"],
            }
            for text in texts
        ],
        "strategy_stats": {strategy: chunk_stats(items) for strategy, items in sorted(by_strategy.items())},
        "strategy_text_stats": {
            f"{strategy}:{text_id}": chunk_stats(items)
            for (strategy, text_id), items in sorted(by_strategy_text.items())
        },
        "chunk_records": [
            {
                "chunk_id": chunk.chunk_id,
                "strategy": chunk.strategy,
                "text_id": chunk.text_id,
                "chunk_index": chunk.chunk_index,
                "line_start": chunk.line_start,
                "line_end": chunk.line_end,
                "token_start": chunk.token_start,
                "token_end": chunk.token_end,
                "source_token_count": chunk.source_token_count,
                "actual_token_count": chunk.actual_token_count,
                "char_start": chunk.char_start,
                "char_end": chunk.char_end,
                "char_count": len(chunk.text),
                "replacement_chars": chunk.text.count("\ufffd"),
                "text_sha256": sha256_text(chunk.text),
            }
            for chunk in chunks
        ],
    }

    if unsafe_vectors is not None and safe_vectors is not None:
        summary["embedding_comparison"] = embedding_summary(
            texts, unsafe_chunks, safe_chunks, unsafe_vectors, safe_vectors
        )
        old_text = text_centroids(unsafe_chunks, unsafe_vectors)
        new_text = text_centroids(safe_chunks, safe_vectors)
        projection = render_centroid_png(texts, old_text, new_text, PUBLIC_PNG_PATH, lang="ja")
        render_centroid_png(texts, old_text, new_text, PUBLIC_EN_PNG_PATH, lang="en")
        summary["projection"] = projection
    if include_local_text:
        local_summary, local_old, local_new = local_text_summary(texts, unsafe_chunks, safe_chunks)
        summary["local_text_comparison"] = local_summary
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--embeddings", action="store_true", help="Use existing old embeddings and embed safe chunks if needed.")
    parser.add_argument("--no-api", action="store_true", help="With --embeddings, require safe embeddings to be cached already.")
    parser.add_argument("--skip-local-text", action="store_true", help="Skip supplemental local character n-gram comparison and SVG.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if MAX_TOKENS <= OVERLAP:
        raise ValueError("OKYOU_MAX_TOKENS must be larger than OKYOU_OVERLAP.")
    if args.embeddings:
        load_project_env()

    encoder = tiktoken.get_encoding("cl100k_base")
    works = load_works(encoder)
    unsafe_chunks: list[Chunk] = []
    safe_chunks: list[Chunk] = []
    for work in works:
        unsafe_chunks.extend(make_unsafe_chunks(work, encoder))
        safe_chunks.extend(make_safe_chunks(work, encoder))

    if len(unsafe_chunks) != len(safe_chunks):
        raise ValueError(f"Chunk count mismatch: unsafe={len(unsafe_chunks)} safe={len(safe_chunks)}")
    for old, new in zip(unsafe_chunks, safe_chunks):
        if old.text_id != new.text_id or old.chunk_index != new.chunk_index:
            raise ValueError("Unsafe/safe chunk grid mismatch")

    unsafe_vectors = None
    safe_vectors = None
    if args.embeddings:
        unsafe_vectors = load_existing_unsafe_vectors(unsafe_chunks)
        safe_vectors = get_safe_vectors(safe_chunks, allow_api=not args.no_api)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = build_summary(
        works,
        unsafe_chunks,
        safe_chunks,
        unsafe_vectors,
        safe_vectors,
        include_local_text=not args.skip_local_text,
    )
    write_json(META_PATH, summary)

    print(f"wrote {META_PATH.relative_to(PROJECT_ROOT)}")
    if args.embeddings:
        print(f"wrote {PUBLIC_PNG_PATH.relative_to(PROJECT_ROOT)}")
        print(f"wrote {PUBLIC_EN_PNG_PATH.relative_to(PROJECT_ROOT)}")
    for strategy in ["unsafe_token_decode", "safe_unicode_700"]:
        stats = summary["strategy_stats"][strategy]
        print(
            f"{strategy}: chunks={stats['chunk_count']} affected={stats['affected_chunks']} "
            f"replacement_chars={stats['replacement_chars']} actual_tokens_median={stats['actual_token_count'].get('median')}"
        )


if __name__ == "__main__":
    main()
