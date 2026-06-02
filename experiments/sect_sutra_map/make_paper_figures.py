#!/usr/bin/env python3
"""Generate paper figures from the sect sutra map viewer data."""

from __future__ import annotations

import json
import os
import argparse
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/okyou-matplotlib")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

from make_viewer_data import build_centroids, build_translator_centroids


ROOT = Path(__file__).resolve().parents[2]
VIEWER_DATA = ROOT / "experiments" / "sect_sutra_map" / "outputs" / "viewer_data.json"
EMBEDDINGS_DATA = ROOT / "experiments" / "sect_sutra_map" / "outputs" / "embeddings.json"
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

SECT_LABELS_EN = {
    "浄土宗": "Jodo",
    "浄土真宗": "Jodo Shinshu",
    "時宗": "Ji",
    "天台宗": "Tendai",
    "日蓮宗": "Nichiren",
    "真言宗": "Shingon",
    "曹洞宗": "Soto",
    "臨済宗": "Rinzai",
    "黄檗宗": "Obaku",
    "華厳宗": "Kegon",
    "法相宗": "Hosso",
}

TRANSLATOR_LABELS_EN = {
    "不空": "Amoghavajra",
    "玄奘": "Xuanzang",
    "鳩摩羅什": "Kumarajiva",
}

TEXT_COLORS = {
    "t0360_larger_sukhavati": "#2563eb",
    "t0365_meditation_sutra": "#60a5fa",
    "t0366_amida_sutra": "#1d4ed8",
    "t0367_praise_pure_land": "#38bdf8",
    "kyogyoshinsho": "#0f766e",
    "t0262_lotus_sutra": "#7c3aed",
    "t0262_kannon_chapter": "#a855f7",
    "t0848_maha_vairocana": "#dc2626",
    "t0865_vajrasekhara": "#f97316",
    "t0243_rishu_kyo": "#facc15",
    "t0251_heart_sutra": "#64748b",
    "t0676_samdhinirmocana": "#0891b2",
    "t0235_diamond_sutra": "#16a34a",
    "t0475_vimalakirti": "#15803d",
    "t0279_flower_garland": "#ca8a04",
}

OVERVIEW_TEXT_IDS = [
    "t0360_larger_sukhavati",
    "t0365_meditation_sutra",
    "t0366_amida_sutra",
    "t0367_praise_pure_land",
    "kyogyoshinsho",
    "t0848_maha_vairocana",
    "t0865_vajrasekhara",
    "t0243_rishu_kyo",
    "t0676_samdhinirmocana",
    "t0235_diamond_sutra",
    "t0475_vimalakirti",
]

OVERLAP_TEXT_IDS = [
    "t0366_amida_sutra",
    "t0367_praise_pure_land",
    "t0360_larger_sukhavati",
    "t0365_meditation_sutra",
    "kyogyoshinsho",
    "t0848_maha_vairocana",
    "t0865_vajrasekhara",
    "t0243_rishu_kyo",
    "t0676_samdhinirmocana",
    "t0235_diamond_sutra",
    "t0475_vimalakirti",
]

HIGHLIGHT_PAIR_IDS = [
    ("t0366_amida_sutra", "t0367_praise_pure_land"),
    ("kyogyoshinsho", "t0360_larger_sukhavati"),
    ("kyogyoshinsho", "t0365_meditation_sutra"),
    ("kyogyoshinsho", "t0366_amida_sutra"),
    ("t0360_larger_sukhavati", "t0365_meditation_sutra"),
    ("t0865_vajrasekhara", "t0243_rishu_kyo"),
    ("t0235_diamond_sutra", "t0475_vimalakirti"),
    ("t0366_amida_sutra", "t0243_rishu_kyo"),
]

BRIDGE_PAIR_IDS = [
    ("t0366_amida_sutra", "t0367_praise_pure_land"),
    ("kyogyoshinsho", "t0360_larger_sukhavati"),
    ("kyogyoshinsho", "t0365_meditation_sutra"),
    ("kyogyoshinsho", "t0366_amida_sutra"),
    ("t0360_larger_sukhavati", "t0365_meditation_sutra"),
    ("t0865_vajrasekhara", "t0243_rishu_kyo"),
    ("t0235_diamond_sutra", "t0475_vimalakirti"),
    ("t0366_amida_sutra", "t0243_rishu_kyo"),
]

