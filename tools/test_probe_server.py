#!/usr/bin/env python3
"""End-to-end smoke test for the isolated Moly probe server."""

from __future__ import annotations

import socket
import struct

import moly_probe_server as moly


USER_ID = 10_000_001


def receive_packet(connection: socket.socket) -> tuple[int, int, int, int, bytes]:
    header = connection.recv(17)
    if len(header) != 17:
        raise AssertionError(f"short header: {len(header)}")
    length, version, command, user_id, result = struct.unpack(">IBIII", header)
    body = bytearray()
    while len(body) < length - 17:
        chunk = connection.recv(length - 17 - len(body))
        if not chunk:
            raise AssertionError("connection ended during packet body")
        body += chunk
    return version, command, user_id, result, bytes(body)


def ensure_server() -> None:
    try:
        with socket.create_connection(("127.0.0.1", 1863), timeout=0.5):
            return
    except OSError:
        pass
    import tempfile
    import threading
    import time
    from pathlib import Path

    log_path = (
        Path(tempfile.gettempdir())
        / f"moly_test_probe_{int(time.time())}.jsonl"
    )
    recorder = moly.Recorder(log_path)
    servers = [
        moly.ThreadedServer(("127.0.0.1", port), recorder)
        for port in (1863, 3200)
    ]
    for s in servers:
        threading.Thread(target=s.serve_forever, daemon=True).start()
    time.sleep(0.3)


