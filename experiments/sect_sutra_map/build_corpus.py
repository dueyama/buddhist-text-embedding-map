#!/usr/bin/env python3
"""Build the local processed corpus for the sect sutra map."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import requests

from common import (
    PROJECT_ROOT,
    PROCESSED_DIR,
    RAW_DIR,
    ensure_dirs,
    load_manifest,
    normalize_text,
    parse_sat_rows,
    sha256_text,
    write_json,
)


def fetch_sat(item: dict[str, Any], refresh: bool = False) -> str:
    raw_path = RAW_DIR / f"{item['id']}.html"
    if raw_path.exists() and not refresh:
        return raw_path.read_text(encoding="utf-8")

    response = requests.get(item["source_url"], timeout=45)
    response.raise_for_status()
    raw_path.write_text(response.text, encoding="utf-8")
    return response.text


def read_local(item: dict[str, Any]) -> str:
    path = PROJECT_ROOT / item["source_url"]
    if not path.exists():
        raise FileNotFoundError(f"Local source not found: {path}")
    return path.read_text(encoding="utf-8")


def rows_from_local(source: str) -> list[tuple[str, str]]:
    rows = []
    for index, line in enumerate(source.splitlines(), start=1):
        body = line.strip()
        if body:
            rows.append((f"local:{index}", body))
    return rows


def build_item(item: dict[str, Any], refresh: bool = False) -> dict[str, Any]:
    if item["source"] == "sat":
        source = fetch_sat(item, refresh=refresh)
        rows = parse_sat_rows(source)
    elif item["source"] == "local":
        source = read_local(item)
        rows = rows_from_local(source)
    else:
        raise ValueError(f"Unsupported source type: {item['source']}")

    rows = [(ref, body) for ref, body in rows if body]
    body = normalize_text(body for _, body in rows)
    if not body:
        raise ValueError(f"Empty body after processing: {item['id']}")

    line_path = PROCESSED_DIR / f"{item['id']}_lines.tsv"
    body_path = PROCESSED_DIR / f"{item['id']}_body.txt"
    line_path.write_text(
        "\n".join(f"{ref}\t{body}" for ref, body in rows) + "\n",
        encoding="utf-8",
    )
    body_path.write_text(body + "\n", encoding="utf-8")

    return {
        **item,
        "line_count": len(rows),
        "char_count": len(body),
        "body_sha256": sha256_text(body),
        "body_path": str(body_path.relative_to(PROJECT_ROOT)),
        "line_path": str(line_path.relative_to(PROJECT_ROOT)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Fetch SAT HTML again.")
    args = parser.parse_args()

    ensure_dirs()
    items = [build_item(item, refresh=args.refresh) for item in load_manifest()]
    write_json(PROCESSED_DIR / "corpus_index.json", {"texts": items})

    for item in items:
        print(f"{item['id']}: {item['char_count']} chars, {item['line_count']} lines")
    print(f"Wrote {(PROCESSED_DIR / 'corpus_index.json').relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