PAIR_SHORT_LABELS = {
    frozenset(("t0366_amida_sutra", "t0367_praise_pure_land")): "阿弥陀/稱讃",
    frozenset(("kyogyoshinsho", "t0360_larger_sukhavati")): "教行/無量寿",
    frozenset(("kyogyoshinsho", "t0365_meditation_sutra")): "教行/観無量寿",
    frozenset(("kyogyoshinsho", "t0366_amida_sutra")): "教行/阿弥陀",
    frozenset(("t0360_larger_sukhavati", "t0365_meditation_sutra")): "無量寿/観無量寿",
    frozenset(("t0865_vajrasekhara", "t0243_rishu_kyo")): "金剛頂/理趣",
    frozenset(("t0235_diamond_sutra", "t0475_vimalakirti")): "金剛/維摩",
    frozenset(("t0366_amida_sutra", "t0243_rishu_kyo")): "阿弥陀/理趣",
}

PAIR_SHORT_LABELS_EN = {
    frozenset(("t0366_amida_sutra", "t0367_praise_pure_land")): "Amitabha/Praise",
    frozenset(("kyogyoshinsho", "t0360_larger_sukhavati")): "KGS/Larger",
    frozenset(("kyogyoshinsho", "t0365_meditation_sutra")): "KGS/Contemplation",
    frozenset(("kyogyoshinsho", "t0366_amida_sutra")): "KGS/Amitabha",
    frozenset(("t0360_larger_sukhavati", "t0365_meditation_sutra")): "Larger/Contemplation",
    frozenset(("t0865_vajrasekhara", "t0243_rishu_kyo")): "Vajrasekhara/Rishukyo",
    frozenset(("t0235_diamond_sutra", "t0475_vimalakirti")): "Diamond/Vimalakirti",
    frozenset(("t0366_amida_sutra", "t0243_rishu_kyo")): "Amitabha/Rishukyo",
}

PAIR_LABEL_OFFSETS = {
    frozenset(("t0366_amida_sutra", "t0367_praise_pure_land")): (6, 8),
    frozenset(("kyogyoshinsho", "t0360_larger_sukhavati")): (6, -13),
    frozenset(("kyogyoshinsho", "t0365_meditation_sutra")): (8, 7),
    frozenset(("kyogyoshinsho", "t0366_amida_sutra")): (8, -18),
    frozenset(("t0360_larger_sukhavati", "t0365_meditation_sutra")): (-74, 7),
    frozenset(("t0865_vajrasekhara", "t0243_rishu_kyo")): (6, 7),
    frozenset(("t0235_diamond_sutra", "t0475_vimalakirti")): (-52, 7),
    frozenset(("t0366_amida_sutra", "t0243_rishu_kyo")): (6, 6),
}


def load_data() -> dict:
    with VIEWER_DATA.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_embeddings() -> dict:
    with EMBEDDINGS_DATA.open(encoding="utf-8") as handle:
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


