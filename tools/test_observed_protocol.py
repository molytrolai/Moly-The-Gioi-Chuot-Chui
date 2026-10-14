#!/usr/bin/env python3
"""Replay every observed world request body against the local response builder."""

from __future__ import annotations

import json
import struct
from pathlib import Path

import moly_probe_server as moly


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = PROJECT_ROOT / "data" / "server" / "probe-events.jsonl"
USER_ID = 10_000_001


def observed_requests() -> dict[int, tuple[int, bytes]]:
    requests: dict[int, tuple[int, bytes]] = {}
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("event") != "decrypted-frame" or event.get("port") != 3200:
            continue
        command = int(event["cmd"])
        requests[command] = (
            int(event.get("version", 1)),
            bytes.fromhex(str(event.get("body_hex", ""))),
        )
    return requests


def main() -> None:
    requests = observed_requests()
    tested: list[int] = []
    for command, (version, body) in sorted(requests.items()):
        if command == 201 or command in moly.KNOWN_ONE_WAY_COMMANDS:
            continue
        response = moly.world_response(command, USER_ID, version, body)
        if response is None:
            raise AssertionError(f"observed command {command} has no response")
        if len(response) < 18:
            raise AssertionError(f"command {command} returned a short encrypted packet")
        length, response_version, response_command, response_user, result = struct.unpack(
            ">IBIII", response[:17]
        )
        assert length == len(response), command
        assert response_version == version, command
        assert response_command == command, command
        assert response_user == USER_ID, command
        assert result == 0, command
        encrypted_body = response[17:]
        assert moly.moly_encrypt(moly.moly_decrypt(encrypted_body)) == encrypted_body
        tested.append(command)

    expected = len(requests) - len(
        set(requests) & ({201} | moly.KNOWN_ONE_WAY_COMMANDS)
    )
    assert len(tested) == expected
    print(f"observed protocol replay: OK ({len(tested)} responses)")


if __name__ == "__main__":
    main()
