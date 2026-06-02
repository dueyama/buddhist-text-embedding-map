#!/usr/bin/env python3
"""Generate three-layer figures for Amida/Shinran source-mixture analysis."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/okyou-matplotlib")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from common import PROJECT_ROOT, token_chunks
from make_paper_figures import chunk_knn_mixing


ROOT = Path(__file__).resolve().parent
EMBEDDINGS_DATA = ROOT / "outputs" / "embeddings.json"
CORPUS_INDEX = ROOT / "data" / "processed" / "corpus_index.json"
FIGURE_DIR = PROJECT_ROOT / "docs" / "figures"
SUMMARY_PATH = ROOT / "outputs" / "three_layer_summary.json"
FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc"

TARGET_ID = "kyogyoshinsho"
SOURCE_IDS = [
    "t0360_larger_sukhavati",
    "t0365_meditation_sutra",
    "t0366_amida_sutra",
    "t0367_praise_pure_land",
]

SOURCE_LABELS = {
    "t0360_larger_sukhavati": "無量寿経",
    "t0365_meditation_sutra": "観無量寿経",
    "t0366_amida_sutra": "羅什訳阿弥陀経",
    "t0367_praise_pure_land": "玄奘訳称讃浄土経",
    "unmarked": "未検出",
}

SOURCE_COLORS = {
    "t0360_larger_sukhavati": "#2563eb",
    "t0365_meditation_sutra": "#60a5fa",
    "t0366_amida_sutra": "#0f766e",
    "t0367_praise_pure_land": "#dc2626",
    "unmarked": "#cbd5e1",
}

VARIANTS = str.maketrans(
    {
        "仏": "佛",
        "佛": "佛",
        "国": "國",
        "國": "國",
        "寿": "壽",
        "壽": "壽",
        "経": "經",
        "經": "經",
        "浄": "淨",
        "淨": "淨",
        "讃": "讚",
        "讚": "讚",
        "称": "稱",
        "稱": "稱",
        "摂": "攝",
        "攝": "攝",
        "声": "聲",
        "聲": "聲",
        "徳": "德",
        "德": "德",
        "実": "實",
        "實": "實",
        "証": "證",
        "證": "證",
        "発": "發",
        "發": "發",
        "辺": "邊",
        "邊": "邊",
        "広": "廣",
        "廣": "廣",
    }
)

REFERENCE_MARKERS = {
    "t0360_larger_sukhavati": [
        "無量壽",
        "法藏",
        "本願",
        "四十八願",
        "願生",
        "安樂",
        "正覺",
    ],
    "t0365_meditation_sutra": [
        "觀無量壽",
        "韋提希",
        "頻婆娑羅",
        "十六觀",
        "日想觀",
        "水想觀",
        "九品",
    ],
    "t0366_amida_sutra": [
        "阿彌陀經",
        "阿彌陀",
        "舍利弗",
        "執持名號",
        "一心不亂",
        "恒河沙",
        "極樂",
    ],
    "t0367_praise_pure_land": [
        "稱讚淨土",
        "稱讚淨土經",
        "玄奘",
        "舍利子",
        "殑伽沙",
        "慈悲加祐",
        "攝受法門",
        "百千倶胝",
    ],
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def setup_font() -> font_manager.FontProperties:
    font = font_manager.FontProperties(fname=FONT_PATH)
    plt.rcParams["font.family"] = font.get_name()
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 160
    return font


def normalize_cjk(text: str) -> str:
    text = text.translate(VARIANTS)
    return "".join(re.findall(r"[一-龯々〆〇A-Za-z0-9]+", text))


def load_bodies() -> dict[str, str]:
    corpus = read_json(CORPUS_INDEX)
    bodies: dict[str, str] = {}
    for text in corpus["texts"]:
        if text["id"] not in set(SOURCE_IDS + [TARGET_ID]):
            continue
        bodies[text["id"]] = (PROJECT_ROOT / text["body_path"]).read_text(encoding="utf-8")
    return bodies


def load_chunk_texts(max_tokens: int, overlap: int) -> dict[str, list[str]]:
    bodies = load_bodies()
    return {
        text_id: token_chunks(body, max_tokens=max_tokens, overlap=overlap)
        for text_id, body in bodies.items()
    }


def chunks_by_text(embeddings: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for chunk in embeddings["chunks"]:
        grouped.setdefault(chunk["text_id"], []).append(chunk)
    return grouped


def text_vectors(embeddings: dict[str, Any]) -> dict[str, np.ndarray]:
    return {
        text["id"]: np.array(text["embedding"], dtype=np.float32)
        for text in embeddings["texts"]
    }


def text_cosine(embeddings: dict[str, Any], text_a: str, text_b: str) -> float:
    vectors = text_vectors(embeddings)
    return float(cosine_similarity(vectors[text_a].reshape(1, -1), vectors[text_b].reshape(1, -1))[0, 0])


def semantic_source_scores(embeddings: dict[str, Any]) -> np.ndarray:
    grouped = chunks_by_text(embeddings)
    target = np.array([chunk["embedding"] for chunk in grouped[TARGET_ID]], dtype=np.float32)
    columns = []
    for source_id in SOURCE_IDS:
        source = np.array([chunk["embedding"] for chunk in grouped[source_id]], dtype=np.float32)
        columns.append(cosine_similarity(target, source).max(axis=1))
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
    full_tfidf = float(cosine_similarity(full_matrix[0], full_matrix[1])[0, 0])
    return np.column_stack(columns), full_tfidf


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
    return np.array(rows, dtype=np.float32)


def softmax_weights(scores: np.ndarray, temperature: float = 0.04) -> np.ndarray:
    centered = scores - scores.max(axis=1, keepdims=True)
    weights = np.exp(centered / temperature)
    denom = weights.sum(axis=1, keepdims=True)
    return np.divide(weights, denom, out=np.zeros_like(weights), where=denom != 0)


def normalize_citation_weights(scores: np.ndarray) -> np.ndarray:
    totals = scores.sum(axis=1, keepdims=True)
    weights = np.divide(scores, totals, out=np.zeros_like(scores), where=totals != 0)
    unmarked = (totals[:, 0] == 0).astype(np.float32).reshape(-1, 1)
    return np.column_stack([weights, unmarked])


def smooth(weights: np.ndarray, window: int = 7) -> np.ndarray:
    if window <= 1:
        return weights
    kernel = np.ones(window) / window
    padded = np.pad(weights, ((window // 2, window // 2), (0, 0)), mode="edge")
    smoothed = np.column_stack(
        [np.convolve(padded[:, column], kernel, mode="valid") for column in range(weights.shape[1])]
    )
    totals = smoothed.sum(axis=1, keepdims=True)
    return np.divide(smoothed, totals, out=np.zeros_like(smoothed), where=totals != 0)


def top5_mixing(embeddings: dict[str, Any]) -> float:
    return chunk_knn_mixing(
        embeddings["chunks"],
        "t0366_amida_sutra",
        "t0367_praise_pure_land",
        k=5,
    )


def figure_three_layer_concept(font: font_manager.FontProperties) -> Path:
    fig, ax = plt.subplots(figsize=(9.2, 4.7))
    ax.set_axis_off()
    boxes = [
        ("意味層 S", "埋め込み cosine\n主題・内容の近さ", "#dbeafe", "#2563eb", (0.06, 0.54)),
        ("文体層 T", "文字 n-gram TF-IDF\n訳語・表記の近さ", "#dcfce7", "#16a34a", (0.37, 0.54)),
        ("引用参照層 C", "経名・訳者名・固定句\n典拠経路の手がかり", "#fee2e2", "#dc2626", (0.68, 0.54)),
    ]
    for title, body, face, edge, (x, y) in boxes:
        patch = FancyBboxPatch(
            (x, y),
            0.25,
            0.25,
            boxstyle="round,pad=0.018,rounding_size=0.02",
            linewidth=1.6,
            edgecolor=edge,
            facecolor=face,
        )
        ax.add_patch(patch)
        ax.text(x + 0.125, y + 0.17, title, ha="center", va="center", fontsize=14, fontproperties=font, color=edge)
        ax.text(x + 0.125, y + 0.07, body, ha="center", va="center", fontsize=10, fontproperties=font, color="#0f172a")

    center = FancyBboxPatch(
        (0.27, 0.12),
        0.46,
        0.17,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.5,
        edgecolor="#334155",
        facecolor="#f8fafc",
    )
    ax.add_patch(center)
    ax.text(
        0.5,
        0.205,
        "三層 source-mixture map",
        ha="center",
        va="center",
        fontsize=14,
        fontproperties=font,
        color="#0f172a",
    )
    ax.text(
        0.5,
        0.145,
        "意味的に近いこと、文体的に近いこと、引用・学習経路として近いことのズレを読む",
        ha="center",
        va="center",
        fontsize=9.5,
        fontproperties=font,
        color="#475569",
    )
    for x in [0.185, 0.495, 0.805]:
        ax.add_patch(FancyArrowPatch((x, 0.53), (0.5, 0.31), arrowstyle="->", mutation_scale=13, color="#64748b"))
    ax.set_title("意味・文体・引用参照の三層地図", fontproperties=font, fontsize=16, pad=10)
    out = FIGURE_DIR / "three-layer-concept-map.png"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_amida_three_layer(metrics: dict[str, float], font: font_manager.FontProperties) -> Path:
    labels = ["意味 S\n本文平均", "文体 T\n文字n-gram", "分布 M\ntop-5混合"]
    values = [
        metrics["semantic_text_cosine"],
        metrics["lexical_tfidf_text_cosine"],
        metrics["semantic_chunk_mixing_top5"],
    ]
    colors = ["#2563eb", "#16a34a", "#f97316"]
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    bars = ax.bar(labels, values, color=colors, width=0.58)
    ax.set_ylim(0, 1)
    ax.set_ylabel("スコア", fontproperties=font)
    ax.set_title("阿弥陀経二訳の意味・文体・分布差分", fontproperties=font, fontsize=15, pad=12)
    ax.grid(axis="y", color="#e2e8f0", linewidth=0.7)
    for tick in ax.get_xticklabels():
        tick.set_fontproperties(font)
    ax.bar_label(bars, fmt="%.3f", fontsize=9, padding=4)
    ax.text(
        0.5,
        -0.22,
        "引用参照層 C は二訳本文内ではなく、親鸞文献側の経名・訳者名・固定句で評価する。",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=9,
        fontproperties=font,
        color="#475569",
    )
    out = FIGURE_DIR / "amida-three-layer-difference.png"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_source_mixture(
    semantic_weights: np.ndarray,
    lexical_weights: np.ndarray,
    citation_weights: np.ndarray,
    font: font_manager.FontProperties,
) -> Path:
    fig, axes = plt.subplots(3, 1, figsize=(10.2, 7.0), sharex=True)
    x = np.arange(semantic_weights.shape[0])
    layers = [
        ("意味層 S: embedding source-mixture", semantic_weights, SOURCE_IDS),
        ("文体層 T: 文字n-gram source-mixture", lexical_weights, SOURCE_IDS),
        ("引用参照層 C: 辞書マーカー source-mixture", citation_weights, SOURCE_IDS + ["unmarked"]),
    ]
    for ax, (title, weights, ids) in zip(axes, layers):
        ax.stackplot(
            x,
            [weights[:, index] for index in range(weights.shape[1])],
            colors=[SOURCE_COLORS[source_id] for source_id in ids],
            labels=[SOURCE_LABELS[source_id] for source_id in ids],
            alpha=0.88,
        )
        ax.set_ylim(0, 1)
        ax.set_ylabel("重み", fontproperties=font)
        ax.set_title(title, fontproperties=font, fontsize=11, loc="left", pad=6)
        ax.grid(axis="y", color="#e2e8f0", linewidth=0.6)
    axes[-1].set_xlabel("『教行信証』 chunk index", fontproperties=font)
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=5, frameon=False, prop=font, bbox_to_anchor=(0.5, 1.01))
    fig.suptitle("『教行信証』の三層 source-mixture map", fontproperties=font, fontsize=16, y=1.06)
    out = FIGURE_DIR / "kyogyoshinsho-three-layer-source-mixture.png"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def layer_means(weights: np.ndarray, ids: list[str]) -> dict[str, float]:
    return {
        SOURCE_LABELS[source_id]: round(float(weights[:, index].mean()), 4)
        for index, source_id in enumerate(ids)
    }


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    embeddings = read_json(EMBEDDINGS_DATA)
    max_tokens = int(embeddings.get("max_tokens", 700))
    overlap = int(embeddings.get("overlap", 100))
    chunk_texts = load_chunk_texts(max_tokens=max_tokens, overlap=overlap)

    semantic_scores = semantic_source_scores(embeddings)
    lexical_scores, amida_tfidf = lexical_source_scores(chunk_texts)
    citation_scores = citation_source_scores(chunk_texts)

    semantic_weights = smooth(softmax_weights(semantic_scores))
    lexical_weights = smooth(softmax_weights(lexical_scores, temperature=0.025))
    citation_weights = smooth(normalize_citation_weights(citation_scores), window=9)

    metrics = {
        "semantic_text_cosine": round(text_cosine(embeddings, "t0366_amida_sutra", "t0367_praise_pure_land"), 4),
        "lexical_tfidf_text_cosine": round(amida_tfidf, 4),
        "semantic_chunk_mixing_top5": round(top5_mixing(embeddings), 4),
    }

    font = setup_font()
    figures = [
        figure_three_layer_concept(font),
        figure_amida_three_layer(metrics, font),
        figure_source_mixture(semantic_weights, lexical_weights, citation_weights, font),
    ]
    summary = {
        "model": embeddings.get("model"),
        "target": TARGET_ID,
        "sources": SOURCE_IDS,
        "source_labels": SOURCE_LABELS,
        "amida_three_layer": metrics,
        "kyogyoshinsho_source_mixture": {
            "chunk_count": int(semantic_weights.shape[0]),
            "semantic_layer_mean_weights": layer_means(semantic_weights, SOURCE_IDS),
            "lexical_layer_mean_weights": layer_means(lexical_weights, SOURCE_IDS),
            "citation_layer_mean_weights": layer_means(citation_weights, SOURCE_IDS + ["unmarked"]),
        },
        "figures": [str(path.relative_to(PROJECT_ROOT)) for path in figures],
    }
    write_json(SUMMARY_PATH, summary)

    print("Amida three-layer metrics")
    for key, value in metrics.items():
        print(f"{key}\t{value:.4f}")
    print("Kyogyoshinsho layer mean weights")
    for layer_key, values in summary["kyogyoshinsho_source_mixture"].items():
        if isinstance(values, dict):
            print(layer_key, values)
    print("Figures")
    for path in figures:
        print(path.relative_to(PROJECT_ROOT))
    print(f"Wrote {SUMMARY_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
