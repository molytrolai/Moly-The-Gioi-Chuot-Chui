import socket
import struct
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))
import moly_probe_server as moly

def send_recv_moly(sock: socket.socket, cmd: int, user_id: int, body: bytes = b""):
    pkt = moly.packet(cmd, user_id, body)
    sock.sendall(pkt)
    hdr = sock.recv(17)
    if len(hdr) < 17:
        raise RuntimeError(f"Header truncated for cmd {cmd}")
    length, ver, r_cmd, r_uid, err = struct.unpack(">IBIII", hdr)
    body_len = length - 17
    r_body = b""
    while len(r_body) < body_len:
        chunk = sock.recv(body_len - len(r_body))
        if not chunk:
            break
        r_body += chunk
    return ver, r_cmd, r_uid, err, r_body

def main():
    print("Testing TCP Server Logins (Admin 0 and Player Random ID)...")

    # 1. Admin 0 Directory Login (Port 1863)
    with socket.create_connection(("127.0.0.1", 1863), timeout=3.0) as s:
        # Directory login cmd 103
        pwd_hash = b"*".ljust(32, b"\0")
        _, cmd, uid, err, body = send_recv_moly(s, 103, 0, pwd_hash)
        assert cmd == 103 and err == 0
        flag = struct.unpack(">I", body[:4])[0]
        assert flag == 0, f"Admin 0 login flag={flag}"
        print("  [PASS] 1. Admin 0 TCP Directory Login: OK (flag=0)")

    # 2. Admin 0 World Server Login (Port 3200)
    with socket.create_connection(("127.0.0.1", 3200), timeout=3.0) as s:
        _, cmd, uid, err, body = send_recv_moly(s, 201, 0, b"MOLYLOCALSESSION")
        assert cmd == 201 and err == 0
        print("  [PASS] 2. Admin 0 TCP World Server Login: OK (cmd=201)")

        # Map enter (cmd 401)
        req401 = moly.moly_encrypt(struct.pack(">IIII", 1, 0, 0, 0))
        _, cmd401, _, _, b401 = send_recv_moly(s, 401, 0, req401)
        assert cmd401 == 401
        print("  [PASS] 3. Admin 0 Map Enter: OK (cmd=401, user_id=0)")

    print("\n>>> ALL TCP TESTS PASSED FOR ADMIN 0! <<<")

if __name__ == "__main__":
    main()
