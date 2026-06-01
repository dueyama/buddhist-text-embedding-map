#!/usr/bin/env python3
"""Analyze Shinran-side evidence for the two Amida Sutra translations.

The goal is not to prove a stemma.  This script separates three layers:

1. explicit citation labels,
2. translation-specific lexical markers, and
3. semantic chunk affinity already computed in the sect sutra map.

Raw downloaded pages and JSON outputs are intentionally ignored by git.
"""

from __future__ import annotations

import html
import json
import os
import re
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", str(Path(os.environ.get("TMPDIR", "/tmp")) / "okyou-matplotlib"))

import matplotlib.pyplot as plt
import numpy as np
import requests
from matplotlib import font_manager
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[1]
SECT_ROOT = PROJECT_ROOT / "experiments" / "sect_sutra_map"
SECT_OUTPUT = SECT_ROOT / "outputs" / "embeddings.json"
MANIFEST_PATH = ROOT / "manifest.json"
RAW_DIR = ROOT / "data" / "raw"
OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = PROJECT_ROOT / "docs" / "figures"
FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc"


VARIANTS = str.maketrans(
    {
        "仮": "假",
        "佛": "佛",
        "仏": "佛",
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
        "尽": "盡",
        "盡": "盡",
        "徳": "德",
        "德": "德",
        "実": "實",
        "實": "實",
        "証": "證",
        "證": "證",
        "発": "發",
        "發": "發",
        "転": "轉",
        "轉": "轉",
        "辺": "邊",
        "邊": "邊",
        "広": "廣",
        "廣": "廣",
    }
)


