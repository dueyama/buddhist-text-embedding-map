#!/usr/bin/env python3
"""Create lightweight JSON consumed by the static sect sutra viewer."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

from common import OUTPUT_DIR, PROJECT_ROOT, cosine, load_json, write_json


def rounded(value: float, digits: int = 4) -> float:
    return round(float(value), digits)


def stripped_text_record(text: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in text.items() if key != "embedding"}


def stripped_chunk_record(chunk: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in chunk.items() if key != "embedding"}


def build_centroids(texts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sects = sorted({sect for text in texts for sect in text["sects"]})
    centroids = []
    for sect in sects:
        members = [
            text
            for text in texts
            if sect in text["sects"] and text["layer"] in {"core_sutra", "founder_text"}
        ]
        if not members:
            continue
        vector = np.array([text["embedding"] for text in members], dtype=np.float32).mean(axis=0)
        centroids.append(
            {
                "id": f"sect::{sect}",
                "title": sect,
                "sects": [sect],
                "layer": "sect_centroid",
                "member_text_ids": [text["id"] for text in members],
                "embedding": vector.astype(float).tolist(),
            }
        )
    return centroids


def normalize_translator(value: str) -> str:
    for name in ["鳩摩羅什", "玄奘", "不空", "親鸞", "康僧鎧", "畺良耶舍", "善無畏", "一行", "實叉難陀"]:
        if name in value:
            return name
    return value.strip() or "unknown"


def build_translator_centroids(texts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for text in texts:
        translator = normalize_translator(text.get("translator", ""))
        if translator in {"unknown", "親鸞"}:
            continue
        groups.setdefault(translator, []).append(text)

    centroids = []
    for translator, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        vector = np.array([text["embedding"] for text in members], dtype=np.float32).mean(axis=0)
        centroids.append(
            {
                "id": f"translator::{translator}",
                "title": translator,
                "sects": ["訳者"],
                "layer": "translator_centroid",
                "member_text_ids": [text["id"] for text in members],
                "embedding": vector.astype(float).tolist(),
            }
        )
    return centroids


def add_coordinates(records: list[dict[str, Any]]) -> None:
    matrix = np.array([record["embedding"] for record in records], dtype=np.float32)
    if len(records) == 1:
        coords = np.array([[0.0, 0.0]], dtype=np.float32)
    else:
        coords = PCA(n_components=2, random_state=0).fit_transform(matrix)
    for record, coord in zip(records, coords):
        record["x"] = rounded(coord[0])
        record["y"] = rounded(coord[1])


def build_text_similarities(texts: list[dict[str, Any]]) -> dict[str, Any]:
    labels = [text["id"] for text in texts]
    matrix = cosine_similarity(np.array([text["embedding"] for text in texts], dtype=np.float32))
    return {
        "labels": labels,
        "matrix": [[rounded(value) for value in row] for row in matrix],
    }


def build_nearest_texts(texts: list[dict[str, Any]], limit: int = 5) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for text in texts:
        candidates = []
        for other in texts:
            if other["id"] == text["id"]:
                continue
            candidates.append(
                {
                    "id": other["id"],
                    "title": other["title"],
                    "sects": other["sects"],
                    "layer": other["layer"],
                    "score": rounded(cosine(text["embedding"], other["embedding"])),
                }
            )
        result[text["id"]] = sorted(candidates, key=lambda item: item["score"], reverse=True)[:limit]
    return result


def build_nearest_chunks(
    texts: list[dict[str, Any]], chunks: list[dict[str, Any]], limit: int = 5
) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for text in texts:
        candidates = []
        for chunk in chunks:
            if chunk["text_id"] == text["id"]:
                continue
            candidates.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "text_id": chunk["text_id"],
                    "chunk_index": chunk["chunk_index"],
                    "score": rounded(cosine(text["embedding"], chunk["embedding"])),
                    "preview": chunk["preview"],
                }
            )
        result[text["id"]] = sorted(candidates, key=lambda item: item["score"], reverse=True)[:limit]
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(OUTPUT_DIR / "embeddings.json"))
    parser.add_argument("--output", default=str(OUTPUT_DIR / "viewer_data.json"))
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.is_absolute():
        input_path = PROJECT_ROOT / input_path
    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path

    embeddings = load_json(input_path)
    texts = embeddings["texts"]
    chunks = embeddings["chunks"]
    centroids = build_centroids(texts)
    translator_centroids = build_translator_centroids(texts)
    coordinate_records = texts + centroids + translator_centroids
    add_coordinates(coordinate_records)

    viewer_data = {
        "model": embeddings["model"],
        "max_tokens": embeddings["max_tokens"],
        "overlap": embeddings["overlap"],
        "texts": [stripped_text_record(text) for text in texts],
        "chunks": [stripped_chunk_record(chunk) for chunk in chunks],
        "sect_centroids": [stripped_text_record(centroid) for centroid in centroids],
        "translator_centroids": [
            stripped_text_record(centroid) for centroid in translator_centroids
        ],
        "similarities": build_text_similarities(texts),
        "nearest_texts": build_nearest_texts(texts),
        "nearest_chunks": build_nearest_chunks(texts, chunks),
    }
    write_json(output_path, viewer_data)

    print(f"Texts: {len(texts)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Sect centroids: {len(centroids)}")
    print(f"Translator centroids: {len(translator_centroids)}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
