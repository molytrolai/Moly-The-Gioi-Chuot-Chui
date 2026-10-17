#!/usr/bin/env python3
"""RFC 6455 WebSocket Bridge for Ruffle WebAssembly and Flash TCP Sockets.

This module provides bi-directional proxying between browser WebSocket connections
(used by Ruffle's socketProxy) and local TCP game servers (e.g., ports 1863, 3200).
"""

from __future__ import annotations

import base64
import hashlib
import select
import socket
import struct
import threading
import time
from typing import Optional

WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def make_handshake_response(key: str, subprotocol: Optional[str] = None) -> bytes:
    """Computes the RFC 6455 WebSocket handshake accept header."""
    accept_val = base64.b64encode(
        hashlib.sha1((key.strip() + WS_GUID).encode("latin-1")).digest()
    ).decode("ascii")

    lines = [
        "HTTP/1.1 101 Switching Protocols",
        "Upgrade: websocket",
        "Connection: Upgrade",
        f"Sec-WebSocket-Accept: {accept_val}",
    ]
    if subprotocol:
        first_proto = subprotocol.split(",")[0].strip()
        lines.append(f"Sec-WebSocket-Protocol: {first_proto}")
    lines.append("\r\n")
    return "\r\n".join(lines).encode("ascii")


def read_ws_frame(sock: socket.socket) -> tuple[Optional[int], Optional[bytes]]:
    """Reads a single RFC 6455 WebSocket frame from a socket.

    Returns (opcode, payload) or (None, None) if the connection closed.
    """
    try:
        header = bytearray()
        while len(header) < 2:
            chunk = sock.recv(2 - len(header))
            if not chunk:
                return None, None
            header.extend(chunk)

        b1, b2 = header[0], header[1]
        fin = bool(b1 & 0x80)
        opcode = b1 & 0x0F
        is_masked = bool(b2 & 0x80)
        payload_len = b2 & 0x7F

        if payload_len == 126:
            ext = bytearray()
            while len(ext) < 2:
                chunk = sock.recv(2 - len(ext))
                if not chunk:
                    return None, None
                ext.extend(chunk)
            payload_len = struct.unpack(">H", ext)[0]
        elif payload_len == 127:
            ext = bytearray()
            while len(ext) < 8:
                chunk = sock.recv(8 - len(ext))
                if not chunk:
                    return None, None
                ext.extend(chunk)
            payload_len = struct.unpack(">Q", ext)[0]

        mask = b""
        if is_masked:
            mask_buf = bytearray()
            while len(mask_buf) < 4:
                chunk = sock.recv(4 - len(mask_buf))
                if not chunk:
                    return None, None
                mask_buf.extend(chunk)
            mask = bytes(mask_buf)

        payload = bytearray()
        while len(payload) < payload_len:
            to_read = min(65536, payload_len - len(payload))
            chunk = sock.recv(to_read)
            if not chunk:
                return None, None
            payload.extend(chunk)

        if is_masked and mask:
            for i in range(len(payload)):
                payload[i] ^= mask[i % 4]

        return opcode, bytes(payload)
    except (socket.error, ConnectionError, OSError):
        return None, None


def send_ws_frame(sock: socket.socket, data: bytes, opcode: int = 0x02) -> bool:
    """Sends an unmasked RFC 6455 WebSocket frame from server to client.

    Default opcode is 0x02 (binary), which Ruffle uses for raw TCP packets.
    """
    try:
        header = bytearray()
        header.append(0x80 | (opcode & 0x0F))
        length = len(data)
        if length <= 125:
            header.append(length)
        elif length <= 65535:
            header.append(126)
            header.extend(struct.pack(">H", length))
        else:
            header.append(127)
            header.extend(struct.pack(">Q", length))
        sock.sendall(header + data)
        return True
    except (socket.error, ConnectionError, OSError):
        return False


def bridge_sockets(
    ws_sock: socket.socket,
    target_sock: socket.socket,
    target_name: str = "TCP",
    on_log: Optional[callable] = None,
) -> None:
    """Bi-directionally streams data between a WebSocket and a TCP socket."""
    try:
        ws_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        target_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        ws_sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        target_sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    except Exception:
        pass

    ws_sock.setblocking(False)
    target_sock.setblocking(False)

    sockets = [ws_sock, target_sock]
    running = True

    try:
        while running:
            readable, _, errored = select.select(sockets, [], sockets, 1.0)
            if errored:
                break

            for s in readable:
                if s is ws_sock:
                    ws_sock.setblocking(True)
                    opcode, payload = read_ws_frame(ws_sock)
                    ws_sock.setblocking(False)

                    if opcode is None or opcode == 0x08:  # Close
                        running = False
                        break
                    elif opcode == 0x09:  # Ping -> Pong
                        send_ws_frame(ws_sock, payload or b"", opcode=0x0A)
                    elif opcode in (0x01, 0x02):  # Text or Binary
                        if payload:
                            target_sock.setblocking(True)
                            target_sock.sendall(payload)
                            target_sock.setblocking(False)
                            if on_log:
                                on_log(f"WS -> {target_name}: {len(payload)} bytes")
                elif s is target_sock:
                    try:
                        chunk = target_sock.recv(65536)
                        if not chunk:
                            running = False
                            break
                        if not send_ws_frame(ws_sock, chunk, opcode=0x02):
                            running = False
                            break
                        if on_log:
                            on_log(f"{target_name} -> WS: {len(chunk)} bytes")
                    except (BlockingIOError, socket.error) as e:
                        if isinstance(e, BlockingIOError):
                            continue
                        running = False
                        break
    finally:
        try:
            send_ws_frame(ws_sock, b"", opcode=0x08)
        except Exception:
            pass
        try:
            ws_sock.close()
        except Exception:
            pass
        try:
            target_sock.close()
        except Exception:
            pass