def add_covariance_ellipse(ax, points: np.ndarray, color: str, linewidth: float = 1.5) -> None:
    if len(points) < 3:
        return
    covariance = np.cov(points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    eigenvalues = np.maximum(eigenvalues, 1e-9)
    order = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    width, height = 2 * np.sqrt(eigenvalues)
    center = points.mean(axis=0)
    ax.add_patch(
        Ellipse(
            xy=center,
            width=width,
            height=height,
            angle=angle,
            facecolor=color,
            edgecolor=color,
            alpha=0.12,
            linewidth=linewidth,
            zorder=2,
        )
    )


def chunks_for_texts(embeddings: dict, text_ids: list[str]) -> list[dict]:
    text_set = set(text_ids)
    return [chunk for chunk in embeddings["chunks"] if chunk["text_id"] in text_set]


def chunks_for_text(embeddings: dict, text_id: str) -> list[dict]:
    return [chunk for chunk in embeddings["chunks"] if chunk["text_id"] == text_id]


def text_embedding_lookup(embeddings: dict) -> dict[str, np.ndarray]:
    return {
        text["id"]: np.array(text["embedding"], dtype=np.float32)
        for text in embeddings["texts"]
        if text.get("embedding")
    }


def text_cosine(embeddings: dict, text_a: str, text_b: str) -> float:
    lookup = text_embedding_lookup(embeddings)
    vector_a = lookup[text_a].reshape(1, -1)
    vector_b = lookup[text_b].reshape(1, -1)
    return float(cosine_similarity(vector_a, vector_b)[0, 0])


def pca_coordinates(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pca = PCA(n_components=2, random_state=0)
    coords = pca.fit_transform(matrix)
    return coords, pca.explained_variance_ratio_


def semantic_pca_ratio(embeddings: dict) -> np.ndarray:
    records = (
        embeddings["texts"]
        + build_centroids(embeddings["texts"])
        + build_translator_centroids(embeddings["texts"])
    )
    matrix = np.array([record["embedding"] for record in records], dtype=np.float32)
    return PCA(n_components=2, random_state=0).fit(matrix).explained_variance_ratio_


def chunk_coordinates(chunks: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    matrix = np.array([chunk["embedding"] for chunk in chunks], dtype=np.float32)
    return pca_coordinates(matrix)


def axis_label(label: str, ratio: float) -> str:
    return f"{label} ({ratio * 100:.1f}%)"


def short_label(text_id: str, fallback: str = "", lang: str = "ja") -> str:
    labels = SHORT_LABELS_EN if lang == "en" else SHORT_LABELS
    return labels.get(text_id, fallback or text_id)


def sect_label(sect: str, lang: str = "ja") -> str:
    return SECT_LABELS_EN.get(sect, sect) if lang == "en" else sect


def translator_label(title: str, lang: str = "ja") -> str:
    return TRANSLATOR_LABELS_EN.get(title, title) if lang == "en" else title


def figure_path(filename: str, lang: str = "ja") -> Path:
    out_dir = FIGURE_DIR / "en" if lang == "en" else FIGURE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / filename


def figure_semantic_map(data: dict, embeddings: dict, font: font_manager.FontProperties, lang: str = "ja") -> Path:
    texts = data["texts"]
    translator_centroids = data.get("translator_centroids", [])
    pca_ratio = semantic_pca_ratio(embeddings)
    fig, ax = plt.subplots(figsize=(9.8, 7.2))

    for text in texts:
        sect = first_sect(text)
        color = SECT_COLORS.get(sect, "#64748b")
        ax.scatter(text["x"], text["y"], s=68, color=color, edgecolor="white", linewidth=0.8, zorder=3)
        ax.text(
            text["x"] + 0.007,
            text["y"] + 0.007,
            short_label(text["id"], text["title"], lang),
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
            translator_label(centroid["title"], lang),
            fontsize=10,
            fontproperties=font,
            fontweight="bold",
            color="#111827",
            zorder=6,
        )

    ax.axhline(0, color="#cbd5e1", linewidth=0.8, zorder=1)
    ax.axvline(0, color="#cbd5e1", linewidth=0.8, zorder=1)
    title = "Semantic Placement of Sectarian Reference Texts" if lang == "en" else "宗派別参照テキスト群の意味配置"
    pc1 = "PCA axis 1" if lang == "en" else "PCA 第1軸"
    pc2 = "PCA axis 2" if lang == "en" else "PCA 第2軸"
    ax.set_title(title, fontproperties=font, fontsize=15, pad=12)
    ax.set_xlabel(axis_label(pc1, pca_ratio[0]), fontproperties=font)
    ax.set_ylabel(axis_label(pc2, pca_ratio[1]), fontproperties=font)
    ax.grid(color="#e2e8f0", linewidth=0.7)

    legend_handles = []
    legend_labels = []
    for sect, color in SECT_COLORS.items():
        if any(sect in text.get("sects", []) for text in texts):
            legend_handles.append(plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=7))
            legend_labels.append(sect_label(sect, lang))
    legend_handles.append(plt.Line2D([0], [0], marker="D", color="w", markerfacecolor="#111827", markersize=7))
    legend_labels.append("translator centroid" if lang == "en" else "訳者重心")
    ax.legend(
        legend_handles,
        legend_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=6,
        fontsize=8,
        prop=font,
        frameon=False,
        columnspacing=1.3,
        handletextpad=0.4,
    )

    out = figure_path("sect-sutra-semantic-map.png", lang)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_chunk_distribution_overview(embeddings: dict, font: font_manager.FontProperties, lang: str = "ja") -> Path:
    chunks = chunks_for_texts(embeddings, OVERVIEW_TEXT_IDS)
    coords, pca_ratio = chunk_coordinates(chunks)
    text_lookup = {text["id"]: text for text in embeddings["texts"]}

    fig, ax = plt.subplots(figsize=(9.8, 7.2))
    for text_id in OVERVIEW_TEXT_IDS:
        indices = [index for index, chunk in enumerate(chunks) if chunk["text_id"] == text_id]
        if not indices:
            continue
        points = coords[indices]
        color = TEXT_COLORS.get(text_id, "#64748b")
        ax.scatter(points[:, 0], points[:, 1], s=13, color=color, alpha=0.32, linewidth=0, zorder=3)
        add_covariance_ellipse(ax, points, color)
        center = points.mean(axis=0)
        ax.scatter(center[0], center[1], s=65, color=color, edgecolor="white", linewidth=0.8, zorder=5)
        ax.text(
            center[0] + 0.14,
            center[1] + 0.14,
            short_label(text_id, text_lookup[text_id]["title"], lang),
            fontsize=8.3,
            fontproperties=font,
            color="#0f172a",
            zorder=6,
        )

    ax.axhline(0, color="#cbd5e1", linewidth=0.8, zorder=1)
    ax.axvline(0, color="#cbd5e1", linewidth=0.8, zorder=1)
    ax.grid(color="#e2e8f0", linewidth=0.7)
    title = "Chunk Distributions and 1-Sigma Ellipses" if lang == "en" else "主要テキストのチャンク分布と1σ楕円"
    pc1 = "chunk PCA axis 1" if lang == "en" else "チャンク PCA 第1軸"
    pc2 = "chunk PCA axis 2" if lang == "en" else "チャンク PCA 第2軸"
    ax.set_title(title, fontproperties=font, fontsize=15, pad=12)
    ax.set_xlabel(axis_label(pc1, pca_ratio[0]), fontproperties=font)
    ax.set_ylabel(axis_label(pc2, pca_ratio[1]), fontproperties=font)

    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=TEXT_COLORS[text_id], markersize=6)
        for text_id in OVERVIEW_TEXT_IDS
    ]
    labels = [short_label(text_id, lang=lang) for text_id in OVERVIEW_TEXT_IDS]
    ax.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=6,
        fontsize=8,
        prop=font,
        frameon=False,
        columnspacing=1.2,
        handletextpad=0.4,
    )

    out = figure_path("sect-sutra-chunk-distribution-overview.png", lang)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_chunk_distribution_focus(embeddings: dict, font: font_manager.FontProperties, lang: str = "ja") -> Path:
    if lang == "en":
        panels = [
            ("Two Amitabha translations", ["t0366_amida_sutra", "t0367_praise_pure_land"]),
            ("Shingon esoteric texts", ["t0848_maha_vairocana", "t0865_vajrasekhara", "t0243_rishu_kyo"]),
            ("Prajna / Hosso / Zen controls", ["t0676_samdhinirmocana", "t0235_diamond_sutra", "t0475_vimalakirti"]),
        ]
    else:
        panels = [
            ("阿弥陀経二訳", ["t0366_amida_sutra", "t0367_praise_pure_land"]),
            ("真言系密教経典", ["t0848_maha_vairocana", "t0865_vajrasekhara", "t0243_rishu_kyo"]),
            ("般若・法相・禅系対照", ["t0676_samdhinirmocana", "t0235_diamond_sutra", "t0475_vimalakirti"]),
        ]

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.4))
    for ax, (title, text_ids) in zip(axes, panels):
        chunks = chunks_for_texts(embeddings, text_ids)
        coords, pca_ratio = chunk_coordinates(chunks)
        for text_id in text_ids:
            indices = [index for index, chunk in enumerate(chunks) if chunk["text_id"] == text_id]
            points = coords[indices]
            color = TEXT_COLORS[text_id]
            ax.scatter(points[:, 0], points[:, 1], s=14, color=color, alpha=0.38, linewidth=0, zorder=3)
            add_covariance_ellipse(ax, points, color)
            center = points.mean(axis=0)
            ax.scatter(center[0], center[1], s=58, color=color, edgecolor="white", linewidth=0.8, zorder=5)
            ax.text(
                center[0] + 0.08,
                center[1] + 0.08,
                short_label(text_id, lang=lang),
                fontsize=8,
                fontproperties=font,
                color="#0f172a",
                zorder=6,
            )
        ax.set_title(
            f"{title}\nPC1+PC2={pca_ratio.sum() * 100:.1f}%",
            fontproperties=font,
            fontsize=10.5,
            pad=8,
        )
        ax.axhline(0, color="#cbd5e1", linewidth=0.7, zorder=1)
        ax.axvline(0, color="#cbd5e1", linewidth=0.7, zorder=1)
        ax.grid(color="#e2e8f0", linewidth=0.6)
        ax.tick_params(labelsize=7)

    title = "Chunk Distributions for Representative Pairs and Groups" if lang == "en" else "代表ペア・グループのチャンク分布"
    fig.suptitle(title, fontproperties=font, fontsize=15, y=1.02)
    out = figure_path("sect-sutra-chunk-distribution-focus.png", lang)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chunk_knn_mixing(chunks: list[dict], text_a: str, text_b: str, k: int = 5) -> float:
    selected = [chunk for chunk in chunks if chunk["text_id"] in {text_a, text_b}]
    if len(selected) <= 1:
        return 0.0
    matrix = np.array([chunk["embedding"] for chunk in selected], dtype=np.float32)
    similarities = cosine_similarity(matrix)
    labels = [chunk["text_id"] for chunk in selected]
    scores = []
    for index, label in enumerate(labels):
        candidates = [other for other in range(len(selected)) if other != index]
        nearest = sorted(candidates, key=lambda other: similarities[index, other], reverse=True)[:k]
        if nearest:
            scores.append(sum(1 for other in nearest if labels[other] != label) / len(nearest))
    return float(np.mean(scores)) if scores else 0.0


