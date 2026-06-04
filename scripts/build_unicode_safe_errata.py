#!/usr/bin/env python3
"""Build Japanese and English errata pages/PDFs for Unicode-safe chunking."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "experiments" / "sect_sutra_map" / "outputs" / "unicode_safe_chunking_comparison_text-embedding-3-large_700_100.json"
THREE_LAYER_SUMMARY_PATH = ROOT / "experiments" / "sect_sutra_map" / "outputs" / "unicode_safe_three_layer_comparison_text-embedding-3-large_700_100.json"
FIGURE_JA_PATH = ROOT / "docs" / "figures" / "unicode-safe-chunking-centroids.png"
FIGURE_EN_PATH = ROOT / "docs" / "figures" / "en" / "unicode-safe-chunking-centroids.png"
ERRATA_DIR = ROOT / "docs" / "errata"
ERRATA_EN_DIR = ERRATA_DIR / "en"
PDF_JA = ERRATA_DIR / "unicode-safe-chunking-errata-ja.pdf"
PDF_EN = ERRATA_EN_DIR / "unicode-safe-chunking-errata-en.pdf"
HTML_JA = ERRATA_DIR / "index.html"
HTML_EN = ERRATA_EN_DIR / "index.html"


def load_summary() -> dict[str, Any]:
    if not SUMMARY_PATH.exists():
        raise SystemExit(f"Missing comparison summary: {SUMMARY_PATH}")
    return json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))


def load_three_layer_summary() -> dict[str, Any]:
    if not THREE_LAYER_SUMMARY_PATH.exists():
        raise SystemExit(f"Missing three-layer comparison summary: {THREE_LAYER_SUMMARY_PATH}")
    return json.loads(THREE_LAYER_SUMMARY_PATH.read_text(encoding="utf-8"))


def fmt(value: float | int | None, digits: int = 6) -> str:
    if value is None:
        return ""
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.{digits}f}".rstrip("0").rstrip(".")


def percentile(values: list[int], q: float) -> float:
    if not values:
        raise ValueError("percentile requires at least one value")
    if len(values) == 1:
        return float(values[0])
    pos = (len(values) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(values) - 1)
    frac = pos - lo
    return values[lo] * (1 - frac) + values[hi] * frac


def full_window_char_summary(data: dict[str, Any]) -> dict[str, int]:
    max_tokens = data["method"]["max_tokens"]
    records = [
        record
        for record in data["chunk_records"]
        if record["strategy"] == "safe_unicode_700" and record["actual_token_count"] == max_tokens
    ]
    if not records:
        records = [record for record in data["chunk_records"] if record["strategy"] == "safe_unicode_700"]
    values = sorted(int(record["char_count"]) for record in records)
    return {
        "count": len(values),
        "median": round(percentile(values, 0.5)),
        "p10": round(percentile(values, 0.1)),
        "p90": round(percentile(values, 0.9)),
    }


def rows_for_strategy(data: dict[str, Any], lang: str) -> list[list[str]]:
    if lang == "ja":
        rows = [["方式", "チャンク数", "置換文字を含むチャンク", "置換文字数", "トークン数中央値", "トークン数平均"]]
        labels = [
            ("unsafe_token_decode", "旧方式"),
            ("safe_unicode_700", "改訂方式"),
        ]
    else:
        rows = [["method", "chunks", "chunks with replacement characters", "replacement characters", "median tokens", "mean tokens"]]
        labels = [
            ("unsafe_token_decode", "old method"),
            ("safe_unicode_700", "revised method"),
        ]
    for key, label in labels:
        stats = data["strategy_stats"][key]
        rows.append(
            [
                label,
                str(stats["chunk_count"]),
                str(stats["affected_chunks"]),
                str(stats["replacement_chars"]),
                fmt(stats["actual_token_count"]["median"], 3),
                fmt(stats["actual_token_count"]["mean"], 3),
            ]
        )
    return rows


def embedding_rows(data: dict[str, Any], lang: str) -> list[list[str]]:
    emb = data["embedding_comparison"]
    overall = emb["same_index_chunk_cosine_overall"]
    text = emb["text_centroid_old_safe_cosine_summary"]
    sect = emb["sect_centroid_old_safe_cosine_summary"]
    if lang == "ja":
        header = ["比較対象", "件数", "最小", "p10", "中央値", "平均", "p90", "最大"]
        labels = ["同一位置チャンク", "本文ごとの重心", "宗派ごとの重心"]
    else:
        header = ["comparison", "count", "min", "p10", "median", "mean", "p90", "max"]
        labels = ["same-position chunks", "text centroids", "sect centroids"]
    return [
        header,
        [labels[0], str(overall["count"]), fmt(overall["min"]), fmt(overall["p10"]), fmt(overall["median"]), fmt(overall["mean"]), fmt(overall["p90"]), fmt(overall["max"])],
        [labels[1], str(text["count"]), fmt(text["min"]), fmt(text["p10"]), fmt(text["median"]), fmt(text["mean"]), fmt(text["p90"]), fmt(text["max"])],
        [labels[2], str(sect["count"]), fmt(sect["min"]), fmt(sect["p10"]), fmt(sect["median"]), fmt(sect["mean"]), fmt(sect["p90"]), fmt(sect["max"])],
    ]


def text_centroid_rows(data: dict[str, Any], lang: str) -> list[list[str]]:
    cosines = data["embedding_comparison"]["text_centroid_old_safe_cosine"]
    sources = {source["id"]: source for source in data["sources"]}
    if lang == "ja":
        rows = [["本文", "ID", "旧方式/改訂方式の重心類似度"]]
    else:
        rows = [["text", "ID", "old/revised centroid cosine"]]
    for text_id, value in sorted(cosines.items(), key=lambda item: item[1]):
        source = sources.get(text_id, {})
        rows.append([source.get("title", text_id), text_id, fmt(value)])
    return rows


def three_layer_rows(data: dict[str, Any], lang: str) -> list[list[str]]:
    labels = {
        "semantic": ("意味層（参照源混合）", "semantic source-mixture layer"),
        "lexical": ("文体・語彙層", "style/lexical layer"),
        "citation": ("典拠マーカー層", "source-marker layer"),
    }
    if lang == "ja":
        rows = [["層", "チャンク", "重みcos中央値", "L1平均", "支配参照源の変化", "巻別支配参照源の変化"]]
    else:
        rows = [["layer", "chunks", "median weight cosine", "mean L1 distance", "dominant-source changes", "volume-dominant changes"]]
    for key in ["semantic", "lexical", "citation"]:
        item = data["layer_comparison"][key]
        volume = data["volume_dominance_comparison"][key]
        rows.append(
            [
                labels[key][0 if lang == "ja" else 1],
                str(item["chunk_count"]),
                fmt(item["row_cosine_summary"]["median"]),
                fmt(item["l1_distance_summary"]["mean"]),
                f"{item['dominant_source_changed_chunks']} / {item['chunk_count']}",
                f"{volume['dominant_changed_volumes']} / {volume['volume_count']}",
            ]
        )
    return rows


def marker_rows(data: dict[str, Any], lang: str) -> list[list[str]]:
    marker = data["citation_marker_summary"]
    if lang == "ja":
        rows = [["指標", "旧方式", "改訂方式"]]
        rows.append(["マーカー検出チャンク", str(marker["old"]["chunks_with_any_marker"]), str(marker["revised"]["chunks_with_any_marker"])])
        rows.append(["総マーカー検出数", str(marker["old"]["total_marker_hits"]), str(marker["revised"]["total_marker_hits"])])
        rows.append(["検出ベクトル完全一致率", fmt(marker["exact_marker_vector_match_rate"]), ""])
        rows.append(["検出ベクトルが変化したチャンク", str(marker["changed_marker_vectors"]), ""])
    else:
        rows = [["metric", "old method", "revised method"]]
        rows.append(["chunks with markers", str(marker["old"]["chunks_with_any_marker"]), str(marker["revised"]["chunks_with_any_marker"])])
        rows.append(["total marker hits", str(marker["old"]["total_marker_hits"]), str(marker["revised"]["total_marker_hits"])])
        rows.append(["exact marker-vector match rate", fmt(marker["exact_marker_vector_match_rate"]), ""])
        rows.append(["chunks with changed marker vector", str(marker["changed_marker_vectors"]), ""])
    return rows


def html_table(rows: list[list[str]]) -> str:
    return "<table>\n" + "\n".join(
        "<tr>" + "".join(
            f"<{'th' if i == 0 else 'td'}>{html.escape(cell)}</{'th' if i == 0 else 'td'}>"
            for cell in row
        ) + "</tr>"
        for i, row in enumerate(rows)
    ) + "\n</table>"


def write_html(data: dict[str, Any], three_data: dict[str, Any]) -> None:
    ERRATA_DIR.mkdir(parents=True, exist_ok=True)
    ERRATA_EN_DIR.mkdir(parents=True, exist_ok=True)
    window_chars = full_window_char_summary(data)
    ja = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Errata: Unicode文字境界を保つチャンク化</title>
  <style>
    body {{ margin: 0; color: #202723; background: #f6f7f2; font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", sans-serif; line-height: 1.75; }}
    main {{ width: min(920px, calc(100% - 40px)); margin: 0 auto; padding: 34px 0 52px; }}
    a {{ color: #2f6f73; text-underline-offset: 3px; }}
    h1 {{ margin: 0 0 8px; font-size: clamp(28px, 4vw, 42px); line-height: 1.18; }}
    h2 {{ margin-top: 30px; font-size: 22px; }}
    .meta, .note {{ color: #66706a; }}
    .notice {{ padding: 16px 18px; border-left: 5px solid #9a5b3f; background: #fff; border: 1px solid #d9ded6; border-radius: 8px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 14px 0 20px; background: #fff; }}
    th, td {{ border: 1px solid #d9ded6; padding: 8px 10px; text-align: left; font-size: 14px; }}
    th {{ background: #eef2ee; }}
    img {{ max-width: 100%; border: 1px solid #d9ded6; background: #fff; }}
  </style>
</head>
<body>
<main>
  <p><a href="../">トップへ戻る</a> / <a href="en/">English</a></p>
  <h1>Errata: Unicode文字境界を保つチャンク化の採用</h1>
  <p class="meta">v1.0.1 追補。2026年6月4日。</p>
  <p class="notice">v1.0.0 の広域的な意味地図を差し替えるものではない。ただし旧方式では、トークン列を一定の長さで切ってから文字列に戻していたため、一部のチャンク（本文断片）で文字の途中が切れ、置換文字 U+FFFD が本文に入ることがあった。以後は、文字の途中で切らないようにチャンク境界を調整する改訂方式を基準とする。</p>
  <h2>比較方法</h2>
  <p>本論で用いた宗派別参照群 15 本文 / 433 チャンクを対象に、700 トークン幅・100 トークン重なりという条件を保ったまま、旧方式と改訂方式を比較した。旧方式は、トークン列を固定幅で切った後、その断片をそのまま文字列へ戻す。改訂方式は、元の本文中の文字位置とトークン位置の対応を確認し、開始位置と終了位置を Unicode 文字の境界に合わせてから本文断片を作る。これにより、文字の一部だけを切り出してしまうことを避ける。</p>
  <p>U+FFFD が発生する理由は、tiktoken のトークンが Unicode 文字そのものではなく、UTF-8 バイト列を分割した単位であるためである。漢字などの1文字は複数バイトで表され、場合によっては複数トークンにまたがる。固定長のトークン断片だけを復号すると、断片の先頭または末尾が不完全な UTF-8 バイト列になり、復号時に置換文字 U+FFFD として現れることがある。</p>
  <p>本コーパスでは、700 トークンに達した改訂方式チャンク {window_chars["count"]} 件の文字数中央値は {window_chars["median"]} 字であり、p10-p90 は {window_chars["p10"]}-{window_chars["p90"]} 字であった。したがって、本稿の 700 トークン窓は、漢字を中心とする本文でおおむね 460 字前後に相当する。ここでの文字数は Python 文字列上の文字数であり、句読点や記号も含む。</p>
  <p>100 トークン重なりにより、境界付近の本文は隣接チャンクにも部分的に含まれる。そのため、境界差の影響は本文重心や巻単位の集計では平均化されやすく、今回の大局的安定性を支える要因の一つと考えられる。ただし、この重なりはチャンク単位の1位参照源判定の揺れを完全に抑えるものではない。</p>
  <p class="note">技術注: 実装では tiktoken の offsets を用いてトークン位置を Python 文字列の文字位置へ対応させた。旧方式の再現確認では、v1.0.0 と同じ固定長トークン列の復号を用いた。</p>
  <h2>文字列品質</h2>
  {html_table(rows_for_strategy(data, "ja"))}
  <h2>数値評価</h2>
  <p>埋め込みモデルは <code>{html.escape(data["method"]["model"])}</code>。旧方式の埋め込みは既存の埋め込みキャッシュを用い、改訂方式の本文断片だけを同じモデルで新規に埋め込んだ。公開成果物には、生本文やチャンク本文そのものは含めない。</p>
  {html_table(embedding_rows(data, "ja"))}
  <p>同じ本文ごとに旧方式と改訂方式の重心を比較すると、最小値でも {fmt(data["embedding_comparison"]["text_centroid_old_safe_cosine_summary"]["min"])} であり、全体として高い一致を示した。</p>
  {html_table(text_centroid_rows(data, "ja"))}
  <h2>三層別の確認</h2>
  <p>ここでいう意味層は、ターゲットチャンクと参照源チャンクの埋め込み cosine に基づく参照源混合である。したがって、意味層の入れ替わりは埋め込み空間全体の崩れではなく、埋め込みを用いた局所的な参照源順位が境界処理差に反応したものとして読む。</p>
  <p>三層参照源混合地図についても、旧方式と改訂方式を同じ条件で比較した。意味層の参照源混合では、チャンク単位の支配的参照源が {three_data["layer_comparison"]["semantic"]["dominant_source_changed_chunks"]} / {three_data["layer_comparison"]["semantic"]["chunk_count"]} で入れ替わった。一方、巻別の支配的参照源は変化せず、文体・語彙層の入れ替わりは {three_data["layer_comparison"]["lexical"]["dominant_source_changed_chunks"]} / {three_data["layer_comparison"]["lexical"]["chunk_count"]}、典拠マーカー層は {three_data["layer_comparison"]["citation"]["dominant_source_changed_chunks"]} / {three_data["layer_comparison"]["citation"]["chunk_count"]} であった。</p>
  {html_table(three_layer_rows(three_data, "ja"))}
  <p>典拠マーカー層では、マーカー検出チャンク数と総マーカー検出数も一致した。</p>
  {html_table(marker_rows(three_data, "ja"))}
  <figure>
    <img src="../figures/unicode-safe-chunking-centroids.png" alt="旧方式と改訂方式の本文重心">
    <figcaption>旧方式と改訂方式の本文重心。線は同じ本文の対応を示す。</figcaption>
  </figure>
  <h2>解釈</h2>
  <p>旧方式で発生した U+FFFD は、本文品質と再現性の問題として明確に避けるべきである。一方、同じ位置にあるチャンク同士の埋め込み類似度は平均 {fmt(data["embedding_comparison"]["same_index_chunk_cosine_overall"]["mean"])}、中央値 {fmt(data["embedding_comparison"]["same_index_chunk_cosine_overall"]["median"])} であり、本文ごとの重心と宗派ごとの重心も高い一致を示した。したがって、v1.0.0 の大局的な意味地図をただちに否定するものではない。</p>
  <p>ただし、意味層の参照源混合は、チャンク単位の1位参照源判定において Unicode 境界処理の差に一定の感度を示した。これは、参照源候補同士が近い局所箇所では入力ノイズにより順位が入れ替わり得ることを示す。一方で、100 トークン重なりは境界付近の差異を隣接チャンクへ部分的に分散させ、本文重心や巻単位の傾向を安定させる方向に働いたと考えられる。巻別の支配的参照源、文体・語彙層、典拠マーカー層は大きく崩れなかった。三層に分けることにより、どの層が揺れ、どの層が安定しているかを分離して確認できた点も、本稿の方法上の利点である。</p>
  <p>本文断片の表示、SAT 行範囲との対応、個別チャンク近傍、引用候補の精査では、旧方式を基準にしない。今後は、文字境界を保つ改訂方式を基準処理とする。</p>
  <p><a href="unicode-safe-chunking-errata-ja.pdf">日本語PDF</a> / <a href="en/unicode-safe-chunking-errata-en.pdf">English PDF</a></p>
</main>
</body>
</html>
"""
    en = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Errata and Supplement: Unicode-aware chunking</title>
  <style>
    body {{ margin: 0; color: #202723; background: #f6f7f2; font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", sans-serif; line-height: 1.7; }}
    main {{ width: min(920px, calc(100% - 40px)); margin: 0 auto; padding: 34px 0 52px; }}
    a {{ color: #2f6f73; text-underline-offset: 3px; }}
    h1 {{ margin: 0 0 8px; font-size: clamp(28px, 4vw, 42px); line-height: 1.18; }}
    h2 {{ margin-top: 30px; font-size: 22px; }}
    .meta, .note {{ color: #66706a; }}
    .notice {{ padding: 16px 18px; border-left: 5px solid #9a5b3f; background: #fff; border: 1px solid #d9ded6; border-radius: 8px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 14px 0 20px; background: #fff; }}
    th, td {{ border: 1px solid #d9ded6; padding: 8px 10px; text-align: left; font-size: 14px; }}
    th {{ background: #eef2ee; }}
    img {{ max-width: 100%; border: 1px solid #d9ded6; background: #fff; }}
  </style>
</head>
<body>
<main>
  <p><a href="../../en/">Back to top</a> / <a href="../">日本語</a></p>
  <h1>Errata and Supplement: adopting Unicode-aware chunking</h1>
  <p class="meta">v1.0.1 supplement. June 4, 2026.</p>
  <p class="notice">This erratum does not replace the broad semantic map in the v1.0.0 release. In the old method, the token stream was split into fixed-length windows and each window was converted back to text on its own. Some chunk boundaries therefore cut through a character representation, producing the replacement character U+FFFD in the chunk text. Future work adopts a revised method that adjusts chunk boundaries so they fall on Unicode character boundaries.</p>
  <h2>Method</h2>
  <p>The comparison uses the sect-sutra corpus used in the paper: 15 texts and 433 chunks. Both methods keep the same 700-token windows and 100-token overlap. The old method takes a fixed-width slice of the token sequence and converts that slice directly back into text. The revised method first relates token positions to character positions in the original Python string, then rounds each chunk start and end to Unicode character boundaries. This prevents a chunk from containing only part of a character representation.</p>
  <p>U+FFFD appears because tiktoken tokens are not Unicode characters themselves; they are units over UTF-8 byte sequences. A CJK character is represented by multiple bytes and can, in some cases, span multiple tokens. When a fixed-length token slice is decoded by itself, the start or end of the slice may contain an incomplete UTF-8 sequence, which is then emitted as the replacement character U+FFFD.</p>
  <p>In this corpus, the {window_chars["count"]} revised chunks that reach 700 tokens have a median length of {window_chars["median"]} characters, with a p10-p90 range of {window_chars["p10"]}-{window_chars["p90"]} characters. The 700-token window therefore corresponds roughly to about 460 CJK text characters in these classical Chinese-based materials. Character counts are Python string characters and include punctuation and symbols.</p>
  <p>The 100-token overlap means that text near a boundary is also partly present in adjacent chunks. Boundary-level differences are therefore more likely to be averaged out in text centroids and volume-level summaries, which is one plausible reason for the broad stability observed here. The overlap does not, however, eliminate all chunk-level first-place source changes.</p>
  <p class="note">Technical note: the implementation uses tiktoken offsets to map token positions to Python string positions. The old behavior was reproduced with the same fixed-token decoding used in v1.0.0.</p>
  <h2>String Quality</h2>
  {html_table(rows_for_strategy(data, "en"))}
  <h2>Quantitative Evaluation</h2>
  <p>The embedding model is <code>{html.escape(data["method"]["model"])}</code>. The old-method embeddings use the existing embedding cache. Only the revised chunks were newly embedded with the same model. Public outputs do not include raw text or chunk text.</p>
  {html_table(embedding_rows(data, "en"))}
  <p>At the text level, the old and revised centroids remain closely aligned. The lowest text-centroid cosine is {fmt(data["embedding_comparison"]["text_centroid_old_safe_cosine_summary"]["min"])}.</p>
  {html_table(text_centroid_rows(data, "en"))}
  <h2>Three-Layer Check</h2>
  <p>The semantic layer here is an embedding-based source mixture: it uses cosine similarity between target chunks and source chunks. The source changes in this layer should therefore be read as changes in local source rankings derived from embeddings, not as a collapse of the embedding space as a whole.</p>
  <p>The three-layer source-mixture map was also recomputed under the old and revised chunking methods. In the semantic source-mixture layer, the dominant source changes for {three_data["layer_comparison"]["semantic"]["dominant_source_changed_chunks"]} / {three_data["layer_comparison"]["semantic"]["chunk_count"]} chunks. However, the dominant source by volume does not change. In the style/lexical layer, the dominant source changes for {three_data["layer_comparison"]["lexical"]["dominant_source_changed_chunks"]} / {three_data["layer_comparison"]["lexical"]["chunk_count"]} chunks. In the source-marker layer, it changes for {three_data["layer_comparison"]["citation"]["dominant_source_changed_chunks"]} / {three_data["layer_comparison"]["citation"]["chunk_count"]} chunks.</p>
  {html_table(three_layer_rows(three_data, "en"))}
  <p>For the source-marker layer, the number of chunks with detected markers and the total number of marker hits are unchanged.</p>
  {html_table(marker_rows(three_data, "en"))}
  <figure>
    <img src="../../figures/en/unicode-safe-chunking-centroids.png" alt="Text centroids for the old and revised methods">
    <figcaption>Text centroids for the old and revised methods. Lines connect the same text.</figcaption>
  </figure>
  <h2>Interpretation</h2>
  <p>The U+FFFD issue in the old method is a real text-quality and reproducibility problem. At the same time, embedding cosine for chunks at the same position remains high: mean {fmt(data["embedding_comparison"]["same_index_chunk_cosine_overall"]["mean"])} and median {fmt(data["embedding_comparison"]["same_index_chunk_cosine_overall"]["median"])}. Text and sect centroids also remain closely aligned. The broad semantic map in v1.0.0 is therefore not immediately invalidated.</p>
  <p>The semantic source-mixture layer nevertheless shows measurable sensitivity in chunk-level first-place source assignments. This suggests that local source rankings can change under input noise when candidate sources are close. At the same time, the 100-token overlap plausibly spreads boundary-level differences into adjacent chunks and helps stabilize text centroids and volume-level tendencies. By contrast, volume-level dominant sources, the style/lexical layer, and the source-marker layer remain stable. This is also a methodological advantage of the three-layer design: it separates where the analysis is sensitive from where it is stable.</p>
  <p>Displaying chunk excerpts, SAT line-range correspondence, individual-neighbor inspection, and future citation-level analysis should not use the old method as the baseline. Future work should use the revised Unicode-aware method.</p>
  <p><a href="../unicode-safe-chunking-errata-ja.pdf">Japanese PDF</a> / <a href="unicode-safe-chunking-errata-en.pdf">English PDF</a></p>
</main>
</body>
</html>
"""
    HTML_JA.write_text(ja, encoding="utf-8")
    HTML_EN.write_text(en, encoding="utf-8")


def register_fonts() -> tuple[str, str]:
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
    return "HeiseiMin-W3", "HeiseiKakuGo-W5"


def pdf_styles(lang: str) -> dict[str, ParagraphStyle]:
    min_font, gothic = register_fonts()
    base_font = min_font if lang == "ja" else "Helvetica"
    bold_font = gothic if lang == "ja" else "Helvetica-Bold"
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=styles["Title"],
            fontName=bold_font,
            fontSize=18,
            leading=24,
            alignment=TA_LEFT,
            spaceAfter=8,
            wordWrap="CJK" if lang == "ja" else None,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=styles["Heading2"],
            fontName=bold_font,
            fontSize=13,
            leading=17,
            spaceBefore=10,
            spaceAfter=5,
            wordWrap="CJK" if lang == "ja" else None,
        ),
        "body": ParagraphStyle(
            "body",
            parent=styles["BodyText"],
            fontName=base_font,
            fontSize=9.3,
            leading=14.2,
            spaceAfter=5,
            wordWrap="CJK" if lang == "ja" else None,
        ),
        "small": ParagraphStyle(
            "small",
            parent=styles["BodyText"],
            fontName=base_font,
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#66706a"),
            wordWrap="CJK" if lang == "ja" else None,
        ),
    }


def pdf_table(rows: list[list[str]], lang: str) -> Table:
    body_font = "HeiseiMin-W3"
    header_font = "HeiseiKakuGo-W5"
    table = Table(rows, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), header_font),
                ("FONTNAME", (0, 1), (-1, -1), body_font),
                ("FONTSIZE", (0, 0), (-1, -1), 7.2),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2ee")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d9ded6")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def write_pdf(data: dict[str, Any], three_data: dict[str, Any], lang: str) -> None:
    path = PDF_JA if lang == "ja" else PDF_EN
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Unicode-aware chunking errata and supplement",
        author="Daishin Ueyama",
    )
    st = pdf_styles(lang)
    window_chars = full_window_char_summary(data)
    story: list[Any] = []
    if lang == "ja":
        story.extend(
            [
                Paragraph("Errata: Unicode文字境界を保つチャンク化の採用", st["title"]),
                Paragraph("v1.0.1 追補。2026年6月4日。", st["small"]),
                Paragraph("要点", st["h2"]),
                Paragraph("v1.0.0 の広域的な意味地図を差し替えるものではない。ただし旧方式では、トークン列を一定の長さで切ってから文字列に戻していたため、一部のチャンクで文字の途中が切れ、置換文字 U+FFFD が本文に入ることがあった。本補遺では、同じ 700 トークン幅・100 トークン重なりを保ちつつ、文字の途中で切らないように境界を調整する改訂方式を検証した。", st["body"]),
                Paragraph("U+FFFD が発生する理由は、tiktoken のトークンが Unicode 文字そのものではなく、UTF-8 バイト列を分割した単位であるためである。漢字などの1文字は複数バイトで表され、場合によっては複数トークンにまたがる。固定長のトークン断片だけを復号すると、断片の先頭または末尾が不完全な UTF-8 バイト列になり、復号時に置換文字 U+FFFD として現れることがある。", st["body"]),
                Paragraph(f"本コーパスでは、700 トークンに達した改訂方式チャンク {window_chars['count']} 件の文字数中央値は {window_chars['median']} 字であり、p10-p90 は {window_chars['p10']}-{window_chars['p90']} 字であった。したがって、本稿の 700 トークン窓は、漢字を中心とする本文でおおむね 460 字前後に相当する。ここでの文字数は Python 文字列上の文字数であり、句読点や記号も含む。", st["body"]),
                Paragraph("100 トークン重なりにより、境界付近の本文は隣接チャンクにも部分的に含まれる。そのため、境界差の影響は本文重心や巻単位の集計では平均化されやすく、今回の大局的安定性を支える要因の一つと考えられる。ただし、この重なりはチャンク単位の1位参照源判定の揺れを完全に抑えるものではない。", st["body"]),
                Paragraph("技術注: 実装では tiktoken の offsets を用いてトークン位置を Python 文字列の文字位置へ対応させた。旧方式の再現確認では、v1.0.0 と同じ固定長トークン列の復号を用いた。", st["small"]),
                Paragraph("文字列品質", st["h2"]),
                pdf_table(rows_for_strategy(data, lang), lang),
                Paragraph("数値評価", st["h2"]),
                Paragraph(f"埋め込みモデルは {data['method']['model']}。旧方式の埋め込みは既存の埋め込みキャッシュを用い、改訂方式の本文断片だけを同じモデルで新規に埋め込んだ。公開成果物には、生本文やチャンク本文そのものは含めない。", st["body"]),
                pdf_table(embedding_rows(data, lang), lang),
                Paragraph(f"同じ本文ごとに旧方式と改訂方式の重心を比較すると、最小値でも {fmt(data['embedding_comparison']['text_centroid_old_safe_cosine_summary']['min'])} であり、全体として高い一致を示した。", st["body"]),
                pdf_table(text_centroid_rows(data, lang), lang),
                Paragraph("三層別の確認", st["h2"]),
                Paragraph("ここでいう意味層は、ターゲットチャンクと参照源チャンクの埋め込み cosine に基づく参照源混合である。したがって、意味層の入れ替わりは埋め込み空間全体の崩れではなく、埋め込みを用いた局所的な参照源順位が境界処理差に反応したものとして読む。", st["body"]),
                Paragraph(f"三層参照源混合地図についても、旧方式と改訂方式を同じ条件で比較した。意味層の参照源混合では、チャンク単位の支配的参照源が {three_data['layer_comparison']['semantic']['dominant_source_changed_chunks']} / {three_data['layer_comparison']['semantic']['chunk_count']} で入れ替わった。一方、巻別の支配的参照源は変化せず、文体・語彙層の入れ替わりは {three_data['layer_comparison']['lexical']['dominant_source_changed_chunks']} / {three_data['layer_comparison']['lexical']['chunk_count']}、典拠マーカー層は {three_data['layer_comparison']['citation']['dominant_source_changed_chunks']} / {three_data['layer_comparison']['citation']['chunk_count']} であった。", st["body"]),
                pdf_table(three_layer_rows(three_data, lang), lang),
                Paragraph("典拠マーカー層では、マーカー検出チャンク数と総マーカー検出数も一致した。", st["body"]),
                pdf_table(marker_rows(three_data, lang), lang),
                Spacer(1, 4 * mm),
            ]
        )
    else:
        story.extend(
            [
                Paragraph("Errata and Supplement: adopting Unicode-aware chunking", st["title"]),
                Paragraph("v1.0.1 supplement. June 4, 2026.", st["small"]),
                Paragraph("Summary", st["h2"]),
                Paragraph("This erratum does not replace the broad semantic map in the v1.0.0 release. In the old method, the token stream was split into fixed-length windows and each window was converted back to text on its own. Some chunk boundaries therefore cut through a character representation, producing the replacement character U+FFFD in the chunk text. This erratum evaluates a revised method that keeps the same 700-token windows and 100-token overlap while adjusting chunk boundaries to Unicode character boundaries.", st["body"]),
                Paragraph("U+FFFD appears because tiktoken tokens are not Unicode characters themselves; they are units over UTF-8 byte sequences. A CJK character is represented by multiple bytes and can, in some cases, span multiple tokens. When a fixed-length token slice is decoded by itself, the start or end of the slice may contain an incomplete UTF-8 sequence, which is then emitted as the replacement character U+FFFD.", st["body"]),
                Paragraph(f"In this corpus, the {window_chars['count']} revised chunks that reach 700 tokens have a median length of {window_chars['median']} characters, with a p10-p90 range of {window_chars['p10']}-{window_chars['p90']} characters. The 700-token window therefore corresponds roughly to about 460 CJK text characters in these classical Chinese-based materials. Character counts are Python string characters and include punctuation and symbols.", st["body"]),
                Paragraph("The 100-token overlap means that text near a boundary is also partly present in adjacent chunks. Boundary-level differences are therefore more likely to be averaged out in text centroids and volume-level summaries, which is one plausible reason for the broad stability observed here. The overlap does not, however, eliminate all chunk-level first-place source changes.", st["body"]),
                Paragraph("Technical note: the implementation uses tiktoken offsets to map token positions to Python string positions. The old behavior was reproduced with the same fixed-token decoding used in v1.0.0.", st["small"]),
                Paragraph("String Quality", st["h2"]),
                pdf_table(rows_for_strategy(data, lang), lang),
                Paragraph("Quantitative Evaluation", st["h2"]),
                Paragraph(f"The embedding model is {data['method']['model']}. The old-method embeddings use the existing embedding cache. Only the revised chunks were newly embedded with the same model. Public outputs do not include raw text or chunk text.", st["body"]),
                pdf_table(embedding_rows(data, lang), lang),
                Paragraph(f"At the text level, the old and revised centroids remain closely aligned. The lowest text-centroid cosine is {fmt(data['embedding_comparison']['text_centroid_old_safe_cosine_summary']['min'])}.", st["body"]),
                pdf_table(text_centroid_rows(data, lang), lang),
                Paragraph("Three-Layer Check", st["h2"]),
                Paragraph("The semantic layer here is an embedding-based source mixture: it uses cosine similarity between target chunks and source chunks. The source changes in this layer should therefore be read as changes in local source rankings derived from embeddings, not as a collapse of the embedding space as a whole.", st["body"]),
                Paragraph(f"The three-layer source-mixture map was also recomputed under the old and revised chunking methods. In the semantic source-mixture layer, the dominant source changes for {three_data['layer_comparison']['semantic']['dominant_source_changed_chunks']} / {three_data['layer_comparison']['semantic']['chunk_count']} chunks. However, the dominant source by volume does not change. In the style/lexical layer, the dominant source changes for {three_data['layer_comparison']['lexical']['dominant_source_changed_chunks']} / {three_data['layer_comparison']['lexical']['chunk_count']} chunks. In the source-marker layer, it changes for {three_data['layer_comparison']['citation']['dominant_source_changed_chunks']} / {three_data['layer_comparison']['citation']['chunk_count']} chunks.", st["body"]),
                pdf_table(three_layer_rows(three_data, lang), lang),
                Paragraph("For the source-marker layer, the number of chunks with detected markers and the total number of marker hits are unchanged.", st["body"]),
                pdf_table(marker_rows(three_data, lang), lang),
                Spacer(1, 4 * mm),
            ]
        )
    figure_path = FIGURE_JA_PATH if lang == "ja" else FIGURE_EN_PATH
    if figure_path.exists():
        story.append(Image(str(figure_path), width=168 * mm, height=122.3 * mm))
        if lang == "ja":
            story.append(Paragraph("図: 旧方式と改訂方式の本文重心。線は同じ本文の対応を示す。", st["small"]))
        else:
            story.append(Paragraph("Figure: text centroids for the old and revised methods. Lines connect the same text.", st["small"]))
    if lang == "ja":
        story.extend(
            [
                Paragraph("解釈", st["h2"]),
                Paragraph(f"旧方式で発生した U+FFFD は、本文品質と再現性の問題として明確に避けるべきである。一方、同じ位置にあるチャンク同士の埋め込み類似度は平均 {fmt(data['embedding_comparison']['same_index_chunk_cosine_overall']['mean'])}、中央値 {fmt(data['embedding_comparison']['same_index_chunk_cosine_overall']['median'])} であり、本文ごとの重心と宗派ごとの重心も高い一致を示した。したがって、v1.0.0 の大局的な意味地図をただちに否定するものではない。", st["body"]),
                Paragraph("ただし、意味層の参照源混合は、チャンク単位の1位参照源判定において Unicode 境界処理の差に一定の感度を示した。これは、参照源候補同士が近い局所箇所では入力ノイズにより順位が入れ替わり得ることを示す。一方で、100 トークン重なりは境界付近の差異を隣接チャンクへ部分的に分散させ、本文重心や巻単位の傾向を安定させる方向に働いたと考えられる。巻別の支配的参照源、文体・語彙層、典拠マーカー層は大きく崩れなかった。三層に分けることにより、どの層が揺れ、どの層が安定しているかを分離して確認できた点も、本稿の方法上の利点である。", st["body"]),
                Paragraph("本文断片の表示、SAT 行範囲との対応、個別チャンク近傍、引用候補の精査では、旧方式を基準にしない。今後は、文字境界を保つ改訂方式を基準処理とする。", st["body"]),
            ]
        )
    else:
        story.extend(
            [
                Paragraph("Interpretation", st["h2"]),
                Paragraph(f"The U+FFFD issue is a real text-quality and reproducibility problem. At the same time, embedding cosine for chunks at the same position remains high: mean {fmt(data['embedding_comparison']['same_index_chunk_cosine_overall']['mean'])} and median {fmt(data['embedding_comparison']['same_index_chunk_cosine_overall']['median'])}. Text and sect centroids also remain closely aligned. The broad semantic map in v1.0.0 is therefore not immediately invalidated.", st["body"]),
                Paragraph("The semantic source-mixture layer nevertheless shows measurable sensitivity in chunk-level first-place source assignments. This suggests that local source rankings can change under input noise when candidate sources are close. At the same time, the 100-token overlap plausibly spreads boundary-level differences into adjacent chunks and helps stabilize text centroids and volume-level tendencies. By contrast, volume-level dominant sources, the style/lexical layer, and the source-marker layer remain stable. This is also a methodological advantage of the three-layer design: it separates where the analysis is sensitive from where it is stable.", st["body"]),
                Paragraph("Displaying chunk excerpts, SAT line-range correspondence, individual-neighbor inspection, and future citation-level analysis should not use the old method as the baseline. Future work should use the revised Unicode-aware method.", st["body"]),
            ]
        )
    doc.build(story)


def main() -> None:
    data = load_summary()
    three_data = load_three_layer_summary()
    write_html(data, three_data)
    write_pdf(data, three_data, "ja")
    write_pdf(data, three_data, "en")
    print(f"wrote {HTML_JA.relative_to(ROOT)}")
    print(f"wrote {HTML_EN.relative_to(ROOT)}")
    print(f"wrote {PDF_JA.relative_to(ROOT)}")
    print(f"wrote {PDF_EN.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
