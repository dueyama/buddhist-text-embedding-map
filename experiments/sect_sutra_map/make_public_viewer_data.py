#!/usr/bin/env python3
"""Create a public GitHub Pages viewer dataset without source text previews."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import OUTPUT_DIR, PROJECT_ROOT, load_json, write_json

PREVIEW_PLACEHOLDER = "Preview omitted from the public GitHub Pages data."
PRIVATE_TEXT_KEYS = {"body_path", "line_path", "source_path"}
PRIVATE_CHUNK_KEYS = set()


def scrub_text(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key not in PRIVATE_TEXT_KEYS}


def scrub_chunk(record: dict[str, Any]) -> dict[str, Any]:
    public = {key: value for key, value in record.items() if key not in PRIVATE_CHUNK_KEYS}
    public["preview"] = PREVIEW_PLACEHOLDER
    return public


def scrub_nearest_chunks(value: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for text_id, items in value.items():
        result[text_id] = []
        for item in items:
            public = dict(item)
            public["preview"] = PREVIEW_PLACEHOLDER
            result[text_id].append(public)
    return result


def assert_no_text_previews(data: dict[str, Any]) -> None:
    previews = [chunk.get("preview", "") for chunk in data.get("chunks", [])]
    previews.extend(
        item.get("preview", "")
        for items in data.get("nearest_chunks", {}).values()
        for item in items
    )
    leaked = [value for value in previews if value and value != PREVIEW_PLACEHOLDER]
    if leaked:
        raise RuntimeError("Public viewer data still contains non-placeholder previews.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(OUTPUT_DIR / "viewer_data.json"))
    parser.add_argument("--output", default=str(PROJECT_ROOT / "docs/viewer/viewer_data.json"))
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.is_absolute():
        input_path = PROJECT_ROOT / input_path
    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path

    data = load_json(input_path)
    public_data = dict(data)
    public_data["texts"] = [scrub_text(text) for text in data.get("texts", [])]
    public_data["chunks"] = [scrub_chunk(chunk) for chunk in data.get("chunks", [])]
    public_data["nearest_chunks"] = scrub_nearest_chunks(data.get("nearest_chunks", {}))
    public_data["publication_note"] = (
        "This public dataset omits raw source text and chunk previews. "
        "Use source_url fields and local rebuild scripts to reproduce corpus text."
    )

    assert_no_text_previews(public_data)
    write_json(output_path, public_data)
    print(f"Texts: {len(public_data['texts'])}")
    print(f"Chunks: {len(public_data['chunks'])}")
    print(f"Wrote {output_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
