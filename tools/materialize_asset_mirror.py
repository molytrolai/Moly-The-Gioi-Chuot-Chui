#!/usr/bin/env python3
"""Materialize successful content-addressed captures into a pinned host/path tree."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def safe_destination(root: Path, host: str, url_path: str) -> Path | None:
    parts = [part for part in Path(unquote(url_path)).parts if part not in {"/", "\\"}]
    if not parts or any(part in {".", ".."} for part in parts):
        return None
    destination = (root / host / Path(*parts)).resolve()
    resolved_root = root.resolve()
    if resolved_root not in destination.parents:
        return None
    return destination


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--capture-root",
        type=Path,
        default=PROJECT_ROOT / "archive" / "clients" / "captured-live",
    )
    parser.add_argument(
        "--mirror-root",
        type=Path,
        default=PROJECT_ROOT / "archive" / "clients" / "offline-mirror",
    )
    parser.add_argument("--host", action="append", default=["mole.61.com"])
    parser.add_argument(
        "--report",
        type=Path,
        default=PROJECT_ROOT / "data" / "server" / "offline-mirror-report.json",
    )
    args = parser.parse_args()

    capture_root = args.capture_root.resolve()
    mirror_root = args.mirror_root.resolve()
    manifest = capture_root / "requests.jsonl"
    allowed_hosts = {host.lower() for host in args.host}
    selected: dict[tuple[str, str], dict[str, object]] = {}

    for line in manifest.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if int(entry.get("status", 0)) != 200 or entry.get("method") != "GET":
            continue
        parsed = urlsplit(str(entry.get("url", "")))
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "http" or host not in allowed_hosts or not parsed.path:
            continue
        selected[(host, parsed.path)] = entry

    report: list[dict[str, object]] = []
    for (host, url_path), entry in sorted(selected.items()):
        digest = str(entry.get("sha256", ""))
        source = capture_root / "objects" / digest[:2] / digest
        destination = safe_destination(mirror_root, host, url_path)
        if destination is None or not source.is_file():
            report.append(
                {
                    "host": host,
                    "path": url_path,
                    "status": "missing-source" if destination else "unsafe-path",
                    "sha256": digest,
                }
            )
            continue
        archived_body = source.read_bytes()
        actual_digest = hashlib.sha256(archived_body).hexdigest()
        if actual_digest != digest:
            report.append(
                {
                    "host": host,
                    "path": url_path,
                    "status": "hash-mismatch",
                    "sha256": digest,
                    "actual_sha256": actual_digest,
                }
            )
            continue
        body = (
            gzip.decompress(archived_body)
            if archived_body.startswith(b"\x1f\x8b")
            else archived_body
        )
        served_digest = hashlib.sha256(body).hexdigest()
        destination.parent.mkdir(parents=True, exist_ok=True)
        if (
            not destination.exists()
            or hashlib.sha256(destination.read_bytes()).hexdigest() != served_digest
        ):
            destination.write_bytes(body)
        report.append(
            {
                "host": host,
                "path": url_path,
                "status": "ready",
                "bytes": len(body),
                "source_bytes": len(archived_body),
                "source_sha256": digest,
                "sha256": served_digest,
                "destination": str(destination),
            }
        )

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    ready = [entry for entry in report if entry["status"] == "ready"]
    total_bytes = sum(int(entry.get("bytes", 0)) for entry in ready)
    print(f"offline mirror: {len(ready)} files, {total_bytes} bytes")
    failures = [entry for entry in report if entry["status"] != "ready"]
    if failures:
        raise SystemExit(f"offline mirror has {len(failures)} unresolved entries")


if __name__ == "__main__":
    main()