def figure_chunk_overlap_heatmap(embeddings: dict, font: font_manager.FontProperties, lang: str = "ja") -> Path:
    selected_ids = OVERLAP_TEXT_IDS
    chunks = embeddings["chunks"]
    n = len(selected_ids)
    matrix = np.zeros((n, n), dtype=float)
    for i, text_a in enumerate(selected_ids):
        for j, text_b in enumerate(selected_ids):
            if i == j:
                matrix[i, j] = np.nan
            elif i < j:
                score = chunk_knn_mixing(chunks, text_a, text_b)
                matrix[i, j] = score
                matrix[j, i] = score

    labels = [short_label(text_id, lang=lang) for text_id in selected_ids]
    fig, ax = plt.subplots(figsize=(8.8, 7.6))
    image = ax.imshow(matrix, cmap="YlOrRd", vmin=0, vmax=0.4)
    title = "Distributional Overlap by Chunk-Neighbor Mixing Rate" if lang == "en" else "チャンク近傍混合率による分布重なり"
    ax.set_title(title, fontproperties=font, fontsize=15, pad=12)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels, fontproperties=font, rotation=45, ha="right", fontsize=8.5)
    ax.set_yticklabels(labels, fontproperties=font, fontsize=8.5)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=7, color="#0f172a")

    cbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    cbar_label = "share of top-5 neighbors from the other text" if lang == "en" else "top-5に相手テキストのチャンクが入る割合"
    cbar.ax.set_ylabel(cbar_label, fontproperties=font)
    out = figure_path("sect-sutra-chunk-overlap-heatmap.png", lang)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def pair_label(text_a: str, text_b: str, lang: str = "ja") -> str:
    pair_key = frozenset((text_a, text_b))
    if lang == "en":
        return PAIR_SHORT_LABELS_EN.get(pair_key, f"{short_label(text_a, lang=lang)}/{short_label(text_b, lang=lang)}")
    return PAIR_SHORT_LABELS.get(pair_key, f"{SHORT_LABELS[text_a]}/{SHORT_LABELS[text_b]}")