def main() -> None:
    ensure_server()
    with socket.create_connection(("127.0.0.1", 1863), timeout=3) as connection:
        connection.sendall(moly.packet(103, USER_ID))
        version, command, user_id, result, body = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 103, USER_ID, 0)
        assert body == struct.pack(">I", 0) + moly.SESSION

        connection.sendall(moly.packet(105, USER_ID))
        version, command, user_id, result, body = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 105, USER_ID, 0)
        assert b"127.0.0.1" in body

    request = moly.packet(
        201, USER_ID, moly.moly_encrypt(b"local-smoke-test"), version=65
    )
    with socket.create_connection(("127.0.0.1", 3200), timeout=3) as connection:
        connection.sendall(request)
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (65, 201, USER_ID, 0)
        profile = moly.moly_decrypt(encrypted)
        assert len(profile) == 215
        assert struct.unpack(">I", profile[:4])[0] == USER_ID
        assert profile[4:20].rstrip(b"\0") == b"Moly Admin"
        assert struct.unpack(">I", profile[36:40])[0] == 33
        assert struct.unpack(">II", profile[134:142]) == (8, 120)

        connection.sendall(
            moly.packet(406, USER_ID, moly.moly_encrypt(struct.pack(">II", 1, 0)))
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 406, USER_ID, 0)
        map_info = moly.moly_decrypt(encrypted)
        assert len(map_info) == 80
        assert struct.unpack(">II", map_info[:8]) == (1, 0)

        connection.sendall(
            moly.packet(3106, USER_ID, moly.moly_encrypt(struct.pack(">I", 0)))
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 3106, USER_ID, 0)
        assert moly.moly_decrypt(encrypted) == struct.pack(">I", 0)

        connection.sendall(
            moly.packet(405, USER_ID, moly.moly_encrypt(struct.pack(">III", 1, 0, 0)))
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 405, USER_ID, 0)
        scene = moly.moly_decrypt(encrypted)
        assert len(scene) == 223
        assert struct.unpack(">II", scene[:8]) == (1, USER_ID)
        assert struct.unpack(">I", scene[40:44])[0] == 33
        assert struct.unpack(">II", scene[44:52]) == (1, 0)

        connection.sendall(moly.packet(2032, USER_ID, moly.moly_encrypt(b"")))
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 2032, USER_ID, 0)
        assert struct.unpack(">I", moly.moly_decrypt(encrypted))[0] == 99_999_900

        connection.sendall(moly.packet(2031, USER_ID, moly.moly_encrypt(b"")))
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 2031, USER_ID, 0)
        assert struct.unpack(">II", moly.moly_decrypt(encrypted)) == (0, 99_999_900)

        connection.sendall(
            moly.packet(8990, USER_ID, moly.moly_encrypt(struct.pack(">I", 0)))
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 8990, USER_ID, 0)
        knight = moly.moly_decrypt(encrypted)
        assert len(knight) == 84
        assert struct.unpack(">II", knight[:8]) == (USER_ID, 1)

        for command, expected in (
            (1915, struct.pack(">I", 0)),
            (8853, struct.pack(">II", 0, 0)),
            (10303, struct.pack(">II", 27_000, 1)),
            (8975, struct.pack(">I", 2)),
        ):
            connection.sendall(moly.packet(command, USER_ID, moly.moly_encrypt(b"")))
            version, reply_command, user_id, result, encrypted = receive_packet(connection)
            assert (version, reply_command, user_id, result) == (
                1, command, USER_ID, 0
            )
            assert moly.moly_decrypt(encrypted) == expected

        connection.sendall(
            moly.packet(402, USER_ID, moly.moly_encrypt(b""))
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 402, USER_ID, 0)
        assert moly.moly_decrypt(encrypted) == struct.pack(">II", 1, USER_ID)

        destination = struct.pack(">IIIIII", 2, 0, 1, 0, 0, 0)
        connection.sendall(
            moly.packet(401, USER_ID, moly.moly_encrypt(destination))
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 401, USER_ID, 0)
        entered = moly.moly_decrypt(encrypted)
        assert len(entered) == 219
        assert struct.unpack(">II", entered[40:48]) == (2, 0)

        connection.sendall(
            moly.packet(
                511,
                USER_ID,
                moly.moly_encrypt(
                    struct.pack(">IIIB", USER_ID, 160_191, 160_192, 2)
                ),
            )
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 511, USER_ID, 0)
        assert moly.moly_decrypt(encrypted) == struct.pack(">II", USER_ID, 0)

        connection.sendall(
            moly.packet(
                11120,
                USER_ID,
                moly.moly_encrypt(struct.pack(">II", 1, 10_071)),
            )
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 11120, USER_ID, 0)
        assert moly.moly_decrypt(encrypted) == struct.pack(">III", 1, 10_071, 0)

        connection.sendall(
            moly.packet(3000, USER_ID, moly.moly_encrypt(b""))
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 3000, USER_ID, 0)
        assert moly.moly_decrypt(encrypted) == struct.pack(">I", 0)

        connection.sendall(
            moly.packet(317, USER_ID, moly.moly_encrypt(b""))
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 317, USER_ID, 0)
        assert moly.moly_decrypt(encrypted) == struct.pack(">H", 0)

        connection.sendall(
            moly.packet(1408, USER_ID, moly.moly_encrypt(struct.pack(">I", 62)))
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 1408, USER_ID, 0)
        assert moly.moly_decrypt(encrypted) == struct.pack(">I", 0)

        connection.sendall(
            moly.packet(
                1243,
                USER_ID,
                moly.moly_encrypt(struct.pack(">III", 61, 1, 1)),
            )
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 1243, USER_ID, 0)
        assert moly.moly_decrypt(encrypted) == struct.pack(">II", 61, 0)

        connection.sendall(
            moly.packet(406, USER_ID, moly.moly_encrypt(struct.pack(">II", 2, 0)))
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 406, USER_ID, 0)
        assert struct.unpack(">II", moly.moly_decrypt(encrypted)[:8]) == (2, 0)

        connection.sendall(
            moly.packet(
                11009,
                USER_ID,
                moly.moly_encrypt(struct.pack(">II", 1, 11)),
            )
        )
        version, command, user_id, result, encrypted = receive_packet(connection)
        assert (version, command, user_id, result) == (1, 11009, USER_ID, 0)
        assert moly.moly_decrypt(encrypted) == struct.pack(">II", 1, 5)

    print("probe server smoke test: OK")


if __name__ == "__main__":
    main()
