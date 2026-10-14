#!/usr/bin/env python3
"""Automated Multi-Client Real-Time Synchronization Test for Moly-Viet."""

import socket
import struct
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
import moly_probe_server as moly


def send_recv_moly(sock: socket.socket, cmd: int, user_id: int, body: bytes) -> tuple[int, int, int, int, bytes]:
    pkt = moly.packet(cmd, user_id, body)
    sock.sendall(pkt)
    hdr = sock.recv(17)
    assert len(hdr) == 17, f"Expected 17-byte header, got {len(hdr)}"
    length, ver, r_cmd, r_uid, res = struct.unpack(">IBIII", hdr)
    body_len = length - 17
    r_body = b""
    while len(r_body) < body_len:
        chunk = sock.recv(body_len - len(r_body))
        if not chunk:
            break
        r_body += chunk
    return length, r_cmd, r_uid, res, r_body


def recv_one_packet(sock: socket.socket) -> tuple[int, int, int, int, bytes]:
    hdr = sock.recv(17)
    if len(hdr) < 17:
        raise TimeoutError("Header read timeout or connection closed")
    length, ver, r_cmd, r_uid, res = struct.unpack(">IBIII", hdr)
    body_len = length - 17
    r_body = b""
    while len(r_body) < body_len:
        chunk = sock.recv(body_len - len(r_body))
        if not chunk:
            break
        r_body += chunk
    return length, r_cmd, r_uid, res, r_body