def figure_overlap_vs_centroid(embeddings: dict, font: font_manager.FontProperties, lang: str = "ja") -> Path:
    chunks = embeddings["chunks"]
    highlighted = {frozenset(pair) for pair in HIGHLIGHT_PAIR_IDS}
    rows = []
    for i, text_a in enumerate(OVERLAP_TEXT_IDS):
        for text_b in OVERLAP_TEXT_IDS[i + 1 :]:
            rows.append(
                {
                    "text_a": text_a,
                    "text_b": text_b,
                    "centroid": text_cosine(embeddings, text_a, text_b),
                    "mixing": chunk_knn_mixing(chunks, text_a, text_b),
                    "highlight": frozenset((text_a, text_b)) in highlighted,
                }
            )

    fig, ax = plt.subplots(figsize=(8.5, 6.2))
    background = [row for row in rows if not row["highlight"]]
    ax.scatter(
        [row["centroid"] for row in background],
        [row["mixing"] for row in background],
        s=34,
        color="#94a3b8",
        alpha=0.46,
        edgecolor="white",
        linewidth=0.5,
        label="other pairs" if lang == "en" else "その他のペア",
        zorder=2,
    )

    palette = ["#2563eb", "#0891b2", "#0f766e", "#60a5fa", "#7c3aed", "#f97316", "#16a34a", "#64748b"]
    for color, (text_a, text_b) in zip(palette, HIGHLIGHT_PAIR_IDS):
        row = next(item for item in rows if {item["text_a"], item["text_b"]} == {text_a, text_b})
        pair_key = frozenset((text_a, text_b))
        ax.scatter(
            row["centroid"],
            row["mixing"],
            s=78,
            color=color,
            edgecolor="white",
            linewidth=0.8,
            zorder=4,
        )
        ax.annotate(
            pair_label(text_a, text_b, lang),
            xy=(row["centroid"], row["mixing"]),
            xytext=PAIR_LABEL_OFFSETS.get(pair_key, (5, 5)),
            textcoords="offset points",
            fontsize=7.6,
            fontproperties=font,
            color="#0f172a",
            zorder=5,
        )

    title = "Text-Mean Similarity vs. Chunk-Distribution Overlap" if lang == "en" else "平均類似度とチャンク分布重なりの関係"
    xlabel = "cosine similarity of text-mean vectors" if lang == "en" else "本文平均ベクトルのコサイン類似度"
    ylabel = "chunk-neighbor mixing rate" if lang == "en" else "チャンク近傍混合率"
    ax.set_title(title, fontproperties=font, fontsize=15, pad=12)
    ax.set_xlabel(xlabel, fontproperties=font)
    ax.set_ylabel(ylabel, fontproperties=font)
    ax.set_xlim(0.45, 0.93)
    ax.set_ylim(-0.01, 0.42)
    ax.grid(color="#e2e8f0", linewidth=0.7)
    ax.legend(loc="upper left", prop=font, frameon=False)

    out = figure_path("sect-sutra-overlap-vs-centroid.png", lang)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def best_bridge_chunk_pair(embeddings: dict, text_a: str, text_b: str) -> dict:
    chunks_a = chunks_for_text(embeddings, text_a)
    chunks_b = chunks_for_text(embeddings, text_b)
    matrix_a = np.array([chunk["embedding"] for chunk in chunks_a], dtype=np.float32)
    matrix_b = np.array([chunk["embedding"] for chunk in chunks_b], dtype=np.float32)
    similarities = cosine_similarity(matrix_a, matrix_b)
    row_index, col_index = np.unravel_index(np.argmax(similarities), similarities.shape)
    chunk_a = chunks_a[row_index]
    chunk_b = chunks_b[col_index]
    return {
        "text_a": text_a,
        "text_b": text_b,
        "chunk_a": chunk_a["chunk_id"],
        "chunk_b": chunk_b["chunk_id"],
        "chunk_index_a": chunk_a["chunk_index"],
        "chunk_index_b": chunk_b["chunk_index"],
        "bridge_similarity": float(similarities[row_index, col_index]),
        "text_similarity": text_cosine(embeddings, text_a, text_b),
        "mixing": chunk_knn_mixing(embeddings["chunks"], text_a, text_b),
    }


