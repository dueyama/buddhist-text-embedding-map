#!/usr/bin/env python3
"""Shared helpers for the sect sutra map experiment."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = ROOT / "outputs"
EMBEDDING_CACHE_DIR = OUTPUT_DIR / "embedding_cache"
MANIFEST_PATH = ROOT / "manifest.json"


def ensure_dirs() -> None:
    for path in [RAW_DIR, PROCESSED_DIR, OUTPUT_DIR, EMBEDDING_CACHE_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def load_project_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_manifest() -> list[dict[str, Any]]:
    return load_json(MANIFEST_PATH)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def strip_html(source: str) -> str:
    source = re.sub(r"<script\b.*?</script>", "", source, flags=re.DOTALL | re.IGNORECASE)
    source = re.sub(r"<style\b.*?</style>", "", source, flags=re.DOTALL | re.IGNORECASE)
    source = re.sub(r"<button\b.*?</button>", "", source, flags=re.DOTALL | re.IGNORECASE)
    source = re.sub(r"<br\s*/?>", "\n", source, flags=re.IGNORECASE)
    source = re.sub(r"</(?:div|p|tr|li|td|span|a)>", "\n", source, flags=re.IGNORECASE)
    source = re.sub(r"<[^>]+>", "", source)
    source = html.unescape(source)
    return source.replace("\xa0", " ")


def clean_sat_line(value: str) -> str:
    value = re.sub(r"Image:\s*&[^;]+;", "", value)
    value = re.sub(r"\[Button:[^\]]+\]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def clean_ref(value: str) -> str:
    value = strip_html(value)
    value = re.sub(r"\s+", "", value)
    return value.rstrip(":")


def parse_sat_rows(source: str) -> list[tuple[str, str]]:
    html_rows = re.findall(
        r'<span style="color:black">(T[^<]+)</span><a name="[^"]*">(.*?)</a><br\s*/?>',
        source,
        flags=re.DOTALL,
    )
    if html_rows:
        return [
            (clean_ref(ref), clean_sat_line(strip_html(body)))
            for ref, body in html_rows
        ]

    text = strip_html(source)
    rows: list[tuple[str, str]] = []
    line_pattern = re.compile(r"(T\d{4}[A-Z]?_?\.\d{2}\.\d{4}[abc]\d{2}:)\s*(.*)")
    for raw_line in text.splitlines():
        match = line_pattern.search(raw_line)
        if not match:
            continue
        ref = match.group(1).strip()
        body = clean_sat_line(match.group(2))
        rows.append((ref, body))
    return rows


def normalize_text(lines: Iterable[str]) -> str:
    text = "".join(line.strip() for line in lines if line.strip())
    text = re.sub(r"\s+", "", text)
    return text


def token_chunks(text: str, max_tokens: int = 700, overlap: int = 100) -> list[str]:
    import tiktoken

    if max_tokens <= overlap:
        raise ValueError("max_tokens must be larger than overlap.")

    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    if not tokens:
        return []

    chunks: list[str] = []
    step = max_tokens - overlap
    for start in range(0, len(tokens), step):
        chunk_tokens = tokens[start : start + max_tokens]
        if len(chunk_tokens) < max_tokens // 4 and chunks:
            break
        chunks.append(encoder.decode(chunk_tokens))
    return chunks


def cosine(a: list[float], b: list[float]) -> float:
    import numpy as np

    left = np.array(a, dtype=float)
    right = np.array(b, dtype=float)
    denom = np.linalg.norm(left) * np.linalg.norm(right)
    if denom == 0:
        return 0.0
    return float(np.dot(left, right) / denom)
