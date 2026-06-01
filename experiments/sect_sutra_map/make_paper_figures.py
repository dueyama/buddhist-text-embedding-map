#!/usr/bin/env python3
"""Generate paper figures from the sect sutra map viewer data."""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/okyou-matplotlib")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


ROOT = Path(__file__).resolve().parents[2]
VIEWER_DATA = ROOT / "experiments" / "sect_sutra_map" / "outputs" / "viewer_data.json"
FIGURE_DIR = ROOT / "docs" / "figures"
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


def load_data() -> dict:
    with VIEWER_DATA.open(encoding="utf-8") as handle:
        return json.load(handle)


def setup_style() -> font_manager.FontProperties:
    font = font_manager.FontProperties(fname=FONT_PATH)
    plt.rcParams["font.family"] = font.get_name()
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 160
    return font


def first_sect(text: dict) -> str:
    sects = text.get("sects") or ["未分類"]
    return sects[0]


def figure_semantic_map(data: dict, font: font_manager.FontProperties) -> Path:
    texts = data["texts"]
    translator_centroids = data.get("translator_centroids", [])
    fig, ax = plt.subplots(figsize=(9.5, 6.5))

    for text in texts:
        sect = first_sect(text)
        color = SECT_COLORS.get(sect, "#64748b")
        ax.scatter(text["x"], text["y"], s=68, color=color, edgecolor="white", linewidth=0.8, zorder=3)
        ax.text(
            text["x"] + 0.007,
            text["y"] + 0.007,
            SHORT_LABELS.get(text["id"], text["title"]),
            fontsize=8.5,
            fontproperties=font,
            color="#0f172a",
            zorder=4,
        )

    for centroid in translator_centroids:
        ax.scatter(
            centroid["x"],
            centroid["y"],
            s=115,
            marker="D",
            color="#111827",
            edgecolor="white",
            linewidth=1,
            zorder=5,
        )
        ax.text(
            centroid["x"] + 0.009,
            centroid["y"] - 0.012,
            centroid["title"],
            fontsize=10,
            fontproperties=font,
            fontweight="bold",
            color="#111827",
            zorder=6,
        )

    ax.axhline(0, color="#cbd5e1", linewidth=0.8, zorder=1)
    ax.axvline(0, color="#cbd5e1", linewidth=0.8, zorder=1)
    ax.set_title("図1  意味埋め込みによる宗派別お経マップ", fontproperties=font, fontsize=15, pad=12)
    ax.set_xlabel("PCA 第1軸", fontproperties=font)
    ax.set_ylabel("PCA 第2軸", fontproperties=font)
    ax.grid(color="#e2e8f0", linewidth=0.7)

    legend_handles = []
    legend_labels = []
    for sect, color in SECT_COLORS.items():
        if any(sect in text.get("sects", []) for text in texts):
            legend_handles.append(plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=7))
            legend_labels.append(sect)
    legend_handles.append(plt.Line2D([0], [0], marker="D", color="w", markerfacecolor="#111827", markersize=7))
    legend_labels.append("訳者重心")
    ax.legend(legend_handles, legend_labels, loc="upper right", fontsize=8, prop=font, frameon=True)

    out = FIGURE_DIR / "sect-sutra-semantic-map.png"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def similarity_lookup(data: dict) -> dict[tuple[str, str], float]:
    lookup: dict[tuple[str, str], float] = {}
    similarities = data["similarities"]
    if isinstance(similarities, dict):
        labels = similarities["labels"]
        matrix = similarities["matrix"]
        for i, source in enumerate(labels):
            for j, target in enumerate(labels):
                lookup[(source, target)] = matrix[i][j]
        return lookup

    for row in similarities:
        lookup[(row["source_id"], row["target_id"])] = row["score"]
    return lookup


def figure_similarity_heatmap(data: dict, font: font_manager.FontProperties) -> Path:
    selected_ids = [
        "t0366_amida_sutra",
        "t0367_praise_pure_land",
        "t0360_larger_sukhavati",
        "t0365_meditation_sutra",
        "kyogyoshinsho",
        "t0848_maha_vairocana",
        "t0865_vajrasekhara",
        "t0243_rishu_kyo",
        "t0251_heart_sutra",
        "t0676_samdhinirmocana",
        "t0235_diamond_sutra",
        "t0475_vimalakirti",
    ]
    lookup = similarity_lookup(data)
    n = len(selected_ids)
    matrix = np.eye(n)
    for i, source in enumerate(selected_ids):
        for j, target in enumerate(selected_ids):
            if source == target:
                continue
            matrix[i, j] = lookup.get((source, target), lookup.get((target, source), np.nan))

    labels = [SHORT_LABELS[text_id] for text_id in selected_ids]
    fig, ax = plt.subplots(figsize=(8.5, 7.5))
    image = ax.imshow(matrix, cmap="YlGnBu", vmin=0.72, vmax=0.92)
    ax.set_title("図2  主要テキスト間のコサイン類似度", fontproperties=font, fontsize=15, pad=12)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels, fontproperties=font, rotation=45, ha="right", fontsize=8.5)
    ax.set_yticklabels(labels, fontproperties=font, fontsize=8.5)

    for i in range(n):
        for j in range(n):
            value = matrix[i, j]
            if i == j or np.isnan(value):
                continue
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=6.5, color="#0f172a")

    cbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.set_ylabel("コサイン類似度", fontproperties=font)
    out = FIGURE_DIR / "sect-sutra-similarity-heatmap.png"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_amida_comparison(font: font_manager.FontProperties) -> Path:
    labels = ["全文レベル", "チャンク最良一致平均"]
    tfidf = [0.1928, 0.1424]
    embedding = [0.8943, 0.7108]
    x = np.arange(len(labels))
    width = 0.34

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.bar(x - width / 2, tfidf, width, label="文字単位 TF-IDF", color="#94a3b8")
    ax.bar(x + width / 2, embedding, width, label="OpenAI 埋め込み", color="#2563eb")
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("類似度", fontproperties=font)
    ax.set_title("図3  阿弥陀経二訳の類似度比較", fontproperties=font, fontsize=15, pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontproperties=font)
    ax.legend(prop=font, loc="upper right")
    ax.grid(axis="y", color="#e2e8f0")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", fontsize=8, padding=3)

    out = FIGURE_DIR / "amida-two-translation-comparison.png"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    font = setup_style()
    data = load_data()
    outputs = [
        figure_semantic_map(data, font),
        figure_similarity_heatmap(data, font),
        figure_amida_comparison(font),
    ]
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