def bridge_pair_rows(embeddings: dict) -> list[dict]:
    return [best_bridge_chunk_pair(embeddings, text_a, text_b) for text_a, text_b in BRIDGE_PAIR_IDS]


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


def figure_similarity_heatmap(data: dict, font: font_manager.FontProperties, lang: str = "ja") -> Path:
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

    labels = [short_label(text_id, lang=lang) for text_id in selected_ids]
    fig, ax = plt.subplots(figsize=(8.5, 7.5))
    image = ax.imshow(matrix, cmap="YlGnBu", vmin=0.72, vmax=0.92)
    title = "Cosine Similarity among Major Texts" if lang == "en" else "主要テキスト間のコサイン類似度"
    ax.set_title(title, fontproperties=font, fontsize=15, pad=12)
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
    cbar.ax.set_ylabel("cosine similarity" if lang == "en" else "コサイン類似度", fontproperties=font)
    out = figure_path("sect-sutra-similarity-heatmap.png", lang)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_amida_comparison(font: font_manager.FontProperties, lang: str = "ja") -> Path:
    labels = ["whole-text direct embedding", "mean best chunk match"] if lang == "en" else ["全文直接埋め込み", "チャンク最良一致平均"]
    tfidf = [0.1928, 0.1424]
    embedding = [0.8943, 0.7108]
    x = np.arange(len(labels))
    width = 0.34

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    tfidf_label = "character TF-IDF" if lang == "en" else "文字単位 TF-IDF"
    embedding_label = "semantic embedding" if lang == "en" else "意味埋め込み"
    ax.bar(x - width / 2, tfidf, width, label=tfidf_label, color="#94a3b8")
    ax.bar(x + width / 2, embedding, width, label=embedding_label, color="#2563eb")
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("similarity" if lang == "en" else "類似度", fontproperties=font)
    title = "Similarity of the Two Amitabha Sutra Translations" if lang == "en" else "阿弥陀経二訳の類似度比較"
    ax.set_title(title, fontproperties=font, fontsize=15, pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontproperties=font)
    ax.legend(prop=font, loc="upper right")
    ax.grid(axis="y", color="#e2e8f0")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", fontsize=8, padding=3)

    out = figure_path("amida-two-translation-comparison.png", lang)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["ja", "en"], default="ja")
    args = parser.parse_args()
    lang = args.lang
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    font = setup_style()
    data = load_data()
    embeddings = load_embeddings()
    outputs = [
        figure_semantic_map(data, embeddings, font, lang),
        figure_chunk_distribution_overview(embeddings, font, lang),
        figure_chunk_distribution_focus(embeddings, font, lang),
        figure_chunk_overlap_heatmap(embeddings, font, lang),
        figure_overlap_vs_centroid(embeddings, font, lang),
        figure_similarity_heatmap(data, font, lang),
        figure_amida_comparison(font, lang),
    ]
    for path in outputs:
        print(path)
    print("bridge_pair\tchunk_a\tchunk_b\tbridge_similarity\ttext_similarity\tmixing")
    for row in bridge_pair_rows(embeddings):
        print(
            f"{pair_label(row['text_a'], row['text_b'], lang)}\t"
            f"{row['chunk_a']}\t{row['chunk_b']}\t"
            f"{row['bridge_similarity']:.4f}\t"
            f"{row['text_similarity']:.4f}\t{row['mixing']:.4f}"
        )


if __name__ == "__main__":
    main()