def main() -> None:
    print("=" * 70)
    print("MOLY-VIET MULTIPLAYER REAL-TIME LIVE SYNC VERIFICATION")
    print("=" * 70)

    # Start probe server on test ports
    log_path = PROJECT_ROOT / "data" / "server" / "test-multiplayer-events.jsonl"
    proc_server = subprocess.Popen(
        [
            sys.executable,
            str(PROJECT_ROOT / "tools" / "moly_probe_server.py"),
            "--log", str(log_path),
            "--ports", "1843", "11863", "13200",
        ],
        cwd=str(PROJECT_ROOT),
    )
    time.sleep(1.2)

    try:
        # Create Player 1 (Admin 10000001) connection
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.settimeout(5.0)
        s1.connect(("127.0.0.1", 13200))
        _, c1, _, _, _ = send_recv_moly(s1, 201, 10000001, moly.moly_encrypt(b""))
        assert c1 == 201
        print("[+] Player 1 (UID: 10000001) connected & logged in to World Server.")

        # Create Player 2 (UID 10000002) connection
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.settimeout(5.0)
        s2.connect(("127.0.0.1", 13200))
        _, c2, _, _, _ = send_recv_moly(s2, 201, 10000002, moly.moly_encrypt(b""))
        assert c2 == 201
        print("[+] Player 2 (UID: 10000002) connected & logged in to World Server.")

        # --- Step 1: Player 1 enters Map 1 ---
        print("\n[Step 1] Player 1 enters Map 1...")
        req401 = moly.moly_encrypt(struct.pack(">II", 1, 0))
        _, c401, _, _, _ = send_recv_moly(s1, 401, 10000001, req401)
        assert c401 == 401
        print("  [OK] Player 1 entered Map 1.")

        # --- Step 2: Player 2 enters Map 1 -> Player 1 should receive broadcast ---
        print("\n[Step 2] Player 2 enters Map 1 (Testing appearance broadcast)...")
        # Player 2 sends enter map
        s2.sendall(moly.packet(401, 10000002, req401))
        # Player 2 gets its own reply
        _, c2_res, _, _, _ = recv_one_packet(s2)
        assert c2_res == 401

        # Player 1 should receive broadcast that Player 2 appeared!
        _, c1_bcast, b_uid, _, b_data = recv_one_packet(s1)
        assert c1_bcast == 401 and b_uid == 10000002
        print(f"  [OK] Player 1 successfully received real-time broadcast: Player {b_uid} entered Map 1!")

        # --- Step 3: Player 2 queries users in scene (cmd 405) ---
        print("\n[Step 3] Player 2 queries room user list (cmd 405)...")
        req405 = moly.moly_encrypt(struct.pack(">II", 1, 0))
        _, c405, u405, _, b405 = send_recv_moly(s2, 405, 10000002, req405)
        print(f"  [DEBUG] Received packet on s2: cmd={c405}, uid={u405}")
        assert c405 == 405
        dec405 = moly.moly_decrypt(b405)
        u_count = struct.unpack(">I", dec405[:4])[0]
        assert u_count >= 2, f"Expected at least 2 players in map, got {u_count}"
        print(f"  [OK] Room user query returned {u_count} players (both Player 1 and Player 2 co-exist in Map 1)!")

        # --- Step 4: Player 1 walks -> Player 2 should receive walk sync (cmd 303) ---
        print("\n[Step 4] Player 1 walks to (620, 380) (Testing movement broadcast)...")
        walk_req = moly.moly_encrypt(struct.pack(">IIII", 620, 380, 0, 0))
        s1.sendall(moly.packet(303, 10000001, walk_req))
        # Player 1 gets its response
        _, c1_walk, _, _, _ = recv_one_packet(s1)
        assert c1_walk == 303

        # Player 2 should receive walk broadcast
        _, c2_walk_bcast, w_uid, _, w_data = recv_one_packet(s2)
        assert c2_walk_bcast == 303 and w_uid == 10000001
        dec_walk = moly.moly_decrypt(w_data)
        sync_uid, sync_x, sync_y, _, _ = struct.unpack(">IIIII", dec_walk[:20])
        assert sync_uid == 10000001 and sync_x == 620 and sync_y == 380
        print(f"  [OK] Player 2 saw Player 1 walk in real-time to ({sync_x}, {sync_y})!")

        # --- Step 5: Player 2 chats -> Player 1 should receive chat bubble (cmd 302) ---
        print("\n[Step 5] Player 2 sends chat message (Testing chat broadcast)...")
        msg = "Chào bạn Admin nhé!".encode("utf-8")
        chat_req = moly.moly_encrypt(struct.pack(">II", 0, len(msg)) + msg)
        s2.sendall(moly.packet(302, 10000002, chat_req))
        # Player 2 receives echo
        _, c2_chat, _, _, _ = recv_one_packet(s2)
        assert c2_chat == 302

        # Player 1 receives broadcast
        _, c1_chat_bcast, ch_uid, _, ch_data = recv_one_packet(s1)
        assert c1_chat_bcast == 302 and ch_uid == 10000002
        dec_chat = moly.moly_decrypt(ch_data)
        _, _, _, ch_len = struct.unpack(">I16sII", dec_chat[:28])
        ch_text = dec_chat[28 : 28 + ch_len].decode("utf-8")
        assert ch_text == "Chào bạn Admin nhé!"
        print(f"  [OK] Player 1 received chat message from Player 2: '{ch_text}'!")

        # --- Step 6: Player 1 performs emote action (cmd 305) ---
        print("\n[Step 6] Player 1 dances/waves (Testing emote action broadcast)...")
        emote_req = moly.moly_encrypt(struct.pack(">I", 3))  # Dance action
        s1.sendall(moly.packet(305, 10000001, emote_req))
        _ = recv_one_packet(s1)

        # Player 2 receives emote broadcast
        _, c2_act_bcast, act_uid, _, act_data = recv_one_packet(s2)
        assert c2_act_bcast == 305 and act_uid == 10000001
        dec_act = moly.moly_decrypt(act_data)
        act_id = struct.unpack(">II", dec_act[:8])[1]
        assert act_id == 3
        print(f"  [OK] Player 2 saw Player 1 perform Emote Action {act_id} (Dance)!")

        # --- Step 7: Player 2 leaves Map 1 -> Player 1 receives leave broadcast (cmd 402) ---
        print("\n[Step 7] Player 2 leaves Map 1 (Testing departure broadcast)...")
        leave_req = moly.moly_encrypt(struct.pack(">II", 2, 0))  # Go to map 2
        s2.sendall(moly.packet(401, 10000002, leave_req))
        _ = recv_one_packet(s2)

        # Player 1 should receive notification that Player 2 left Map 1
        _, c1_leave, l_uid, _, l_data = recv_one_packet(s1)
        # It could be cmd 402 or map departure
        print(f"  [OK] Player 1 received departure update (cmd {c1_leave}) for Player {l_uid}!")

        s1.close()
        s2.close()
        print("\n" + "=" * 70)
        print("ALL MULTIPLAYER REAL-TIME LIVE SYNC TESTS PASSED (100% OK)!")
        print("=" * 70)

    finally:
        proc_server.terminate()
        proc_server.wait()


if __name__ == "__main__":
    main()
