#!/usr/bin/env python3
"""Compare Unicode-aware chunking effects on the three-layer source-mixture analysis."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import tiktoken
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ROOT = PROJECT_ROOT / "experiments" / "sect_sutra_map"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(EXPERIMENT_ROOT))

from compare_unicode_safe_chunking import (  # noqa: E402
    MODEL,
    Chunk,
    get_safe_vectors,
    load_existing_unsafe_vectors,
    load_works,
    make_safe_chunks,
    make_unsafe_chunks,
    normalize_rows,
    rounded,
    vector_summary,
)
from common import OUTPUT_DIR, write_json  # noqa: E402
from make_three_layer_figures import (  # noqa: E402
    CITATION_SMOOTHING_WINDOW,
    LEXICAL_TEMPERATURE,
    REFERENCE_MARKERS,
    SEMANTIC_TEMPERATURE,
    SOURCE_IDS,
    SOURCE_LABELS,
    SOURCE_MIXTURE_SMOOTHING_WINDOW,
    TARGET_ID,
    normalize_citation_weights,
    normalize_cjk,
    smooth,
    softmax_weights,
    volume_annotations,
    volume_layer_means,
)

SUMMARY_PATH = OUTPUT_DIR / f"unicode_safe_three_layer_comparison_{MODEL}_700_100.json"
RELEVANT_IDS = [TARGET_ID] + SOURCE_IDS


def cosine_summary(old: np.ndarray, new: np.ndarray) -> dict[str, Any]:
    old_norm = normalize_rows(old)
    new_norm = normalize_rows(new)
    values = [float(np.dot(old_norm[index], new_norm[index])) for index in range(old.shape[0])]
    return vector_summary(values)


def chunks_by_text(chunks: list[Chunk]) -> dict[str, list[Chunk]]:
    grouped: dict[str, list[Chunk]] = {text_id: [] for text_id in RELEVANT_IDS}
    for chunk in chunks:
        if chunk.text_id in grouped:
            grouped[chunk.text_id].append(chunk)
    for items in grouped.values():
        items.sort(key=lambda chunk: chunk.chunk_index)
    return grouped


def vectors_by_text(chunks: list[Chunk], vectors: np.ndarray) -> dict[str, np.ndarray]:
    pairs = [
        (chunk, vectors[index])
        for index, chunk in enumerate(chunks)
        if chunk.text_id in RELEVANT_IDS
    ]
    grouped: dict[str, list[tuple[int, np.ndarray]]] = {text_id: [] for text_id in RELEVANT_IDS}
    for chunk, vector in pairs:
        grouped[chunk.text_id].append((chunk.chunk_index, vector))
    return {
        text_id: np.array([vector for _, vector in sorted(items)], dtype=float)
        for text_id, items in grouped.items()
    }


def chunk_texts_by_text(chunks: list[Chunk]) -> dict[str, list[str]]:
    grouped = chunks_by_text(chunks)
    return {text_id: [chunk.text for chunk in items] for text_id, items in grouped.items()}


def semantic_source_scores(vectors: dict[str, np.ndarray]) -> np.ndarray:
    target = normalize_rows(vectors[TARGET_ID])
    columns = []
    for source_id in SOURCE_IDS:
        source = normalize_rows(vectors[source_id])
        columns.append((target @ source.T).max(axis=1))
    return np.column_stack(columns)


def lexical_source_scores(chunk_texts: dict[str, list[str]]) -> tuple[np.ndarray, float]:
    target_chunks = chunk_texts[TARGET_ID]
    source_chunks = [chunk for source_id in SOURCE_IDS for chunk in chunk_texts[source_id]]
    source_offsets: list[tuple[int, int]] = []
    cursor = 0
    for source_id in SOURCE_IDS:
        next_cursor = cursor + len(chunk_texts[source_id])
        source_offsets.append((cursor, next_cursor))
        cursor = next_cursor

    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 5), lowercase=False, norm="l2")
    matrix = vectorizer.fit_transform(target_chunks + source_chunks)
    target_matrix = matrix[: len(target_chunks)]
    source_matrix = matrix[len(target_chunks) :]
    similarities = cosine_similarity(target_matrix, source_matrix)
    columns = [similarities[:, start:end].max(axis=1) for start, end in source_offsets]

    full_vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 5), lowercase=False, norm="l2")
    full_matrix = full_vectorizer.fit_transform(
        [
            "".join(chunk_texts["t0366_amida_sutra"]),
            "".join(chunk_texts["t0367_praise_pure_land"]),
        ]
    )
    amida_pair = float(cosine_similarity(full_matrix[0], full_matrix[1])[0, 0])
    return np.column_stack(columns), amida_pair


def citation_source_scores(chunk_texts: dict[str, list[str]]) -> np.ndarray:
    rows = []
    for chunk in chunk_texts[TARGET_ID]:
        normalized = normalize_cjk(chunk)
        values = []
        for source_id in SOURCE_IDS:
            score = 0.0
            for marker in REFERENCE_MARKERS[source_id]:
                if normalize_cjk(marker) in normalized:
                    score += 1.0
            values.append(score)
        rows.append(values)
    return np.array(rows, dtype=float)


def layer_weights(scores: np.ndarray, layer: str) -> np.ndarray:
    if layer == "semantic":
        return smooth(
            softmax_weights(scores, temperature=SEMANTIC_TEMPERATURE),
            window=SOURCE_MIXTURE_SMOOTHING_WINDOW,
        )
    if layer == "lexical":
        return smooth(
            softmax_weights(scores, temperature=LEXICAL_TEMPERATURE),
            window=SOURCE_MIXTURE_SMOOTHING_WINDOW,
        )
    if layer == "citation":
        return smooth(normalize_citation_weights(scores), window=CITATION_SMOOTHING_WINDOW)
    raise ValueError(layer)


def compare_weights(old: np.ndarray, new: np.ndarray, labels: list[str]) -> dict[str, Any]:
    diff = np.abs(old - new)
    l1 = diff.sum(axis=1)
    old_dom = old.argmax(axis=1)
    new_dom = new.argmax(axis=1)
    changed = old_dom != new_dom
    return {
        "chunk_count": int(old.shape[0]),
        "row_cosine_summary": cosine_summary(old, new),
        "l1_distance_summary": vector_summary([float(value) for value in l1]),
        "max_absolute_weight_delta": rounded(float(diff.max())),
        "dominant_source_match_rate": rounded(float((~changed).mean())),
        "dominant_source_changed_chunks": int(changed.sum()),
        "mean_absolute_delta_by_source": {
            labels[index]: rounded(float(diff[:, index].mean()))
            for index in range(diff.shape[1])
        },
    }


def compare_volume_dominance(
    old_weights: np.ndarray,
    new_weights: np.ndarray,
    ids: list[str],
    volumes: dict[str, Any],
) -> dict[str, Any]:
    old_rows = volume_layer_means(old_weights, ids, volumes)
    new_rows = volume_layer_means(new_weights, ids, volumes)
    rows = []
    changed = 0
    for old, new in zip(old_rows, new_rows):
        changed += int(old["dominant_source"] != new["dominant_source"])
        rows.append(
            {
                "volume": old["volume_label"],
                "chunk_range": old["chunk_range"],
                "old_dominant": SOURCE_LABELS[old["dominant_source"]],
                "old_weight": old["dominant_weight"],
                "revised_dominant": SOURCE_LABELS[new["dominant_source"]],
                "revised_weight": new["dominant_weight"],
                "dominant_changed": old["dominant_source"] != new["dominant_source"],
            }
        )
    return {
        "volume_count": len(rows),
        "dominant_changed_volumes": changed,
        "rows": rows,
    }


def marker_summary(scores: np.ndarray) -> dict[str, Any]:
    detected = scores.sum(axis=1) > 0
    return {
        "target_chunk_count": int(scores.shape[0]),
        "chunks_with_any_marker": int(detected.sum()),
        "total_marker_hits": int(scores.sum()),
        "source_marker_hits": {
            SOURCE_LABELS[source_id]: int(scores[:, index].sum())
            for index, source_id in enumerate(SOURCE_IDS)
        },
    }


def main() -> None:
    encoder = tiktoken.get_encoding("cl100k_base")
    works = load_works(encoder)
    unsafe_chunks: list[Chunk] = []
    safe_chunks: list[Chunk] = []
    for work in works:
        unsafe_chunks.extend(make_unsafe_chunks(work, encoder))
        safe_chunks.extend(make_safe_chunks(work, encoder))

    unsafe_vectors = load_existing_unsafe_vectors(unsafe_chunks)
    safe_vectors = get_safe_vectors(safe_chunks, allow_api=False)
    old_texts = chunk_texts_by_text(unsafe_chunks)
    new_texts = chunk_texts_by_text(safe_chunks)
    old_vectors = vectors_by_text(unsafe_chunks, unsafe_vectors)
    new_vectors = vectors_by_text(safe_chunks, safe_vectors)

    for text_id in RELEVANT_IDS:
        if len(old_texts[text_id]) != len(new_texts[text_id]):
            raise ValueError(f"{text_id}: old/revised chunk count mismatch")

    semantic_old = semantic_source_scores(old_vectors)
    semantic_new = semantic_source_scores(new_vectors)
    lexical_old, old_amida_tfidf = lexical_source_scores(old_texts)
    lexical_new, new_amida_tfidf = lexical_source_scores(new_texts)
    citation_old = citation_source_scores(old_texts)
    citation_new = citation_source_scores(new_texts)

    weights = {
        "semantic": (
            layer_weights(semantic_old, "semantic"),
            layer_weights(semantic_new, "semantic"),
            [SOURCE_LABELS[source_id] for source_id in SOURCE_IDS],
        ),
        "lexical": (
            layer_weights(lexical_old, "lexical"),
            layer_weights(lexical_new, "lexical"),
            [SOURCE_LABELS[source_id] for source_id in SOURCE_IDS],
        ),
        "citation": (
            layer_weights(citation_old, "citation"),
            layer_weights(citation_new, "citation"),
            [SOURCE_LABELS[source_id] for source_id in SOURCE_IDS + ["unmarked"]],
        ),
    }

    target_body = next(work.body for work in works if work.meta["id"] == TARGET_ID)
    volumes = volume_annotations(
        target_body,
        max_tokens=700,
        overlap=100,
        chunk_count=len(old_texts[TARGET_ID]),
    )

    summary = {
        "title": "Unicode-aware chunking comparison for three-layer source mixture",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "model": MODEL,
        "target": TARGET_ID,
        "sources": SOURCE_IDS,
        "source_labels": SOURCE_LABELS,
        "method": {
            "semantic_layer": "source-mixture weights from max target-source chunk embedding cosine",
            "lexical_layer": "source-mixture weights from character 2-5 gram TF-IDF max target-source chunk cosine",
            "citation_layer": "source-marker weights from scripture-title, translator-name, and fixed-phrase dictionary hits",
            "raw_text_policy": "metadata excludes raw/chunk text",
        },
        "layer_comparison": {
            layer: compare_weights(old, new, labels)
            for layer, (old, new, labels) in weights.items()
        },
        "volume_dominance_comparison": {
            "semantic": compare_volume_dominance(weights["semantic"][0], weights["semantic"][1], SOURCE_IDS, volumes),
            "lexical": compare_volume_dominance(weights["lexical"][0], weights["lexical"][1], SOURCE_IDS, volumes),
            "citation": compare_volume_dominance(weights["citation"][0], weights["citation"][1], SOURCE_IDS + ["unmarked"], volumes),
        },
        "lexical_amida_pair_tfidf_cosine": {
            "old": rounded(old_amida_tfidf),
            "revised": rounded(new_amida_tfidf),
            "absolute_delta": rounded(abs(old_amida_tfidf - new_amida_tfidf)),
        },
        "citation_marker_summary": {
            "old": marker_summary(citation_old),
            "revised": marker_summary(citation_new),
            "exact_marker_vector_match_rate": rounded(float(np.all(citation_old == citation_new, axis=1).mean())),
            "changed_marker_vectors": int((~np.all(citation_old == citation_new, axis=1)).sum()),
        },
    }
    write_json(SUMMARY_PATH, summary)

    print(f"wrote {SUMMARY_PATH.relative_to(PROJECT_ROOT)}")
    for layer, item in summary["layer_comparison"].items():
        print(
            f"{layer}: dominant_match={item['dominant_source_match_rate']} "
            f"changed_chunks={item['dominant_source_changed_chunks']} "
            f"mean_l1={item['l1_distance_summary']['mean']} "
            f"max_abs_delta={item['max_absolute_weight_delta']}"
        )
    print(
        "citation markers:",
        summary["citation_marker_summary"]["old"]["chunks_with_any_marker"],
        "->",
        summary["citation_marker_summary"]["revised"]["chunks_with_any_marker"],
        "changed_vectors=",
        summary["citation_marker_summary"]["changed_marker_vectors"],
    )


if __name__ == "__main__":
    main()
