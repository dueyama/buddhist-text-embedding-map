#!/usr/bin/env python3
"""Print reproducibility and reviewer-response statistics for the paper."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

from make_paper_figures import OVERLAP_TEXT_IDS, chunk_knn_mixing
from make_viewer_data import build_centroids, build_translator_centroids


ROOT = Path(__file__).resolve().parents[2]
CORPUS_PATH = ROOT / "experiments" / "sect_sutra_map" / "data" / "processed" / "corpus_index.json"
EMBEDDINGS_PATH = ROOT / "experiments" / "sect_sutra_map" / "outputs" / "embeddings.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def pca_ratio(records: list[dict]) -> np.ndarray:
    matrix = np.array([record["embedding"] for record in records], dtype=np.float32)
    return PCA(n_components=2, random_state=0).fit(matrix).explained_variance_ratio_


def text_lookup(embeddings: dict) -> dict[str, dict]:
    return {text["id"]: text for text in embeddings["texts"]}


def chunk_labels(embeddings: dict, text_a: str, text_b: str) -> tuple[np.ndarray, list[str]]:
    selected = [chunk for chunk in embeddings["chunks"] if chunk["text_id"] in {text_a, text_b}]
    matrix = np.array([chunk["embedding"] for chunk in selected], dtype=np.float32)
    labels = [chunk["text_id"] for chunk in selected]
    return cosine_similarity(matrix), labels


def mixing_from_similarity(similarities: np.ndarray, labels: list[str], k: int) -> float:
    scores = []
    for index, label in enumerate(labels):
        candidates = [other for other in range(len(labels)) if other != index]
        nearest = sorted(candidates, key=lambda other: similarities[index, other], reverse=True)[:k]
        scores.append(sum(1 for other in nearest if labels[other] != label) / len(nearest))
    return float(np.mean(scores))


def shuffle_summary(embeddings: dict, text_a: str, text_b: str, k: int, n: int = 5000) -> dict:
    similarities, labels = chunk_labels(embeddings, text_a, text_b)
    observed = mixing_from_similarity(similarities, labels, k)
    rng = np.random.default_rng(0)
    values = []
    for _ in range(n):
        shuffled = labels.copy()
        rng.shuffle(shuffled)
        values.append(mixing_from_similarity(similarities, shuffled, k))
    array = np.array(values, dtype=float)
    return {
        "k": k,
        "observed": observed,
        "shuffle_mean": float(array.mean()),
        "shuffle_p2_5": float(np.percentile(array, 2.5)),
        "shuffle_p50": float(np.percentile(array, 50)),
        "shuffle_p97_5": float(np.percentile(array, 97.5)),
    }


def pair_rank(embeddings: dict, text_a: str, text_b: str, k: int) -> tuple[int, int]:
    rows = []
    for index, source in enumerate(OVERLAP_TEXT_IDS):
        for target in OVERLAP_TEXT_IDS[index + 1 :]:
            rows.append((chunk_knn_mixing(embeddings["chunks"], source, target, k), source, target))
    rows.sort(reverse=True)
    target_pair = {text_a, text_b}
    for rank, (_, source, target) in enumerate(rows, start=1):
        if {source, target} == target_pair:
            return rank, len(rows)
    raise ValueError("pair not found")


def main() -> None:
    corpus = load_json(CORPUS_PATH)["texts"]
    embeddings = load_json(EMBEDDINGS_PATH)
    lookup = text_lookup(embeddings)

    records = (
        embeddings["texts"]
        + build_centroids(embeddings["texts"])
        + build_translator_centroids(embeddings["texts"])
    )
    semantic_ratio = pca_ratio(records)

    print("PCA")
    print(f"semantic_map_pc1={semantic_ratio[0]:.4f}")
    print(f"semantic_map_pc2={semantic_ratio[1]:.4f}")
    print(f"semantic_map_total={semantic_ratio.sum():.4f}")

    print("\nCorpus table")
    print("id\ttitle\tsource\tchar_count\tchunk_count")
    for item in corpus:
        print(
            f"{item['id']}\t{item['title']}\t{item['source']}\t"
            f"{item['char_count']}\t{lookup[item['id']]['chunk_count']}"
        )

    text_a = "t0366_amida_sutra"
    text_b = "t0367_praise_pure_land"
    print("\nAmida top-k mixing sensitivity")
    print("k\tobserved\tpair_rank\tpairs\tshuffle_mean\tshuffle_95pct")
    for k in [1, 3, 5, 10]:
        summary = shuffle_summary(embeddings, text_a, text_b, k)
        rank, total = pair_rank(embeddings, text_a, text_b, k)
        print(
            f"{k}\t{summary['observed']:.4f}\t{rank}\t{total}\t"
            f"{summary['shuffle_mean']:.4f}\t"
            f"{summary['shuffle_p2_5']:.4f}-{summary['shuffle_p97_5']:.4f}"
        )


if __name__ == "__main__":
    main()