MARKERS = [
    {
        "family": "rajiv",
        "label": "舍利弗",
        "terms": ["舍利弗"],
        "weight": 1,
    },
    {
        "family": "rajiv",
        "label": "執持名號・一心不亂",
        "terms": ["執持名號", "一心不亂"],
        "weight": 2,
    },
    {
        "family": "rajiv",
        "label": "恒河沙",
        "terms": ["恒河沙"],
        "weight": 1,
    },
    {
        "family": "rajiv",
        "label": "諸佛所護念經",
        "terms": ["一切諸佛所護念經"],
        "weight": 2,
    },
    {
        "family": "xuanzang_title",
        "label": "稱讚淨土經",
        "terms": ["称讃浄土経"],
        "weight": 2,
    },
    {
        "family": "xuanzang_explicit",
        "label": "稱讚淨土經・玄奘",
        "terms": ["称讃浄土経", "玄奘"],
        "weight": 4,
    },
    {
        "family": "xuanzang",
        "label": "舍利子",
        "terms": ["舍利子"],
        "weight": 1,
    },
    {
        "family": "xuanzang",
        "label": "殑伽沙",
        "terms": ["殑伽沙"],
        "weight": 1,
    },
    {
        "family": "xuanzang",
        "label": "慈悲加祐・心不亂",
        "terms": ["慈悲加祐", "心不亂"],
        "weight": 2,
    },
    {
        "family": "xuanzang",
        "label": "攝受法門",
        "terms": ["攝受法門"],
        "weight": 2,
    },
    {
        "family": "xuanzang",
        "label": "百千倶胝舌讃嘆",
        "terms": ["百千倶胝", "舌", "無量", "聲", "功德", "盡"],
        "weight": 3,
    },
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def strip_html(source: str) -> str:
    source = re.sub(r"<script\b.*?</script>", "", source, flags=re.I | re.S)
    source = re.sub(r"<style\b.*?</style>", "", source, flags=re.I | re.S)
    source = re.sub(r"<br\s*/?>", "\n", source, flags=re.I)
    source = re.sub(r"<[^>]+>", " ", source)
    source = html.unescape(source)
    return re.sub(r"[ \t\r\f\v]+", " ", source)


def extract_figure_text(source: str, figure_id: str) -> str:
    match = re.search(
        rf'<figure[^>]+id="{re.escape(figure_id)}"[^>]*>(.*?)</figure>',
        source,
        flags=re.I | re.S,
    )
    if not match:
        return ""
    body = re.sub(r"<figcaption\b.*?</figcaption>", "", match.group(1), flags=re.I | re.S)
    lines = [line.strip() for line in strip_html(body).splitlines()]
    return "\n".join(line for line in lines if line)


def fetch_shinshuseiten(item: dict[str, Any], refresh: bool) -> str:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / f"{item['id']}.html"
    if raw_path.exists() and not refresh:
        source = raw_path.read_text(encoding="utf-8")
    else:
        response = requests.get(item["url"], timeout=30)
        response.raise_for_status()
        source = response.text
        raw_path.write_text(source, encoding="utf-8")

    main = extract_figure_text(source, "TEXT_MAIN")
    origin = extract_figure_text(source, "TEXT_ORIGIN")
    return "\n".join(part for part in [main, origin] if part)


def load_sources(refresh: bool) -> tuple[dict[str, str], dict[str, str]]:
    manifest = read_json(MANIFEST_PATH)
    targets = {
        item["id"]: (PROJECT_ROOT / item["path"]).read_text(encoding="utf-8")
        for item in manifest["target_translations"]
    }
    shinran: dict[str, str] = {}
    for item in manifest["shinran_sources"]:
        if item["source"] == "shinshuseiten":
            shinran[item["id"]] = fetch_shinshuseiten(item, refresh=refresh)
        else:
            shinran[item["id"]] = (PROJECT_ROOT / item["path"]).read_text(encoding="utf-8")
    return targets, shinran


def compact_cjk(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"&M\d+;", "", text)
    text = re.sub(r"P--\d+|#\d+", "", text)
    text = text.translate(VARIANTS)
    return "".join(re.findall(r"[一-龯々〆〇]", text))


def marker_hit(text: str, marker: dict[str, Any]) -> bool:
    normalized = compact_cjk(text)
    return all(compact_cjk(term) in normalized for term in marker["terms"])


def marker_summary(shinran_sources: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for source_id, text in shinran_sources.items():
        hits = [marker for marker in MARKERS if marker_hit(text, marker)]
        weights = Counter()
        counts = Counter()
        for marker in hits:
            weights[marker["family"]] += marker["weight"]
            counts[marker["family"]] += 1
        rows.append(
            {
                "source_id": source_id,
                "hits": [{"family": marker["family"], "label": marker["label"]} for marker in hits],
                "counts": dict(counts),
                "weights": dict(weights),
            }
        )
    return rows


def exact_matches(targets: dict[str, str], shinran_sources: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    normalized_targets = {key: compact_cjk(value) for key, value in targets.items()}
    normalized_sources = {key: compact_cjk(value) for key, value in shinran_sources.items()}
    for target_id, target_text in normalized_targets.items():
        for source_id, source_text in normalized_sources.items():
            matcher = SequenceMatcher(None, target_text, source_text, autojunk=False)
            blocks = []
            for block in matcher.get_matching_blocks():
                if block.size < 8:
                    continue
                value = target_text[block.a : block.a + block.size]
                if len(set(value)) < 4:
                    continue
                blocks.append(
                    {
                        "target_start": block.a,
                        "source_start": block.b,
                        "length": block.size,
                        "match": value[:32],
                    }
                )
            blocks.sort(key=lambda item: item["length"], reverse=True)
            rows.append(
                {
                    "target_id": target_id,
                    "source_id": source_id,
                    "top_matches": blocks[:8],
                    "longest": blocks[0]["length"] if blocks else 0,
                }
            )
    return rows


def embedding_summary() -> dict[str, Any]:
    embeddings = read_json(SECT_OUTPUT)
    texts = {text["id"]: text for text in embeddings["texts"]}
    chunks = embeddings["chunks"]
    chunk_groups = {
        text_id: [chunk for chunk in chunks if chunk["text_id"] == text_id]
        for text_id in ["kyogyoshinsho", "t0366_amida_sutra", "t0367_praise_pure_land"]
    }

    def cosine(a: list[float], b: list[float]) -> float:
        left = np.array(a, dtype=np.float32).reshape(1, -1)
        right = np.array(b, dtype=np.float32).reshape(1, -1)
        return float(cosine_similarity(left, right)[0, 0])

    text_level = {
        "kyogyoshinsho_to_t0366": cosine(
            texts["kyogyoshinsho"]["embedding"], texts["t0366_amida_sutra"]["embedding"]
        ),
        "kyogyoshinsho_to_t0367": cosine(
            texts["kyogyoshinsho"]["embedding"], texts["t0367_praise_pure_land"]["embedding"]
        ),
    }

    kg_matrix = np.array([chunk["embedding"] for chunk in chunk_groups["kyogyoshinsho"]], dtype=np.float32)
    rows = []
    target_maxima = {}
    for target_id in ["t0366_amida_sutra", "t0367_praise_pure_land"]:
        target_matrix = np.array([chunk["embedding"] for chunk in chunk_groups[target_id]], dtype=np.float32)
        sims = cosine_similarity(kg_matrix, target_matrix)
        maxima = sims.max(axis=1)
        target_maxima[target_id] = maxima
        for index, score in enumerate(maxima):
            best_target = int(sims[index].argmax())
            rows.append(
                {
                    "target_id": target_id,
                    "kyogyoshinsho_chunk": chunk_groups["kyogyoshinsho"][index]["chunk_id"],
                    "target_chunk": chunk_groups[target_id][best_target]["chunk_id"],
                    "score": float(score),
                }
            )
    rows.sort(key=lambda item: item["score"], reverse=True)

    deltas = []
    for index, (rajiv_score, xuanzang_score) in enumerate(
        zip(target_maxima["t0366_amida_sutra"], target_maxima["t0367_praise_pure_land"])
    ):
        deltas.append(
            {
                "chunk_index": index,
                "chunk_id": chunk_groups["kyogyoshinsho"][index]["chunk_id"],
                "t0366": float(rajiv_score),
                "t0367": float(xuanzang_score),
                "delta_t0367_minus_t0366": float(xuanzang_score - rajiv_score),
            }
        )

    return {
        "text_level": text_level,
        "top_chunk_affinities": rows[:12],
        "chunk_deltas": deltas,
    }


def setup_font() -> font_manager.FontProperties:
    font = font_manager.FontProperties(fname=FONT_PATH)
    plt.rcParams["font.family"] = font.get_name()
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 160
    return font


def figure_marker_summary(rows: list[dict[str, Any]], font: font_manager.FontProperties) -> Path:
    labels = {
        "kyogyoshinsho": "教行信証",
        "nyushutsu_nimonge_p543": "入出二門偈 p543",
    }
    categories = [
        ("rajiv", "羅什訳固有語"),
        ("xuanzang", "玄奘訳固有語"),
        ("xuanzang_title", "称讃浄土経名"),
        ("xuanzang_explicit", "玄奘訳明示"),
    ]
    x = np.arange(len(rows))
    width = 0.18
    colors = ["#2563eb", "#dc2626", "#f97316", "#111827"]

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    for offset, ((key, label), color) in enumerate(zip(categories, colors)):
        values = [row["weights"].get(key, 0) for row in rows]
        ax.bar(x + (offset - 1.5) * width, values, width, label=label, color=color)

    ax.set_title("親鸞テキスト側の阿弥陀経二訳ソース指標", fontproperties=font, fontsize=14, pad=10)
    ax.set_ylabel("指標スコア", fontproperties=font)
    ax.set_xticks(x)
    ax.set_xticklabels([labels.get(row["source_id"], row["source_id"]) for row in rows], fontproperties=font)
    ax.grid(axis="y", color="#e2e8f0", linewidth=0.7)
    ax.legend(prop=font, frameon=False, ncol=2, loc="upper left")

    out = FIGURE_DIR / "shinran-amida-source-markers.png"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def figure_kyogyoshinsho_chunk_affinity(summary: dict[str, Any], font: font_manager.FontProperties) -> Path:
    deltas = summary["chunk_deltas"]
    x = [row["chunk_index"] for row in deltas]
    t0366 = [row["t0366"] for row in deltas]
    t0367 = [row["t0367"] for row in deltas]

    fig, ax = plt.subplots(figsize=(9.5, 4.9))
    ax.plot(x, t0366, color="#2563eb", linewidth=1.1, alpha=0.8, label="羅什訳 阿弥陀経")
    ax.plot(x, t0367, color="#dc2626", linewidth=1.1, alpha=0.8, label="玄奘訳 称讃浄土経")
    ax.fill_between(x, t0366, t0367, where=np.array(t0367) >= np.array(t0366), color="#fecaca", alpha=0.35)
    ax.fill_between(x, t0366, t0367, where=np.array(t0367) < np.array(t0366), color="#bfdbfe", alpha=0.35)
    ax.set_title("教行信証チャンクから見た阿弥陀経二訳への近さ", fontproperties=font, fontsize=14, pad=10)
    ax.set_xlabel("教行信証 chunk index", fontproperties=font)
    ax.set_ylabel("各訳チャンクへの最大コサイン類似度", fontproperties=font)
    ax.grid(color="#e2e8f0", linewidth=0.7)
    ax.legend(prop=font, frameon=False, loc="upper right")

    out = FIGURE_DIR / "shinran-kyogyoshinsho-amida-chunk-affinity.png"
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    refresh = "--refresh" in sys.argv
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    targets, shinran_sources = load_sources(refresh=refresh)
    markers = marker_summary(shinran_sources)
    matches = exact_matches(targets, shinran_sources)
    embeddings = embedding_summary()
    font = setup_font()
    figures = [
        str(figure_marker_summary(markers, font).relative_to(PROJECT_ROOT)),
        str(figure_kyogyoshinsho_chunk_affinity(embeddings, font).relative_to(PROJECT_ROOT)),
    ]

    result = {
        "sources": {
            "target_ids": list(targets),
            "shinran_ids": list(shinran_sources),
        },
        "marker_summary": markers,
        "exact_matches": matches,
        "embedding_summary": embeddings,
        "figures": figures,
    }
    write_json(OUTPUT_DIR / "analysis_results.json", result)

    print("Marker summary")
    for row in markers:
        print(row["source_id"], row["weights"], [hit["label"] for hit in row["hits"]])
    print("Text-level embedding")
    for key, value in embeddings["text_level"].items():
        print(key, f"{value:.4f}")
    print("Top chunk affinities")
    for row in embeddings["top_chunk_affinities"][:8]:
        print(row["target_id"], row["kyogyoshinsho_chunk"], row["target_chunk"], f"{row['score']:.4f}")
    print("Figures")
    for path in figures:
        print(path)
    print(f"Wrote {(OUTPUT_DIR / 'analysis_results.json').relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
