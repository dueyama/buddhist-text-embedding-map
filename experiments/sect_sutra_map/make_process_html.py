#!/usr/bin/env python3
"""Render the repository process report Markdown as a static Pages HTML file."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs" / "repo-launch-process-report.md"
OUTPUT = ROOT / "docs" / "process" / "index.html"


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        lambda match: f'<a href="{html.escape(match.group(2), quote=True)}">{match.group(1)}</a>',
        escaped,
    )
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def close_lists(parts: list[str], stack: list[str]) -> None:
    while stack:
        parts.append(f"</{stack.pop()}>")


def markdown_to_html(markdown: str) -> str:
    parts: list[str] = []
    stack: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            close_lists(parts, stack)
            parts.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_lists(parts, stack)
            level = len(heading.group(1))
            text = inline_markdown(heading.group(2))
            parts.append(f"<h{level}>{text}</h{level}>")
            continue

        bullet = re.match(r"^-\s+(.+)$", stripped)
        if bullet:
            flush_paragraph()
            if stack != ["ul"]:
                close_lists(parts, stack)
                stack.append("ul")
                parts.append("<ul>")
            parts.append(f"<li>{inline_markdown(bullet.group(1))}</li>")
            continue

        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if numbered:
            flush_paragraph()
            if stack != ["ol"]:
                close_lists(parts, stack)
                stack.append("ol")
                parts.append("<ol>")
            parts.append(f"<li>{inline_markdown(numbered.group(1))}</li>")
            continue

        paragraph.append(stripped)

    flush_paragraph()
    close_lists(parts, stack)
    return "\n".join(parts)


def page(content: str) -> str:
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>制作プロセス | 宗派別お経マップ</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7f2;
      --paper: #ffffff;
      --ink: #202723;
      --muted: #66706a;
      --line: #d9ded6;
      --accent: #2f6f73;
      --warm: #9a5b3f;
      font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", "Noto Sans JP", sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--ink); line-height: 1.82; }}
    header {{ background: var(--paper); border-bottom: 1px solid var(--line); padding: 28px 0 18px; }}
    main {{ background: var(--paper); border: 1px solid var(--line); border-radius: 8px; margin: 22px auto 44px; padding: 32px 44px; }}
    .wrap {{ width: min(980px, calc(100% - 40px)); margin: 0 auto; }}
    a {{ color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 3px; }}
    .site-nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }}
    .nav-link {{ display: inline-flex; align-items: center; min-height: 36px; padding: 0 13px; border: 1px solid var(--line); border-radius: 6px; background: #fff; color: var(--ink); font-size: 14px; text-decoration: none; }}
    .nav-link[aria-current="page"] {{ border-color: #bccbc8; background: #f4f7f5; color: var(--accent); font-weight: 700; }}
    h1 {{ margin: 0; font-size: clamp(28px, 4.2vw, 44px); line-height: 1.2; letter-spacing: 0; }}
    h2 {{ margin: 34px 0 10px; padding-top: 12px; border-top: 1px solid var(--line); font-size: 24px; line-height: 1.35; letter-spacing: 0; }}
    h3 {{ margin: 24px 0 8px; font-size: 19px; line-height: 1.35; letter-spacing: 0; }}
    h4 {{ margin: 20px 0 8px; font-size: 16px; line-height: 1.35; letter-spacing: 0; }}
    p {{ margin: 0 0 14px; }}
    ul, ol {{ padding-left: 1.5em; margin: 8px 0 18px; }}
    li {{ margin: 4px 0; }}
    code {{ background: #f0f3ed; border: 1px solid var(--line); border-radius: 4px; padding: 1px 4px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.92em; }}
    .lead {{ color: var(--muted); margin-top: 10px; max-width: 760px; }}
    .note {{ border-left: 5px solid var(--warm); background: #fffaf5; padding: 14px 16px; margin: 20px 0; color: var(--ink); }}
    footer {{ border-top: 1px solid var(--line); padding: 18px 0; color: var(--muted); font-size: 12px; background: var(--paper); }}
    @media (max-width: 720px) {{
      main {{ padding: 24px 22px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>制作プロセス</h1>
      <p class="lead">Okyouリポジトリの立ち上げから、実験、査読対応、PDF/HTML論文、GitHub Pages公開準備までの流れをまとめた記録です。</p>
      <nav class="site-nav" aria-label="サイト内ナビゲーション">
        <a class="nav-link" href="../">トップ</a>
        <a class="nav-link" href="../paper/">論文</a>
        <a class="nav-link" href="../paper/sect-sutra-map-paper.pdf">PDF</a>
        <a class="nav-link" href="../viewer/">ビューア</a>
        <a class="nav-link" href="./" aria-current="page">制作プロセス</a>
      </nav>
    </div>
  </header>
  <main class="wrap">
    <section class="note">
      OpenAI APIキー、ChatGPT Proアカウント、ローカルCodex/Git環境を前提に、人文学系データ解析研究をAI支援で半自動的に進めるための実例として読めるように整理しています。
    </section>
{content}
  </main>
  <footer>
    <div class="wrap">宗派別お経マップ v0.1。制作プロセス文書は研究用の予備的記録です。</div>
  </footer>
</body>
</html>
"""


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    content = markdown_to_html(SOURCE.read_text(encoding="utf-8"))
    OUTPUT.write_text(page(content), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
