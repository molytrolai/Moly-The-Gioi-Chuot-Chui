#!/usr/bin/env python3
"""Verify that every current map-graph asset is served locally without upstream."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def inspect(proxy: str, asset: str) -> dict[str, object]:
    relative = urllib.parse.urlsplit(asset).path.lstrip("/")
    url = proxy.rstrip("/") + "/" + urllib.parse.quote(relative, safe="/")
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"Host": "mole.61.com", "Connection": "close"},
    )
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                source = response.headers.get("X-Moly-Source", "")
                length = int(response.headers.get("Content-Length", "0"))
                ok = (
                    response.status == 200
                    and source in {"override", "mirror"}
                    and length > 0
                )
                return {
                    "asset": asset,
                    "status": response.status,
                    "source": source,
                    "bytes": length,
                    "ok": ok,
                    "attempts": attempt,
                }
        except (OSError, ValueError, urllib.error.URLError) as error:
            last_error = error
    return {
        "asset": asset,
        "status": 0,
        "source": "",
        "bytes": 0,
        "ok": False,
        "attempts": 3,
        "error": f"{type(last_error).__name__}: {last_error}",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proxy", default="http://127.0.0.1:18080")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--graph",
        type=Path,
        default=PROJECT_ROOT
        / "archive"
        / "community"
        / "moleworld.net"
        / "mole2016"
        / "current"
        / "mo-mapgraph.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data" / "server" / "offline-map-audit.json",
    )
    args = parser.parse_args()

    graph = json.loads(args.graph.read_text(encoding="utf-8-sig"))
    assets = sorted(
        {
            str(asset)
            for map_assets in graph.get("maps", {}).values()
            for asset in map_assets
            if isinstance(asset, str) and asset
        }
    )
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        results = list(pool.map(lambda asset: inspect(args.proxy, asset), assets))

    failures = [result for result in results if not result["ok"]]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "graph": str(args.graph.resolve()),
        "asset_count": len(assets),
        "local_count": len(results) - len(failures),
        "failed_count": len(failures),
        "sources": {
            source: sum(result["source"] == source for result in results)
            for source in ("override", "mirror", "")
        },
        "failures": failures,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
