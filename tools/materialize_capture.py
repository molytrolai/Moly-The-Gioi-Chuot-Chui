#!/usr/bin/env python3
"""Create a readable host/path tree from the immutable capture object store."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


def safe_parts(path: str) -> list[str]:
    parts: list[str] = []
    for part in PurePosixPath(unquote(path)).parts:
        if part in {"", "/", ".", ".."}:
            continue
        cleaned = "".join(
            character if character not in '<>:"\\|?*' else "_" for character in part
        )
        parts.append(cleaned or "_")
    return parts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()

    archive = args.archive.resolve()
    objects = archive / "objects"
    output = archive / "named"
    latest: dict[tuple[str, str], dict[str, object]] = {}
    with (archive / "requests.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            entry = json.loads(line)
            if entry.get("status") != 200:
                continue
            parsed = urlsplit(str(entry["url"]))
            latest[(parsed.netloc.lower(), parsed.path)] = entry

    output.mkdir(parents=True, exist_ok=True)
    index: list[dict[str, object]] = []
    for (host, path), entry in sorted(latest.items()):
        digest = str(entry["sha256"])
        source = objects / digest[:2] / digest
        relative_parts = safe_parts(path)
        if not relative_parts or path.endswith("/"):
            relative_parts.append("index")
        destination = output.joinpath(host, *relative_parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        index.append(
            {
                "host": host,
                "path": path,
                "url": entry["url"],
                "sha256": digest,
                "size": entry["size"],
                "file": str(destination.relative_to(archive)),
            }
        )

    (archive / "named-manifest.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Materialized {len(index)} latest public assets in {output}")


if __name__ == "__main__":
    main()
