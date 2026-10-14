#!/usr/bin/env python3
"""Report world commands observed in the probe log but not handled locally."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


ONE_WAY_COMMANDS = {
    303: "walking broadcast (the server does not echo it to the sender)",
    305: "avatar action broadcast (the server does not echo it to the sender)",
    9245: "client statistics upload (no response parser is registered)",
    12053: "legacy magic-spirit tutorial notification (no response listener is registered)",
}


def command_names(path: Path) -> dict[int, str]:
    names: dict[int, str] = {}
    pattern = re.compile(r"const\s+([A-Za-z0-9_]+).*?=\s*(\d+)\s*;")
    for name, value in pattern.findall(path.read_text(encoding="utf-8")):
        names.setdefault(int(value), name)
    return names


def handled_commands(path: Path) -> set[int]:
    source = path.read_text(encoding="utf-8")
    return {201} | {
        int(value)
        for value in re.findall(r"(?:if|elif)\s+cmd\s*==\s*(\d+)", source)
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--server", type=Path, required=True)
    parser.add_argument("--command-ids", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    seen: Counter[int] = Counter()
    last_body: dict[int, str] = {}
    for line in args.log.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("event") == "decrypted-frame" and event.get("port") == 3200:
            command = int(event["cmd"])
            seen[command] += 1
            last_body[command] = str(event.get("body_hex", ""))

    names = command_names(args.command_ids)
    handled = handled_commands(args.server)
    missing = [command for command in sorted(seen) if command not in handled and command not in ONE_WAY_COMMANDS]
    report = {
        "observed_command_count": len(seen),
        "handled_observed_count": sum(command in handled for command in seen),
        "known_one_way": [
            {
                "command": command,
                "name": names.get(command),
                "requests": seen[command],
                "reason": ONE_WAY_COMMANDS[command],
            }
            for command in sorted(seen)
            if command in ONE_WAY_COMMANDS
        ],
        "missing": [
            {
                "command": command,
                "name": names.get(command),
                "requests": seen[command],
                "last_body_hex": last_body[command],
            }
            for command in missing
        ],
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
