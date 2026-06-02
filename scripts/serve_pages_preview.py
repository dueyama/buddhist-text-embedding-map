#!/usr/bin/env python3
"""Serve the GitHub Pages docs directory for local or Tailscale preview."""

from __future__ import annotations

import argparse
import functools
import http.client
import subprocess
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def detect_tailscale_ip() -> str | None:
    try:
        result = subprocess.run(
            ["tailscale", "ip", "-4"],
            check=True,
            capture_output=True,
            text=True,
            timeout=3,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

    for line in result.stdout.splitlines():
        ip = line.strip()
        if ip:
            return ip
    return None


def choose_host(bind: str) -> tuple[str, str]:
    tailscale_ip = detect_tailscale_ip()
    if bind == "tailscale":
        if not tailscale_ip:
            raise SystemExit("Tailscale IPv4 address was not available. Is Tailscale running?")
        return tailscale_ip, f"http://{tailscale_ip}"
    if bind == "local":
        return "127.0.0.1", "http://127.0.0.1"
    if bind == "all":
        display = tailscale_ip or "127.0.0.1"
        return "0.0.0.0", f"http://{display}"
    if tailscale_ip:
        return tailscale_ip, f"http://{tailscale_ip}"
    return "127.0.0.1", "http://127.0.0.1"


def probe(host: str, port: int) -> int | None:
    connection: http.client.HTTPConnection | None = None
    try:
        connection = http.client.HTTPConnection(host, port, timeout=3)
        connection.request("HEAD", "/")
        response = connection.getresponse()
        response.read()
        return response.status
    except OSError:
        return None
    finally:
        if connection is not None:
            connection.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serve docs/ for GitHub Pages preview, optionally bound to the Tailscale IP."
    )
    parser.add_argument("--port", type=int, default=8768, help="Port to serve on. Default: 8768")
    parser.add_argument(
        "--bind",
        choices=("auto", "tailscale", "local", "all"),
        default="auto",
        help="Bind address mode. Default: auto, preferring the Tailscale IPv4 address.",
    )
    parser.add_argument(
        "--directory",
        default="docs",
        help="Directory to serve, relative to the repository root unless absolute. Default: docs",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check whether the preview URL responds; do not start a server.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    directory = Path(args.directory)
    if not directory.is_absolute():
        directory = PROJECT_ROOT / directory
    directory = directory.resolve()
    if not directory.is_dir():
        raise SystemExit(f"Preview directory does not exist: {directory}")

    host, display_base = choose_host(args.bind)
    url = f"{display_base}:{args.port}/"

    if args.check:
        status = probe(host, args.port)
        if status is None:
            print(f"not responding: {url}")
            return 1
        print(f"OK {status}: {url}")
        return 0

    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(directory))
    try:
        server = ThreadingHTTPServer((host, args.port), handler)
    except OSError as error:
        status = probe(host, args.port)
        if status is not None:
            print(f"Already running {status}: {url}")
            return 0
        raise SystemExit(f"Could not bind {host}:{args.port}: {error}") from error
    server.daemon_threads = True

    print(f"Serving {directory}")
    print(f"URL: {url}")
    print("Press Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
