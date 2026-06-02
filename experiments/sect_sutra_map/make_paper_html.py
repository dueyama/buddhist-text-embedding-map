#!/usr/bin/env python3
"""Render the sect sutra paper TeX source as a readable GitHub Pages HTML page."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = PROJECT_ROOT / "docs/paper/sect-sutra-map-paper-5.tex"
DEFAULT_OUTPUT = PROJECT_ROOT / "docs/paper/index.html"
AUTHOR_URL = "https://sites.google.com/site/dueyama/"
GLOSSARY_SECTION_MARKER = '<h2 id="付録-用語-モデル-ツール">'
GLOSSARY_DEFINITIONS = [
    ("<strong>コーパス：</strong>", "glossary-corpus"),
    ("<strong>前処理と正規化：</strong>", "glossary-preprocess"),
    ("<strong>トークン：</strong>", "glossary-token"),
    ("<strong><code>tiktoken</code> と <code>cl100k_base</code>：</strong>", "glossary-tiktoken"),
    ("<strong>チャンクとオーバーラップ：</strong>", "glossary-chunk"),
    ("<strong>埋め込みと <code>text-embedding-3-large</code>：</strong>", "glossary-embedding"),
    ("<strong>埋め込み空間：</strong>", "glossary-embedding-space"),
    ("<strong>OpenAI API、APIキー、SDK：</strong>", "glossary-openai-api"),
    ("<strong>APIトークンとキャッシュ：</strong>", "glossary-api-cache"),
    ("<strong>コサイン類似度：</strong>", "glossary-cosine"),
    ("<strong>L2正規化：</strong>", "glossary-l2"),
    ("<strong>重心：</strong>", "glossary-centroid"),
    ("<strong>PCA：</strong>", "glossary-pca"),
    ("<strong>寄与率：</strong>", "glossary-explained-variance"),
    ("<strong>1標準偏差楕円：</strong>", "glossary-ellipse"),
    ("<strong>TF-IDF と文字n-gram：</strong>", "glossary-tfidf"),
    ("<strong>stylometry（計量文体論）：</strong>", "glossary-stylometry"),
    ("<strong>top-k近傍とチャンク近傍混合率：</strong>", "glossary-top-k"),
    ("<strong>三層参照源混合地図（source-mixture map）：</strong>", "glossary-source-mixture"),
    ("<strong>softmax：</strong>", "glossary-softmax"),
    ("<strong>optimal transport と unbalanced optimal transport：</strong>", "glossary-optimal-transport"),
    ("<strong>ラベルランダム化と完全混合参照：</strong>", "glossary-randomization"),
    ("<strong>top-1 accuracy、MRR、ROC-AUC：</strong>", "glossary-retrieval-metrics"),
    (
        "<strong>parallel句、intertextuality、cross-linguistic semantic textual similarity：</strong>",
        "glossary-parallel-intertextuality",
    ),
    ("<strong>manifest、JSON、HTML：</strong>", "glossary-formats"),
    ("<strong>静的ビューアとGitHub Pages：</strong>", "glossary-static-viewer"),
    ("<strong>SAT、聖教DB、84000：</strong>", "glossary-sources"),
]
GLOSSARY_TERMS = [
    ("cross-linguistic semantic textual similarity", "glossary-parallel-intertextuality"),
    ("cross-lingual semantic textual similarity", "glossary-parallel-intertextuality"),
    ("unbalanced optimal transport", "glossary-optimal-transport"),
    ("三層参照源混合地図", "glossary-source-mixture"),
    ("source-mixture map", "glossary-source-mixture"),
    ("text-embedding-3-large", "glossary-embedding"),
    ("チャンク近傍混合率", "glossary-top-k"),
    ("top-1 accuracy", "glossary-retrieval-metrics"),
    ("intertextuality", "glossary-parallel-intertextuality"),
    ("OpenAI API", "glossary-openai-api"),
    ("OpenAI SDK", "glossary-openai-api"),
    ("APIトークン", "glossary-api-cache"),
    ("APIキー", "glossary-openai-api"),
    ("オーバーラップ", "glossary-chunk"),
    ("完全混合参照", "glossary-randomization"),
    ("ラベルランダム化", "glossary-randomization"),
    ("optimal transport", "glossary-optimal-transport"),
    ("コサイン類似度", "glossary-cosine"),
    ("埋め込み空間", "glossary-embedding-space"),
    ("1標準偏差楕円", "glossary-ellipse"),
    ("静的ビューア", "glossary-static-viewer"),
    ("GitHub Pages", "glossary-static-viewer"),
    ("文字n-gram", "glossary-tfidf"),
    ("cl100k_base", "glossary-tiktoken"),
    ("stylometry", "glossary-stylometry"),
    ("前処理", "glossary-preprocess"),
    ("正規化", "glossary-preprocess"),
    ("コーパス", "glossary-corpus"),
    ("トークン", "glossary-token"),
    ("tiktoken", "glossary-tiktoken"),
    ("チャンク", "glossary-chunk"),
    ("埋め込み", "glossary-embedding"),
    ("キャッシュ", "glossary-api-cache"),
    ("L2正規化", "glossary-l2"),
    ("重心", "glossary-centroid"),
    ("PCA", "glossary-pca"),
    ("寄与率", "glossary-explained-variance"),
    ("TF-IDF", "glossary-tfidf"),
    ("top-k", "glossary-top-k"),
    ("softmax", "glossary-softmax"),
    ("MRR", "glossary-retrieval-metrics"),
    ("ROC-AUC", "glossary-retrieval-metrics"),
    ("parallel句", "glossary-parallel-intertextuality"),
    ("manifest", "glossary-formats"),
    ("JSON", "glossary-formats"),
    ("HTML", "glossary-formats"),
    ("SAT", "glossary-sources"),
    ("聖教DB", "glossary-sources"),
    ("84000", "glossary-sources"),
]


def find_braced(source: str, command: str) -> str:
    match = re.search(rf"\\{command}\{{(.+?)\}}", source, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def linked_author(author: str) -> str:
    escaped = html.escape(author)
    author_link = f'<a href="{AUTHOR_URL}">上山大信</a>'
    return escaped.replace("上山大信", author_link)


def document_body(source: str) -> str:
    match = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", source, flags=re.DOTALL)
    if not match:
        raise ValueError("Could not find LaTeX document body.")
    return match.group(1).strip()


def split_bibliography(body: str) -> tuple[str, str]:
    match = re.search(
        r"\\begin\{thebibliography\}\{99\}(.*?)\\end\{thebibliography\}",
        body,
        flags=re.DOTALL,
    )
    if not match:
        return body, ""
    return body[: match.start()].strip(), match.group(1).strip()


def extract_abstract(body: str) -> tuple[str, str]:
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", body, flags=re.DOTALL)
    if not match:
        return "", body
    abstract = match.group(1).strip()
    without = (body[: match.start()] + body[match.end() :]).strip()
    return abstract, without


def parse_bibliography(source: str) -> tuple[dict[str, int], list[tuple[str, str]]]:
    entries: list[tuple[str, str]] = []
    current_key = ""
    current_lines: list[str] = []
    for raw_line in source.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.match(r"\\bibitem\{([^}]+)\}", line)
        if match:
            if current_key:
                entries.append((current_key, " ".join(current_lines)))
            current_key = match.group(1)
            current_lines = []
            continue
        line = line.replace(r"\newblock", "").strip()
        if line:
            current_lines.append(line)
    if current_key:
        entries.append((current_key, " ".join(current_lines)))
    return {key: index + 1 for index, (key, _) in enumerate(entries)}, entries


def collect_label_numbers(body: str) -> dict[str, str]:
    labels: dict[str, str] = {}
    fig_no = 0
    table_no = 0
    blocks = re.finditer(
        r"\\begin\{(figure|table)\}\[H\](.*?)\\end\{\1\}|\\begin\{longtable\}.*?\\end\{longtable\}",
        body,
        flags=re.DOTALL,
    )
    for match in blocks:
        block = match.group(0)
        if block.startswith(r"\begin{figure}"):
            fig_no += 1
            prefix = "図"
            number = fig_no
        else:
            table_no += 1
            prefix = "表"
            number = table_no
        label = re.search(r"\\label\{([^}]+)\}", block)
        if label:
            labels[label.group(1)] = f"{number}"
            labels[f"typed::{label.group(1)}"] = f"{prefix}{number}"
    return labels


def strip_wrappers(value: str) -> str:
    value = value.replace(r"\centering", "")
    value = value.replace(r"\small", "")
    value = value.replace(r"\footnotesize", "")
    value = value.replace(r"\noindent", "")
    value = re.sub(r"\\setlength\{[^}]+\}\{[^}]+\}", "", value)
    value = re.sub(r"\\label\{[^}]+\}", "", value)
    value = re.sub(r"\\caption\{[^}]+\}", "", value, flags=re.DOTALL)
    value = re.sub(r"\\begin\{tabular\}\{[^}]*\}", "", value)
    value = value.replace(r"\end{tabular}", "")
    value = re.sub(r"\\begin\{longtable\}\{[^}]*\}", "", value)
    value = value.replace(r"\end{longtable}", "")
    return value


def replace_balanced_command(text: str, command: str, open_tag: str, close_tag: str) -> str:
    pattern = rf"\\{command}\{{([^{{}}]*)\}}"
    while re.search(pattern, text):
        text = re.sub(pattern, rf"{open_tag}\1{close_tag}", text)
    return text


def inline_tex(value: str, citation_numbers: dict[str, int], label_numbers: dict[str, str]) -> str:
    value = value.strip()
    value = value.replace("~", " ")
    value = value.replace(r"{\footnotesize", "")
    value = value.replace(r"\%", "%")
    value = value.replace(r"\_", "_")
    value = value.replace(r"\&", "&")
    value = value.replace(r"\par}", "")
    value = value.replace("--", "–")
    value = re.sub(r"\\(?:noindent|small|footnotesize)\b", "", value)
    math_values: list[str] = []

    def stash_math(match: re.Match[str]) -> str:
        math_values.append(match.group(1).strip())
        return f"@@MATH{len(math_values) - 1}@@"

    value = re.sub(r"\$(.+?)\$", stash_math, value)
    escaped = html.escape(value, quote=False)

    def cite_repl(match: re.Match[str]) -> str:
        keys = [key.strip() for key in match.group(1).split(",")]
        links = []
        for key in keys:
            number = citation_numbers.get(key)
            if number is None:
                links.append(html.escape(key))
            else:
                links.append(f'<a href="#ref-{html.escape(key)}">{number}</a>')
        return "[" + ", ".join(links) + "]"

    def ref_repl(match: re.Match[str]) -> str:
        label = match.group(1)
        return label_numbers.get(label, label)

    def url_repl(match: re.Match[str]) -> str:
        url = html.unescape(match.group(1))
        return f'<a href="{html.escape(url, quote=True)}">{html.escape(url)}</a>'

    escaped = re.sub(r"\\cite\{([^}]+)\}", cite_repl, escaped)
    escaped = re.sub(r"\\ref\{([^}]+)\}", ref_repl, escaped)
    escaped = re.sub(r"\\url\{([^}]+)\}", url_repl, escaped)
    escaped = replace_balanced_command(escaped, "texttt", "<code>", "</code>")
    escaped = replace_balanced_command(escaped, "textit", "<em>", "</em>")
    escaped = replace_balanced_command(escaped, "textbf", "<strong>", "</strong>")
    escaped = re.sub(r"\\mathrm\{([^}]+)\}", r"\1", escaped)
    escaped = escaped.replace(r"\cup", "∪")
    escaped = escaped.replace(r"\in", "∈")
    escaped = escaped.replace(r"\max", "max")
    escaped = escaped.replace(r"\tau_S", "τ_S")
    escaped = escaped.replace(r"\tau_T", "τ_T")
    for index, math_value in enumerate(math_values):
        math_html = html.escape(math_value, quote=False)
        escaped = escaped.replace(f"@@MATH{index}@@", f'<span class="math-inline">\\({math_html}\\)</span>')
    return escaped.strip()


def math_block_html(block: str) -> str:
    math_html = html.escape(block.strip(), quote=False)
    return f'<div class="math-display">\\[{math_html}\\]</div>'


def split_rows(block: str) -> list[list[str]]:
    kept_lines = []
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line in {"{\\small", "{", "}"}:
            continue
        if line.startswith((
            r"\begin{table}",
            r"\end{table}",
            r"\begin{tabular}",
            r"\end{tabular}",
            r"\begin{longtable}",
            r"\end{longtable}",
            r"\caption",
            r"\label",
            r"\centering",
            r"\setlength",
        )):
            continue
        if re.fullmatch(r"\\(?:toprule|midrule|bottomrule|endfirsthead|endhead)", line):
            continue
        kept_lines.append(line)
    cleaned = strip_wrappers("\n".join(kept_lines))
    cleaned = re.sub(r"\\(?:toprule|midrule|bottomrule|endfirsthead|endhead)", "", cleaned)
    rows: list[list[str]] = []
    for raw_row in cleaned.split(r"\\"):
        row = raw_row.strip()
        if not row:
            continue
        if row.startswith("{") or row.startswith("}"):
            continue
        cells = [cell.strip() for cell in row.split("&")]
        if len(cells) > 1:
            rows.append(cells)
    if len(rows) > 1 and rows[1] == rows[0]:
        rows.pop(1)
    return rows


def table_html(block: str, citation_numbers: dict[str, int], label_numbers: dict[str, str]) -> str:
    caption_match = re.search(r"\\caption\{(.+?)\}", block, flags=re.DOTALL)
    caption = inline_tex(caption_match.group(1), citation_numbers, label_numbers) if caption_match else ""
    label_match = re.search(r"\\label\{([^}]+)\}", block)
    table_id = f' id="{html.escape(label_match.group(1))}"' if label_match else ""
    if label_match and label_match.group(1) in label_numbers:
        caption = f"表{label_numbers[label_match.group(1)]}. {caption}"
    rows = split_rows(block)
    if not rows:
        return ""
    head = rows[0]
    body_rows = rows[1:]
    head_html = "".join(f"<th>{inline_tex(cell, citation_numbers, label_numbers)}</th>" for cell in head)
    body_html = "\n".join(
        "<tr>" + "".join(f"<td>{inline_tex(cell, citation_numbers, label_numbers)}</td>" for cell in row) + "</tr>"
        for row in body_rows
    )
    caption_html = f"<caption>{caption}</caption>" if caption else ""
    return (
        f'<div class="table-wrap"{table_id}><table>{caption_html}<thead><tr>{head_html}</tr></thead>'
        f"<tbody>{body_html}</tbody></table></div>"
    )


def figure_html(block: str, citation_numbers: dict[str, int], label_numbers: dict[str, str]) -> str:
    image_match = re.search(r"\\includegraphics(?:\[[^]]+\])?\{([^}]+)\}", block)
    caption_match = re.search(r"\\caption\{(.+?)\}", block, flags=re.DOTALL)
    label_match = re.search(r"\\label\{([^}]+)\}", block)
    if not image_match:
        return ""
    src = image_match.group(1)
    label = label_match.group(1) if label_match else ""
    caption = inline_tex(caption_match.group(1), citation_numbers, label_numbers) if caption_match else ""
    number = label_numbers.get(label, "")
    caption_prefix = f"図{number}. " if number else ""
    figure_id = f' id="{html.escape(label)}"' if label else ""
    return (
        f'<figure{figure_id}><img src="{html.escape(src, quote=True)}" alt="{caption}">'
        f"<figcaption>{caption_prefix}{caption}</figcaption></figure>"
    )


def flush_paragraph(parts: list[str], output: list[str]) -> None:
    text = " ".join(part.strip() for part in parts if part.strip()).strip()
    if text:
        output.append(f"<p>{text}</p>")
    parts.clear()


def section_id(title: str) -> str:
    base = re.sub(r"[^\w一-龥ぁ-んァ-ン]+", "-", title, flags=re.UNICODE).strip("-")
    return base or "section"


def add_glossary_definition_ids(fragment: str) -> str:
    for heading, anchor in GLOSSARY_DEFINITIONS:
        fragment = fragment.replace(f"<p>{heading}", f'<p id="{anchor}">{heading}', 1)
    return fragment


def link_glossary_text(text: str, seen_terms: set[str]) -> str:
    term_pairs = sorted(GLOSSARY_TERMS, key=lambda item: len(item[0]), reverse=True)
    pattern = re.compile("|".join(re.escape(term) for term, _ in term_pairs))
    anchors = dict(term_pairs)

    def repl(match: re.Match[str]) -> str:
        term = match.group(0)
        if term in seen_terms:
            return term
        seen_terms.add(term)
        return f'<a class="glossary-link" href="#{anchors[term]}">{term}</a>'

    return pattern.sub(repl, text)


def add_glossary_links(fragment: str, seen_terms: set[str]) -> str:
    output: list[str] = []
    blocked_tags: list[str] = []
    blocked = {"a", "pre", "h1", "h2", "h3", "figcaption", "caption", "th", "script", "style"}
    for token in re.split(r"(<[^>]+>)", fragment):
        if not token:
            continue
        if token.startswith("<"):
            end_tag = re.match(r"</([a-zA-Z0-9]+)>", token)
            start_tag = re.match(r"<([a-zA-Z0-9]+)(?:\s|>|/)", token)
            if end_tag:
                tag = end_tag.group(1).lower()
                if tag in blocked_tags:
                    blocked_tags.remove(tag)
            elif start_tag and not token.endswith("/>"):
                tag = start_tag.group(1).lower()
                if tag in blocked:
                    blocked_tags.append(tag)
            output.append(token)
            continue
        if blocked_tags:
            output.append(token)
        else:
            output.append(link_glossary_text(token, seen_terms))
    return "".join(output)


def add_glossary_anchors_and_links(body_html: str, seen_terms: set[str]) -> str:
    body_html = add_glossary_definition_ids(body_html)
    before, marker, after = body_html.partition(GLOSSARY_SECTION_MARKER)
    if not marker:
        return add_glossary_links(body_html, seen_terms)
    return add_glossary_links(before, seen_terms) + marker + after


def content_html(body: str, citation_numbers: dict[str, int], label_numbers: dict[str, str]) -> str:
    body = body.replace(r"\maketitle", "")
    output: list[str] = []
    paragraph: list[str] = []
    lines = body.splitlines()
    index = 0
    in_list = False
    while index < len(lines):
        raw = lines[index]
        line = raw.strip()
        if not line:
            flush_paragraph(paragraph, output)
            index += 1
            continue
        if line in {"{\\small", "{", "}"} or line.startswith(r"\setlength"):
            index += 1
            continue
        if line == r"\[":
            flush_paragraph(paragraph, output)
            block_lines = []
            index += 1
            while index < len(lines) and lines[index].strip() != r"\]":
                block_lines.append(lines[index].strip())
                index += 1
            if index < len(lines):
                index += 1
            output.append(math_block_html("\n".join(block_lines)))
            continue
        section = re.match(r"\\section\*?\{(.+?)\}", line)
        subsection = re.match(r"\\subsection\*?\{(.+?)\}", line)
        if section or subsection:
            flush_paragraph(paragraph, output)
            title = (section or subsection).group(1)
            clean_title = inline_tex(title, citation_numbers, label_numbers)
            tag = "h2" if section else "h3"
            output.append(f'<{tag} id="{html.escape(section_id(title))}">{clean_title}</{tag}>')
            index += 1
            continue
        if line == r"\begin{enumerate}":
            flush_paragraph(paragraph, output)
            output.append("<ol>")
            in_list = True
            index += 1
            continue
        if line == r"\end{enumerate}":
            flush_paragraph(paragraph, output)
            output.append("</ol>")
            in_list = False
            index += 1
            continue
        item = re.match(r"\\item\s+(.+)", line)
        if item and in_list:
            output.append(f"<li>{inline_tex(item.group(1), citation_numbers, label_numbers)}</li>")
            index += 1
            continue
        if line.startswith(r"\begin{figure}"):
            flush_paragraph(paragraph, output)
            block_lines = [line]
            index += 1
            while index < len(lines) and not lines[index].strip().startswith(r"\end{figure}"):
                block_lines.append(lines[index].strip())
                index += 1
            if index < len(lines):
                block_lines.append(lines[index].strip())
                index += 1
            output.append(figure_html("\n".join(block_lines), citation_numbers, label_numbers))
            continue
        if line.startswith(r"\begin{table}") or line.startswith(r"\begin{longtable}"):
            flush_paragraph(paragraph, output)
            end_token = r"\end{table}" if line.startswith(r"\begin{table}") else r"\end{longtable}"
            block_lines = [line]
            index += 1
            while index < len(lines) and not lines[index].strip().startswith(end_token):
                block_lines.append(lines[index].strip())
                index += 1
            if index < len(lines):
                block_lines.append(lines[index].strip())
                index += 1
            html_table = table_html("\n".join(block_lines), citation_numbers, label_numbers)
            if html_table:
                output.append(html_table)
            continue
        if line.startswith(r"\begin{") or line.startswith(r"\end{"):
            index += 1
            continue
        paragraph.append(inline_tex(line, citation_numbers, label_numbers))
        index += 1
    flush_paragraph(paragraph, output)
    return "\n".join(output)


def bibliography_html(entries: list[tuple[str, str]], citation_numbers: dict[str, int], label_numbers: dict[str, str]) -> str:
    items = []
    for key, value in entries:
        number = citation_numbers[key]
        items.append(
            f'<li id="ref-{html.escape(key)}" value="{number}">'
            f"{inline_tex(value, citation_numbers, label_numbers)}</li>"
        )
    return '<section class="references"><h2 id="references">参考文献</h2><ol>' + "\n".join(items) + "</ol></section>"


def build_html(source: str) -> str:
    title = find_braced(source, "title")
    author = find_braced(source, "author")
    date = find_braced(source, "date")
    body = document_body(source)
    main_body, bibliography = split_bibliography(body)
    abstract, main_body = extract_abstract(main_body)
    citation_numbers, entries = parse_bibliography(bibliography)
    label_numbers = collect_label_numbers(main_body)
    seen_glossary_terms: set[str] = set()
    body_html = content_html(main_body, citation_numbers, label_numbers)
    abstract_html = "\n".join(
        f"<p>{inline_tex(part, citation_numbers, label_numbers)}</p>"
        for part in re.split(r"\n\s*\n", abstract)
        if part.strip()
    )
    abstract_html = add_glossary_links(abstract_html, seen_glossary_terms)
    body_html = add_glossary_anchors_and_links(body_html, seen_glossary_terms)
    references = bibliography_html(entries, citation_numbers, label_numbers)
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f8f4;
      --paper: #ffffff;
      --ink: #1f2723;
      --muted: #657069;
      --line: #d8ded6;
      --accent: #2f6f73;
      --warm: #9a5b3f;
      font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", "Noto Sans JP", sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--ink); line-height: 1.82; }}
    a {{ color: var(--accent); text-underline-offset: 3px; }}
    .page {{ width: min(980px, calc(100% - 32px)); margin: 0 auto; }}
    header {{ padding: 36px 0 22px; border-bottom: 1px solid var(--line); background: var(--paper); }}
    main {{ background: var(--paper); border: 1px solid var(--line); border-radius: 8px; margin: 22px auto 44px; padding: 34px 44px; }}
    h1 {{ margin: 0 0 12px; font-size: clamp(28px, 4vw, 42px); line-height: 1.22; letter-spacing: 0; }}
    .meta {{ color: var(--muted); font-size: 14px; }}
    .actions {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px; }}
    .button {{ display: inline-flex; min-height: 36px; align-items: center; padding: 0 13px; border: 1px solid var(--line); border-radius: 6px; color: var(--ink); text-decoration: none; background: #fff; font-size: 14px; }}
    .button.primary {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
    .abstract {{ border-left: 5px solid var(--accent); background: #f4f7f5; padding: 18px; margin: 0 0 24px; }}
    .abstract h2 {{ margin-top: 0; }}
    h2 {{ margin: 34px 0 12px; font-size: 25px; line-height: 1.35; letter-spacing: 0; }}
    h3 {{ margin: 26px 0 10px; font-size: 19px; line-height: 1.4; letter-spacing: 0; }}
    p {{ margin: 0 0 1em; }}
    code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.92em; background: #f3f5f2; padding: 0 3px; border-radius: 3px; }}
    .math-inline {{ white-space: nowrap; }}
    .math-display {{ margin: 16px 0 20px; padding: 13px 16px; border: 1px solid var(--line); border-radius: 6px; background: #f8faf7; color: #25302b; overflow-x: auto; }}
    .glossary-link {{ color: var(--accent); text-decoration-style: dotted; text-decoration-thickness: 1px; text-underline-offset: 3px; }}
    p[id^="glossary-"] {{ scroll-margin-top: 18px; }}
    figure {{ margin: 26px 0; }}
    figure img {{ display: block; width: 100%; height: auto; border: 1px solid var(--line); border-radius: 7px; background: #fff; }}
    figcaption, caption {{ color: var(--muted); font-size: 13px; line-height: 1.6; }}
    figcaption {{ margin-top: 8px; }}
    .table-wrap {{ overflow-x: auto; margin: 24px 0; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; line-height: 1.55; }}
    th, td {{ border: 1px solid var(--line); padding: 7px 8px; vertical-align: top; }}
    th {{ background: #f5f7f4; font-weight: 700; }}
    caption {{ caption-side: top; text-align: left; margin-bottom: 8px; font-weight: 700; }}
    ol {{ padding-left: 1.5em; }}
    .references ol {{ font-size: 13px; line-height: 1.6; }}
    .references li {{ margin-bottom: 0.7em; }}
    @media (max-width: 720px) {{
      main {{ padding: 22px 18px; }}
      table {{ font-size: 13px; }}
    }}
  </style>
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [["\\\\(", "\\\\)"]],
        displayMath: [["\\\\[", "\\\\]"]],
        processEscapes: true
      }},
      svg: {{ fontCache: "global" }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
  <header>
    <div class="page">
      <h1>{html.escape(title)}</h1>
      <div class="meta">{linked_author(author)} / {html.escape(date)}</div>
      <div class="actions">
        <a class="button primary" href="./">HTMLで読む</a>
        <a class="button" href="sect-sutra-map-paper-5.pdf">PDF版</a>
        <a class="button" href="../viewer/">公開版ビューア</a>
        <a class="button" href="../">プロジェクト概要</a>
      </div>
    </div>
  </header>
  <main class="page">
    <section class="abstract">
      <h2>要旨</h2>
      {abstract_html}
    </section>
    {body_html}
    {references}
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.is_absolute():
        input_path = PROJECT_ROOT / input_path
    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_html(input_path.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"Wrote {output_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
