#!/usr/bin/env python3
"""Isolated TCP recorder for discovering the Moly client protocol.

The recorder does not authenticate against or forward to official servers.
It logs incoming local test packets on E so protocol replies can be
implemented incrementally.
"""

from __future__ import annotations

import argparse
import json
import socket
import socketserver
import struct
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


POLICY = (
    b'<?xml version="1.0"?>'
    b'<cross-domain-policy>'
    b'<allow-access-from domain="*" to-ports="1863,3200" />'
    b'</cross-domain-policy>\0'
)
SESSION = b"MOLYLOCALSESSION"
MOLY_KEY = b"^FStx,wl6NquAVRF@f%6"
# The native client cipher walks indices 0..20 and then reuses index 0.
# Index 20 is the C string terminator, hence this 22-byte cycle.
MOLY_KEY_CYCLE = MOLY_KEY + b"\0" + MOLY_KEY[:1]
KNOWN_ONE_WAY_COMMANDS = {303, 305, 9245, 12053}
PROJECT_ROOT = Path(__file__).resolve().parents[1]
try:
    from account_system import accounts, DEFAULT_MOLY_ADMIN_ID, SUPER_LAMU_SPECIES
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from account_system import accounts, DEFAULT_MOLY_ADMIN_ID, SUPER_LAMU_SPECIES

DEFAULT_ACCOUNT = {
    "nickname": "Moly Viet",
    "color": 1,
    "vip_flags": 0,
    "vip_level": 0,
    "vip_month": 0,
    "vip_value": 0,
    "vip_end": 0,
    "gold_beans": 0,
    "element_knight_type": 0,
    "element_knight_talent": 1,
}


def fixed_text(value: object, size: int) -> bytes:
    return str(value).encode("utf-8")[:size].ljust(size, b"\0")


def account_profile(user_id: int) -> dict[str, object]:
    acc = accounts.get_account(user_id)
    if acc:
        accounts.check_vip_status(user_id)
        return accounts.get_account(user_id) or acc
    profile = dict(DEFAULT_ACCOUNT)
    return profile


def packet(
    cmd: int,
    user_id: int,
    body: bytes = b"",
    error: int = 0,
    version: int = 1,
) -> bytes:
    return struct.pack(">IBIII", 17 + len(body), version, cmd, user_id, error) + body


def moly_encrypt(clear: bytes) -> bytes:
    """Reimplement com.fcc.MEncrypt from TaomeeCoreDLL."""
    mixed = bytes(
        value ^ MOLY_KEY_CYCLE[index % len(MOLY_KEY_CYCLE)]
        for index, value in enumerate(clear)
    )
    if not mixed:
        return b"\x03"
    encrypted = bytearray(len(mixed) + 1)
    encrypted[0] = ((mixed[0] << 5) & 0xFF) | 3
    for index in range(1, len(mixed)):
        encrypted[index] = ((mixed[index] << 5) & 0xFF) | (mixed[index - 1] >> 3)
    encrypted[-1] = mixed[-1] >> 3
    return bytes(encrypted)


def moly_decrypt(encrypted: bytes) -> bytes:
    """Reimplement com.fcc.MDecrypt from TaomeeCoreDLL."""
    if len(encrypted) < 1:
        return b""
    clear = bytearray(len(encrypted) - 1)
    for index in range(len(clear)):
        value = ((encrypted[index] & 0xE0) >> 5) | (
            (encrypted[index + 1] << 3) & 0xFF
        )
        clear[index] = value ^ MOLY_KEY_CYCLE[index % len(MOLY_KEY_CYCLE)]
    return bytes(clear)


def auth_code_response(user_id: int) -> bytes:
    """Command 101: 0 indicates no captcha required for directory login."""
    return packet(101, user_id, struct.pack(">I", 0))


def login_response(user_id: int, request_body: bytes = b"") -> bytes:
    """Handle directory login (cmd 103) with local authentication."""
    actual_uid = user_id
    if user_id == 0 and len(request_body) >= 64:
        identifier = request_body[:64].decode("utf-8", errors="ignore").rstrip("\0").strip()
        acc = accounts.get_account_by_identifier(identifier)
        if acc:
            actual_uid = int(acc["user_id"])
        elif identifier in ("0", "00000000", "admin"):
            actual_uid = 0

    if len(request_body) >= 32:
        pwd_offset = 64 if (user_id == 0 and len(request_body) >= 96) else 0
        pwd_hash = request_body[pwd_offset : pwd_offset + 32].decode("ascii", errors="ignore")
        ok, _ = accounts.authenticate(actual_uid, pwd_hash)
        if not ok:
            # Flag 1 = Password incorrect
            return packet(103, actual_uid, struct.pack(">I", 1) + b"\0" * 16)

    return packet(103, actual_uid, struct.pack(">I", 0) + SESSION)


def create_mole_response(user_id: int, request_body: bytes = b"") -> bytes:
    """Command 107: create character / set initial nickname."""
    if len(request_body) >= 32:
        nick = request_body[16:32].decode("utf-8", errors="ignore").rstrip("\0")
        if nick:
            accounts.update_account(user_id, {"nickname": nick})
    return packet(107, user_id, struct.pack(">I", 0))


def server_info() -> bytes:
    ip = b"127.0.0.1".ljust(16, b"\0")
    return struct.pack(">II16sHI", 1, 1, ip, 3200, 0)


def recommended_servers_response(user_id: int) -> bytes:
    body = struct.pack(">I", 1) + server_info()
    body += struct.pack(">III", 1, 0, 0)
    return packet(105, user_id, body)


def all_servers_response(user_id: int) -> bytes:
    return packet(106, user_id, struct.pack(">I", 1) + server_info())


def online_login_response(user_id: int, version: int) -> bytes:
    """Minimal command-201 profile accepted by LoginOnlineSreRes."""
    profile = account_profile(user_id)
    nickname = fixed_text(profile["nickname"], 16)
    body = bytearray()
    body += struct.pack(">I16s", user_id, nickname)
    body += struct.pack(">III", 0, 0, 0)  # parent and invite counts
    body += struct.pack(">III", int(profile["color"]), int(profile["vip_flags"]), 0)
    body += struct.pack(">IIIIIIIIIIII", 0, 25_000_000, 9999, 9999, 9999, 9999, 99_999_999, 9999, 9999, 9999, 9999, 0)
    body += struct.pack(">III", 0, 1, 0)  # dining level, map id, map type
    body += struct.pack(">BIBII", 0, 0, 0, 480, 280)
    body += struct.pack(">IIIIIIIII", 1, 0, 0, 0, int(profile["vip_level"]), int(profile["vip_month"]), int(profile["vip_value"]), int(profile["vip_end"]), 0)
    body += struct.pack(">I16sI", 0, b"".ljust(16, b"\0"), 0)
    body += struct.pack(">I", 7200)
    body += b"\0" * 32
    body += b"\0"  # zero starter items
    if len(body) != 215:
        raise AssertionError(f"unexpected command-201 body size: {len(body)}")
    return packet(201, user_id, moly_encrypt(bytes(body)), version=version)


def scene_user_record(
    user_id: int,
    map_id: int = 1,
    map_type: int = 0,
    xpos: int = 480,
    ypos: int = 280,
) -> bytes:
    """Build the player record shared by commands 401 and 405."""
    profile = account_profile(user_id)
    nickname = fixed_text(profile["nickname"], 16)
    clothes = accounts.get_clothes(user_id)
    lamu = accounts.get_lamu(user_id)
    is_super = bool(lamu.get("is_super_lamu") or int(profile.get("vip_level", 0)) > 0)
    following = bool(lamu.get("following", True))

    if following and lamu:
        pet_id = int(lamu.get("id", 1))
        pet_nick = fixed_text(str(lamu.get("name", "Bé LaMu")), 16)
        stype = str(lamu.get("super_type", "classic"))
        spec_info = SUPER_LAMU_SPECIES.get(stype, SUPER_LAMU_SPECIES["classic"])
        pet_color = int(lamu.get("color", spec_info.get("color", 1)))
        pet_cloth = int(lamu.get("cloth_id", spec_info.get("cloth_id", 0)))
        pet_level = 101 if is_super else int(lamu.get("level", 1))
        pet_honor = 0
        can_fly = 1 if is_super else 0
    else:
        pet_id = 0
        pet_nick = b"".ljust(16, b"\0")
        pet_color = 0
        pet_level = 0
        pet_cloth = 0
        pet_honor = 0
        can_fly = 0

    record = bytearray(struct.pack(">I16s", user_id, nickname))
    record += struct.pack(">IIIIIII", 0, 0, 0, int(profile["color"]), int(profile["vip_flags"]), map_id, map_type)
    record += struct.pack(">BIBI", 0, 0, 0, 1)
    record += struct.pack(">IIIII", xpos, ypos, 0, 0, pet_id)
    record += struct.pack(">16sIB", pet_nick, pet_color, pet_level)
    record += struct.pack(">IIIIIII", 0, 0, 0, 0, 0, 0, 0)
    record += struct.pack(">BBBIII", 0, 0, 0, pet_cloth, pet_honor, can_fly)
    record += b"\0" * 32  # activity bit field
    record += struct.pack(">I16sIIII", 0, b"".ljust(16, b"\0"), 0, 0, 0, 0)
    # Role / animal_nbr, clothes count, clothes IDs, and guide state
    record += struct.pack(">IB", 0, len(clothes))
    for cid in clothes:
        record += struct.pack(">I", cid)
    record += struct.pack(">I", 0)  # guide state
    expected_len = 219 + 4 * len(clothes)
    if len(record) != expected_len:
        raise AssertionError(f"unexpected scene-user record size: {len(record)} (expected {expected_len})")
    return bytes(record)


def user_detail_record(target_uid: int) -> bytes:
    """Build the comprehensive profile card record for cmd 204."""
    prof = account_profile(target_uid)
    nickname = fixed_text(prof.get("nickname", "Moly"), 16)
    clothes = accounts.get_clothes(target_uid)
    color = int(prof.get("color", 1))
    vip_flags = int(prof.get("vip_flags", 0))
    vip_level = int(prof.get("vip_level", 0))
    vip_month = int(prof.get("vip_month", 0))
    vip_value = int(prof.get("vip_value", 0))
    vip_end = int(prof.get("vip_end", 0))

    rec = bytearray(struct.pack(">I16s", target_uid, nickname))
    rec += struct.pack(">IIIII", 0, 0, 0, color, vip_flags)
    rec += struct.pack(
        ">IIIIIIIIIIIIIIIIII",
        0, 25_000_000, 9999, 9999, 9999, 9999, 99_999_999, 9999, 9999,
        9999, 9999, 0, 0, vip_level, vip_month, vip_value, vip_end, 0,
    )
    rec += struct.pack(">II", 1, 0)
    rec += struct.pack(">BIBIII", 0, 0, 0, 480, 280, 0)
    rec += b"\0" * 32
    rec += struct.pack(">I16sI", 0, b"".ljust(16, b"\0"), 0)
    rec += struct.pack(">IIII", 0, 0, 0, 0)
    rec += struct.pack("B", len(clothes))
    for cid in clothes:
        rec += struct.pack(">I", cid)
    rec += struct.pack(">I", 0)
    return bytes(rec)


class WorldHub:
    """Manages active online sessions, map rooms, and real-time multiplayer broadcasts."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._handlers: set[Handler] = set()
        self._users: dict[int, Handler] = {}
        self._map_rooms: dict[int, set[Handler]] = {}

    def register(self, handler: Handler) -> None:
        with self._lock:
            self._handlers.add(handler)

    def unregister(self, handler: Handler) -> None:
        with self._lock:
            self._handlers.discard(handler)
            if handler.user_id in self._users:
                self._users.pop(handler.user_id, None)
            if handler.map_id in self._map_rooms:
                self._map_rooms[handler.map_id].discard(handler)
                if not self._map_rooms[handler.map_id]:
                    del self._map_rooms[handler.map_id]

    def set_user(self, handler: Handler, user_id: int) -> None:
        with self._lock:
            handler.user_id = user_id
            self._users[user_id] = handler

    def enter_map(self, handler: Handler, map_id: int, map_type: int = 0) -> None:
        with self._lock:
            old_map = handler.map_id
            if old_map in self._map_rooms:
                self._map_rooms[old_map].discard(handler)
            handler.map_id = map_id
            handler.map_type = map_type
            self._map_rooms.setdefault(map_id, set()).add(handler)

    def get_users_in_map(self, map_id: int) -> list[Handler]:
        with self._lock:
            return [h for h in self._map_rooms.get(map_id, set()) if getattr(h, "is_alive", False) and h.user_id is not None and h.user_id >= 0]

    def broadcast_to_map(
        self,
        map_id: int,
        packet_bytes: bytes,
        exclude_handler: Optional[Handler] = None,
    ) -> None:
        targets: list[Handler] = []
        with self._lock:
            for h in self._map_rooms.get(map_id, set()):
                if h is not exclude_handler and getattr(h, "is_alive", False) and h.user_id is not None and h.user_id >= 0:
                    targets.append(h)
        for h in targets:
            try:
                h.send_raw(packet_bytes)
            except Exception:
                pass

    def is_online(self, user_id: int) -> bool:
        with self._lock:
            return user_id in self._users

    def get_online_count(self) -> int:
        with self._lock:
            return len(self._users)


world_hub = WorldHub()


def scene_users_body(
    user_id: int,
    map_id: int = 1,
    map_type: int = 0,
    xpos: int = 480,
    ypos: int = 280,
) -> bytes:
    """Build the scene list containing all players currently in the map."""
    peers = world_hub.get_users_in_map(map_id)
    has_self = any(p.user_id == user_id for p in peers)
    records = [
        scene_user_record(p.user_id, map_id, map_type, p.xpos, p.ypos)
        for p in peers
    ]
    if not has_self and user_id is not None and user_id >= 0:
        records.append(scene_user_record(user_id, map_id, map_type, xpos, ypos))
    if not records:
        records.append(scene_user_record(user_id, map_id, map_type, xpos, ypos))
    return struct.pack(">I", len(records)) + b"".join(records)


def world_response(
    cmd: int,
    user_id: int,
    version: int,
    request_body: bytes,
) -> bytes | None:
    """Return safe, minimal payloads required while the world starts up."""
    body: bytes
    if cmd == 11010:  # initialize extended player state
        body = b""
    elif cmd == 3106:  # all NPC jobs: empty list
        body = struct.pack(">I", 0)
    elif cmd == 406:  # map metadata, echoing the requested destination
        map_id, map_type = (
            struct.unpack(">II", request_body[:8])
            if len(request_body) >= 8
            else (1, 0)
        )
        name = f"Moly Viet Map {map_id}".encode("ascii").ljust(64, b"\0")
        body = struct.pack(">II64sII", map_id, map_type, name, 0, 0)
    elif cmd == 6034:  # statistics acknowledgement
        body = b""
    elif cmd == 609:  # blacklist: empty list
        body = struct.pack(">I", 0)
    elif cmd == 10101:  # completion flag for the requested feature / task
        feature = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else 0
        tasks = accounts.get_tasks(user_id)
        status = int(tasks.get(str(feature), {}).get("status", 0))
        body = struct.pack(">II", feature, status)
    elif cmd == 2008:  # NPC ballot bit field
        body = b"\0" * 32
    elif cmd == 10301:  # server time: seconds and microseconds
        now = time.time()
        body = struct.pack(">II", int(now), int((now % 1) * 1_000_000))
    elif cmd == 8817:  # discontinued summer mini-game state
        body = struct.pack(">III", 0, 0, 0)
    elif cmd == 10302:  # VIP web session
        body = struct.pack(">I32s", int(time.time()), SESSION.ljust(32, b"\0"))
    elif cmd == 10303:  # VIP status query (strictly reflects account VIP)
        vip_status = accounts.check_vip_status(user_id)
        is_vip = 1 if vip_status.get("is_vip") else 0
        days_left = int(vip_status.get("days_left", 0))
        body = struct.pack(">II", days_left, is_vip)
    elif cmd == 426:  # external mini-game session bytes
        body = b"MOLYVIET-GAME-SESSION".ljust(32, b"\0")
    elif cmd == 8920:  # payment password is not enabled
        body = struct.pack(">I", 0)
    elif cmd == 8606:  # exchange state bitset and the queried type
        query_type = (
            struct.unpack(">I", request_body[:4])[0]
            if len(request_body) >= 4
            else 0
        )
        body = struct.pack(">II", 0, query_type)
    elif cmd == 8755:  # legacy activity status
        activity = (
            struct.unpack(">I", request_body[:4])[0]
            if len(request_body) >= 4
            else 0
        )
        body = struct.pack(">III", activity, 0, 0)
    elif cmd == 8974:  # no elemental-knight profession
        body = struct.pack(">I", int(account_profile(user_id)["element_knight_type"]))
    elif cmd == 8975:  # the admin profile already owns an element-knight class
        body = struct.pack(">I", 2)
    elif cmd == 8990:  # element-knight profile for the unrestricted test account
        profile = account_profile(user_id)
        knight_type = int(profile["element_knight_type"])
        if knight_type == 0:
            return None
        body = struct.pack(
            ">II16s",
            user_id, knight_type, fixed_text(profile["nickname"], 16),
        ) + struct.pack(
            ">IIIIIIIIIIIIII",
            25_000_000, 9999, 9999, int(profile["element_knight_talent"]),
            0, 9999, 9999, 9999, 9999, 9999, 0, 0, 1,
            0,
        ) + struct.pack(">I", 0)
    elif cmd == 12018:  # magic-spirit bag: empty list
        body = struct.pack(">I", 0)
    elif cmd == 11009:  # return one flag per requested limit id
        count = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else 0
        count = min(count, max(0, (len(request_body) - 4) // 4))
        limit_ids = [
            struct.unpack(">I", request_body[4 + index * 4 : 8 + index * 4])[0]
            for index in range(count)
        ]
        # Limit id 11 stores the obsolete Magic Spirit tutorial step.  Mark it
        # complete so a new local account reaches the normal map instead of a
        # server-backed tutorial that no longer exists.
        flags = [5 if limit_id == 11 else 0 for limit_id in limit_ids]
        body = struct.pack(">I", count) + b"".join(
            struct.pack(">I", flag) for flag in flags
        )
    elif cmd == 1328:  # 200-byte profession bitmap
        profs = accounts.get_professions(user_id)
        bitmap = bytearray(200)
        # Guide bit (1), Police bit (2), Journalist bit (4), Knight bit (8)
        val = 0
        if "guide" in profs:
            val |= 1
        if "police" in profs:
            val |= 2
        if "journalist" in profs:
            val |= 4
        if "knight" in profs:
            val |= 8
        bitmap[0] = val
        body = bytes(bitmap)
    elif cmd == 401:  # enter a map after the leave-map acknowledgement
        map_id, map_type = (
            struct.unpack(">II", request_body[:8])
            if len(request_body) >= 8
            else (1, 0)
        )
        body = scene_user_record(user_id, map_id, map_type)
    elif cmd == 402:  # confirm that the local player left the previous map
        body = struct.pack(">II", 1, user_id)
    elif cmd == 405:  # users currently in the requested scene
        map_id, map_type = (
            struct.unpack(">II", request_body[:8])
            if len(request_body) >= 8
            else (1, 0)
        )
        body = scene_users_body(user_id, map_id, map_type)
    elif cmd == 805:  # unread postcard count
        body = struct.pack(">I", 0)
    elif cmd == 802:  # get all postcards (TotalCnt=0, UnreadCnt=0, ReadCnt=0)
        body = struct.pack(">HHH", 0, 0, 0)
    elif cmd == 204:  # User detail / Profile card
        target_uid = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else user_id
        if target_uid == 0:
            target_uid = user_id
        body = user_detail_record(target_uid)
    elif cmd == 207:  # Get user basic info
        target_uid = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else user_id
        if target_uid == 0:
            target_uid = user_id
        prof = account_profile(target_uid)
        nick = fixed_text(prof.get("nickname", "Moly"), 16)
        color = int(prof.get("color", 1))
        vip = int(prof.get("vip_flags", 0))
        body = struct.pack(">I16sIIIIIIBI", target_uid, nick, color, 0, 0, vip, 1, 0, 0, 0)
    elif cmd == 606:  # Friend list (count: 0)
        body = struct.pack(">I", 0)
    elif cmd == 610:  # Friends online query (serverCount: 0)
        body = struct.pack(">H", 0)
    elif cmd == 6061:  # discontinued compensation state
        body = struct.pack(">I", 0)
    elif cmd == 9124:  # legacy reward list: empty
        body = struct.pack(">I", 0)
    elif cmd == 11019:  # one byte-valued bit-buffer flag per request
        count = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else 0
        count = min(count, max(0, (len(request_body) - 4) // 4))
        body = struct.pack(">I", count) + (b"\0" * count)
    elif cmd == 12004:  # minimal magic-spirit owner record, with no active team
        body = bytearray()
        body += struct.pack(">IBIIHIHHB", user_id, 1, 0, 100, 100, int(time.time()), 0, 10, 0)
        body += b"\0" * 100  # five teams, five uint32 slots each
        body = bytes(body)
    elif cmd == 216:  # task-state list from account storage
        tasks = accounts.get_tasks(user_id)
        if tasks:
            max_tid = max(max(int(k) for k in tasks.keys()) + 1, 672)
            task_bytes = bytearray(max_tid)
            for tid_str, tdata in tasks.items():
                try:
                    tid = int(tid_str)
                    if tid < max_tid:
                        task_bytes[tid] = int(tdata.get("status", 1))
                except ValueError:
                    pass
            body = struct.pack(">I", max_tid) + bytes(task_bytes)
        else:
            body = struct.pack(">I", 0)
    elif cmd == 228:  # pet learning record: no pet/classes
        body = struct.pack(">II", 0, 0)
    elif cmd == 232:  # Super Lamu pet active flag
        lamu = accounts.get_lamu(user_id)
        is_super = 1 if lamu.get("is_super_lamu") or int(account_profile(user_id).get("vip_level", 0)) > 0 else 0
        body = struct.pack("B", is_super)
    elif cmd == 233:  # Outside / following pets in map
        lamu = accounts.get_lamu(user_id)
        prof = account_profile(user_id)
        is_super = 1 if lamu.get("is_super_lamu") or int(prof.get("vip_level", 0)) > 0 else 0
        following = bool(lamu.get("following", True))
        if following and lamu:
            pet_id = int(lamu.get("id", 1))
            user_nick = fixed_text(prof.get("nickname", "Moly"), 16)
            pet_flag = 1 | (2 if is_super else 0)
            now_sec = int(time.time())
            birth = now_sec - 86400 * 30
            age = 30
            pet_nick = fixed_text(str(lamu.get("name", "Bé LaMu")), 16)
            stype = str(lamu.get("super_type", "classic"))
            spec_info = SUPER_LAMU_SPECIES.get(stype, SUPER_LAMU_SPECIES["classic"])
            color = int(lamu.get("color", spec_info.get("color", 1)))
            cloth_id = int(lamu.get("cloth_id", spec_info.get("cloth_id", 0)))
            hungry = int(lamu.get("hunger", 100))
            thirsty = int(lamu.get("thirsty", 100))
            sanitary = int(lamu.get("cleanliness", 100))
            spirit = int(lamu.get("mood", 100))
            level = 101 if is_super else int(lamu.get("level", 1))
            skill = 15 if is_super else 1
            pet_entry = struct.pack(
                ">II16sIII16sIBBBBBIIIIIIBBBII",
                pet_id,
                user_id,
                user_nick,
                pet_flag,
                birth,
                age,
                pet_nick,
                color,
                hungry, thirsty, sanitary, spirit,
                level,
                skill,
                0, 0, 0,
                0, 100,
                0, 0, 0,
                cloth_id,
                0
            )
            body = struct.pack(">I", 1) + pet_entry
        else:
            body = struct.pack(">I", 0)
    elif cmd == 2031:  # test purchases are accepted without consuming beans
        balance = min(int(account_profile(user_id)["gold_beans"]), 42_949_672)
        body = struct.pack(">II", 0, balance * 100)
    elif cmd == 2032:  # premium balance, encoded as hundredths
        balance = min(int(account_profile(user_id)["gold_beans"]), 42_949_672)
        body = struct.pack(">I", balance * 100)
    elif cmd == 2040:  # premium-shop login streak/score
        body = struct.pack(">III", 1, 0, 0)
    elif cmd == 6026:  # legacy 30-day login package: unavailable
        body = struct.pack(">II", 0, 0)
    elif cmd == 6024:  # normal login package: no pending daily rewards
        body = struct.pack(">IIIIII", 0, 0, 0, 0, 0, 0)
    elif cmd == 1496:  # pet class list: empty
        body = struct.pack(">I", 0)
    elif cmd == 1915:  # arbitrary inventory-item counts: none owned yet
        body = struct.pack(">I", 0)
    elif cmd == 8853:  # jeweler profession experience and level-step list
        body = struct.pack(">II", 0, 0)
    elif cmd == 511:  # inventory range query
        if len(request_body) >= 12:
            chk_uid, itm_start, itm_end = struct.unpack(">III", request_body[:12])
        else:
            chk_uid, itm_start, itm_end = (user_id, 0, 0xFFFFFFFF)
        inv = accounts.get_inventory(chk_uid)
        matched = [(itm, cnt) for itm, cnt in inv.items() if itm_start <= itm <= itm_end]
        matched_bytes = b"".join(struct.pack(">II", itm, cnt) for itm, cnt in matched)
        body = struct.pack(">II", chk_uid, len(matched)) + matched_bytes
    elif cmd == 317:  # random map pickups: none spawned
        body = struct.pack(">H", 0)
    elif cmd == 1408:  # map pet-skill eggs: empty list
        body = struct.pack(">I", 0)
    elif cmd == 3000:  # initialize the legacy knight-card book
        body = struct.pack(">I", 0)
    elif cmd == 1243:  # legacy exchange result: accepted, no item delta yet
        exchange_type = (
            struct.unpack(">I", request_body[:4])[0]
            if len(request_body) >= 4
            else 0
        )
        body = struct.pack(">II", exchange_type, 0)
    elif cmd == 11120:  # generic limit values requested by map activities
        count = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else 0
        count = min(count, max(0, (len(request_body) - 4) // 4))
        types = [
            struct.unpack(">I", request_body[4 + index * 4 : 8 + index * 4])[0]
            for index in range(count)
        ]
        body = struct.pack(">I", count) + b"".join(
            struct.pack(">II", value_type, 0) for value_type in types
        )
    elif cmd == 8081:  # persist a client buffer value
        body = b""
    elif cmd == 10011:  # time greeting state
        greeting_type = (
            struct.unpack(">I", request_body[:4])[0]
            if len(request_body) >= 4
            else 0
        )
        body = struct.pack(">III", greeting_type, 0, 0)
    elif cmd == 11014:  # magic-spirit friend list: empty
        body = struct.pack(">I", 0)
    elif cmd == 11023:  # magic-spirit tutorial update acknowledgement
        body = b""
    elif cmd == 302:  # player talk / chat broadcast
        if len(request_body) >= 8:
            recvrid, msglen = struct.unpack(">II", request_body[:8])
            mesg = request_body[8 : 8 + msglen]
            nick = fixed_text(account_profile(user_id)["nickname"], 16)
            body = struct.pack(">I16sII", user_id, nick, recvrid, len(mesg)) + mesg
        else:
            body = b""
    elif cmd == 303:  # player walk synchronization
        xpos, ypos, item, grid = (
            struct.unpack(">IIII", request_body[:16])
            if len(request_body) >= 16
            else (480, 280, 0, 0)
        )
        body = struct.pack(">IIIII", user_id, xpos, ypos, item, grid)
    elif cmd == 304:  # throw item (snowball, water balloon)
        body = struct.pack(">I", user_id) + request_body
    elif cmd == 305:  # player action / emote (dance, wave, sit)
        action_id = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else 0
        body = struct.pack(">II", user_id, action_id)
    elif cmd == 407:  # minigame score report (anti-cheat cap applied)
        rate, score, check_num = (
            struct.unpack(">III", request_body[:12])
            if len(request_body) >= 12
            else (100, 100, 0)
        )
        earned_beans = min(max(5, score // 10), 100)  # Capped at 100 Beans max per minigame session
        accounts.add_gold_beans(user_id, earned_beans)
        # Return 0 bonus items
        body = struct.pack(">I", 0)
    elif cmd == 501:  # buy item from shop (strict balance verification)
        item_id, count = (
            struct.unpack(">II", request_body[:8])
            if len(request_body) >= 8
            else (0, 1)
        )
        if count <= 0 or count > 99:
            count = 1
        cost = count * 10
        ok, remaining = accounts.deduct_gold_beans(user_id, cost)
        if ok:
            accounts.add_item(user_id, item_id, count)
            body = struct.pack(">I", min(remaining, 42_949_672))
        else:
            # Insufficient funds: return current balance without giving item
            body = struct.pack(">I", min(remaining, 42_949_672))
    elif cmd == 503:  # use / wear body clothes
        count = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else 0
        count = min(count, max(0, (len(request_body) - 4) // 4))
        clothes = [
            struct.unpack(">I", request_body[4 + idx * 4 : 8 + idx * 4])[0]
            for idx in range(count)
        ]
        accounts.set_clothes(user_id, clothes)
        # Server response: user_id (uint32) + count (uint32) + count * (item_id: uint32, dress_up: uint8 = 1)
        body = struct.pack(">II", user_id, len(clothes)) + b"".join(
            struct.pack(">IB", item_id, 1) for item_id in clothes
        )
    elif cmd == 507:  # item bag list query
        inv = accounts.get_inventory(user_id)
        clothes = accounts.get_clothes(user_id)
        all_items = list(set(list(inv.keys()) + clothes))
        count = min(len(all_items), 255)
        items_payload = b"".join(struct.pack(">I", itm) for itm in all_items[:count])
        body = struct.pack(">IB", user_id, count) + items_payload
    elif cmd == 409:  # Home info: style, cleanliness, level, decorations
        target_uid = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else user_id
        if target_uid == 0:
            target_uid = user_id
        prof = account_profile(target_uid)
        home_data = accounts.get_home(target_uid)
        nick_bytes = str(prof.get("nickname", "Moly")).encode("gbk", errors="replace")[:16].ljust(16, b"\0")
        is_online = 1 if world_hub.is_online(target_uid) else 0
        style_itm = int(home_data.get("style_item", 160001))
        cleanliness = int(home_data.get("cleanliness", 100))
        level = int(home_data.get("level", 1))
        decorations = home_data.get("decorations", [])
        body = struct.pack(">I16sIIHH8sI", target_uid, nick_bytes, is_online, style_itm, cleanliness, level, b"\0" * 8, len(decorations))
        for item in decorations:
            itm_id = item.get("item_id", 0) if isinstance(item, dict) else int(item)
            x = item.get("x", 100) if isinstance(item, dict) else 100
            y = item.get("y", 100) if isinstance(item, dict) else 100
            body += struct.pack(">IHH8s", itm_id, x, y, b"\0" * 8)
    elif cmd == 1301:  # Homeland farm info: background, decorations, and crops
        target_uid = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else user_id
        if target_uid == 0:
            target_uid = user_id
        prof = account_profile(target_uid)
        home_data = accounts.get_home(target_uid)
        nick_bytes = str(prof.get("nickname", "Moly")).encode("gbk", errors="replace")[:16].ljust(16, b"\0")
        is_online = 1 if world_hub.is_online(target_uid) else 0
        home_bg_itm = int(home_data.get("homeland_bg", 1230001))
        farm_decorations = home_data.get("homeland_decorations", [])
        farm_crops = home_data.get("farm_crops", [])
        body = struct.pack(">I16sIIII", target_uid, nick_bytes, is_online, home_bg_itm, len(farm_decorations), len(farm_crops))
        for item in farm_decorations:
            itm_id = item.get("item_id", 0) if isinstance(item, dict) else int(item)
            x = item.get("x", 100) if isinstance(item, dict) else 100
            y = item.get("y", 100) if isinstance(item, dict) else 100
            body += struct.pack(">IHH8s", itm_id, x, y, b"\0" * 8)
        now_ts = int(time.time())
        for idx, crop in enumerate(farm_crops, start=1):
            c_num = crop.get("number", idx)
            c_itemid = crop.get("itemid", 1230001)
            c_x = crop.get("x", 150 + idx * 50)
            c_y = crop.get("y", 200)
            c_val = crop.get("value", 50)
            c_sick = crop.get("sickflag", 0)
            c_fruit_num = crop.get("fruit_num", 5)
            c_status = crop.get("fruit_status", 3)
            c_mature = crop.get("mature_time", now_ts)
            diff_mature = max(0, c_mature - now_ts)
            c_rate = crop.get("cur_grow_rate", 100)
            c_earth = crop.get("earth", 100)
            c_pollinate = crop.get("pollinate_num", 0)
            c_thief = 0
            body += struct.pack(">IIHHIIIIIIIIII", c_num, c_itemid, c_x, c_y, c_val, c_sick, c_fruit_num, c_status, c_mature, diff_mature, c_rate, c_earth, c_pollinate, c_thief)
    elif cmd == 1304:  # Plant seed in Homeland
        bg_id, seed_id, px, py = struct.unpack(">IIII", request_body[:16]) if len(request_body) >= 16 else (1230001, 1230001, 200, 200)
        crop = accounts.plant_crop(user_id, seed_id, px, py)
        now_ts = int(time.time())
        c_num = crop.get("number", 1)
        c_itemid = crop.get("itemid", seed_id)
        c_x = crop.get("x", px)
        c_y = crop.get("y", py)
        c_val = crop.get("value", 10)
        c_sick = crop.get("sickflag", 0)
        c_fruit_num = crop.get("fruit_num", 5)
        c_status = crop.get("fruit_status", 1)
        c_mature = crop.get("mature_time", now_ts + 60)
        diff_mature = max(0, c_mature - now_ts)
        c_rate = crop.get("cur_grow_rate", 100)
        c_earth = crop.get("earth", 100)
        c_pollinate = 0
        c_thief = 0
        body = struct.pack(">IIHHIIIIIIIIII", c_num, c_itemid, c_x, c_y, c_val, c_sick, c_fruit_num, c_status, c_mature, diff_mature, c_rate, c_earth, c_pollinate, c_thief)
    elif cmd == 1306:  # Water plant in Homeland
        target_uid, crop_num = struct.unpack(">II", request_body[:8]) if len(request_body) >= 8 else (user_id, 1)
        accounts.water_crop(target_uid, crop_num)
        body = struct.pack(">I", 0)
    elif cmd == 1309:  # Harvest fruits in Homeland
        crop_num = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else 1
        itmid, count = accounts.harvest_crop(user_id, crop_num)
        body = struct.pack(">III", crop_num, itmid, count)
    elif cmd in {212, 240}:  # Get Lamu pet info (212=single/all, 240=all)
        target_uid = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else user_id
        if target_uid == 0:
            target_uid = user_id
        lamu = accounts.get_lamu(target_uid)
        prof = account_profile(target_uid)
        is_super = 1 if lamu.get("is_super_lamu") or int(prof.get("vip_level", 0)) > 0 else 0
        pet_id = int(lamu.get("id", 1))
        pet_flag = 1 | (2 if is_super else 0)
        now_sec = int(time.time())
        birth = now_sec - 86400 * 30
        age = 30
        nick = fixed_text(str(lamu.get("name", "Bé LaMu")), 16)
        stype = str(lamu.get("super_type", "classic"))
        spec_info = SUPER_LAMU_SPECIES.get(stype, SUPER_LAMU_SPECIES["classic"])
        color = int(lamu.get("color", spec_info.get("color", 1)))
        cloth_id = int(lamu.get("cloth_id", spec_info.get("cloth_id", 0)))
        sicktime = 0
        pos_x = 100
        pos_y = 100
        hungry = int(lamu.get("hunger", 100))
        thirsty = int(lamu.get("thirsty", 100))
        sanitary = int(lamu.get("cleanliness", 100))
        spirit = int(lamu.get("mood", 100))
        level = 101 if is_super else int(lamu.get("level", 1))
        skill = 15 if is_super else 1
        sick_type = 0
        pet_body = struct.pack(
            ">IIII16sIIBBBBBBBIIIIIIIBBBII",
            pet_id, pet_flag, birth, age, nick, color, sicktime,
            pos_x, pos_y, hungry, thirsty, sanitary, spirit, level,
            skill, sick_type, 0, 0, 0, 0, 100, 0, 0, 0, cloth_id, 0
        )
        body = struct.pack(">II", target_uid, 1) + pet_body
    elif cmd == 214:  # Get pet count
        target_uid = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else user_id
        if target_uid == 0:
            target_uid = user_id
        body = struct.pack(">II", target_uid, 1)
    elif cmd in {215, 251}:  # Follow pet (215) / Call Super Lamu (251)
        if len(request_body) >= 8:
            pet_id, status = struct.unpack(">II", request_body[:8])
            following = bool(status)
        elif len(request_body) >= 5:
            pet_id, p_type = struct.unpack(">IB", request_body[:5])
            following = bool(p_type)
        else:
            pet_id = 1
            following = True
        accounts.set_lamu_following(user_id, following)
        lamu = accounts.get_lamu(user_id)
        prof = account_profile(user_id)
        is_super = 1 if lamu.get("is_super_lamu") or int(prof.get("vip_level", 0)) > 0 else 0
        stype = str(lamu.get("super_type", "classic"))
        spec_info = SUPER_LAMU_SPECIES.get(stype, SUPER_LAMU_SPECIES["classic"])
        color = int(lamu.get("color", spec_info.get("color", 1)))
        cloth_id = int(lamu.get("cloth_id", spec_info.get("cloth_id", 0)))
        nick = fixed_text(str(lamu.get("name", "Bé LaMu")), 16)
        level = 101 if is_super else int(lamu.get("level", 1))
        skill = 15 if is_super else 1
        body = struct.pack(
            ">II16sIIBBBBBIIIIIIBBBII",
            user_id,
            pet_id,
            nick,
            color,
            1 if following else 0,
            int(lamu.get("hunger", 100)),
            int(lamu.get("thirsty", 100)),
            int(lamu.get("cleanliness", 100)),
            int(lamu.get("mood", 100)),
            level,
            skill,
            0, 0, 0,
            0, 100,
            0, 0, 0,
            cloth_id,
            0
        )
    elif cmd == 231:  # Become Super Lamu
        accounts.update_lamu(user_id, {"is_super_lamu": True})
        body = struct.pack("B", 1)
    elif cmd == 238:  # Modify pet color
        if len(request_body) >= 12:
            petid, new_color, itemid = struct.unpack(">III", request_body[:12])
        elif len(request_body) >= 8:
            petid, new_color = struct.unpack(">II", request_body[:8])
            itemid = 0
        else:
            petid, new_color, itemid = 1, 1, 0
        accounts.update_lamu(user_id, {"color": new_color})
        body = struct.pack(">IIIII", itemid, 0, 1, petid, new_color)
    elif cmd == 1121:  # Pet clothes use / wear
        if len(request_body) >= 8:
            petid, cloth_id = struct.unpack(">II", request_body[:8])
        else:
            petid, cloth_id = 1, 0
        accounts.update_lamu(user_id, {"cloth_id": cloth_id})
        body = struct.pack(">IIIIB", user_id, petid, 1, cloth_id, 1)
    elif cmd == 10304:  # Update VIP value & star level
        prof = account_profile(user_id)
        body = struct.pack(">II", int(prof.get("vip_value", 0)), int(prof.get("vip_level", 0)))
    elif cmd == 239:  # Send pet home
        pet_id = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else 1
        accounts.set_lamu_following(user_id, False)
        body = struct.pack(">II", user_id, pet_id)
    elif cmd == 218:  # Set pet nick
        pet_id = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else 1
        nick_raw = request_body[4:20] if len(request_body) >= 20 else b"B\xe9 LaMu".ljust(16, b"\0")
        try:
            nick_str = nick_raw.split(b"\0")[0].decode("gbk", errors="ignore")
        except Exception:
            nick_str = "Bé LaMu"
        accounts.set_lamu_nick(user_id, nick_str)
        body = struct.pack(">I16s", pet_id, nick_raw.ljust(16, b"\0"))
    elif cmd == 219:  # Play / feed pet
        pet_id = struct.unpack(">I", request_body[:4])[0] if len(request_body) >= 4 else 1
        accounts.feed_or_play_lamu(user_id)
        body = struct.pack(">IBB", pet_id, 100, 100)
    else:
        return None
    return packet(cmd, user_id, moly_encrypt(body), version=version)


class Recorder:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()

    def write(self, event: dict[str, object]) -> None:
        event["at"] = datetime.now(timezone.utc).isoformat()
        line = json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n"
        with self.lock:
            with self.path.open("a", encoding="utf-8", newline="") as stream:
                stream.write(line)
        print(line, end="", flush=True)


class ThreadedServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address: tuple[str, int], recorder: Recorder) -> None:
        self.recorder = recorder
        super().__init__(address, Handler)


class Handler(socketserver.BaseRequestHandler):
    def setup(self) -> None:
        self.is_alive = True
        self.user_id: int = 0
        self.map_id: int = 0
        self.map_type: int = 0
        self.xpos: int = 480
        self.ypos: int = 280
        self._send_lock = threading.Lock()

    def send_raw(self, data: bytes) -> None:
        with self._send_lock:
            self.request.sendall(data)

    def handle(self) -> None:
        server = self.server
        assert isinstance(server, ThreadedServer)
        port = server.server_address[1]
        peer_host, peer_port = self.client_address
        server.recorder.write(
            {"event": "connect", "port": port, "peer": f"{peer_host}:{peer_port}"}
        )
        if port == 3200:
            world_hub.register(self)
        self.request.settimeout(1 if port == 3200 else 30)
        buffer = b""
        try:
            while True:
                try:
                    data = self.request.recv(65536)
                except socket.timeout:
                    if port == 3200:
                        # World connections are persistent.  A quiet client is
                        # normal and must not be treated as disconnected.
                        continue
                    raise
                if not data:
                    break
                server.recorder.write(
                    {
                        "event": "data",
                        "port": port,
                        "peer": f"{peer_host}:{peer_port}",
                        "size": len(data),
                        "hex": data.hex(),
                    }
                )
                if port == 843 or b"<policy-file-request/>" in data:
                    self.send_raw(POLICY)
                    server.recorder.write(
                        {
                            "event": "send-policy",
                            "port": port,
                            "peer": f"{peer_host}:{peer_port}",
                            "size": len(POLICY),
                        }
                    )
                    continue

                buffer += data
                header_length = 17
                while len(buffer) >= 4:
                    frame_length = struct.unpack(">I", buffer[:4])[0]
                    if frame_length < header_length or frame_length > 4 * 1024 * 1024:
                        server.recorder.write(
                            {
                                "event": "invalid-frame",
                                "port": port,
                                "peer": f"{peer_host}:{peer_port}",
                                "declared_length": frame_length,
                            }
                        )
                        buffer = b""
                        break
                    if len(buffer) < frame_length:
                        break
                    frame, buffer = buffer[:frame_length], buffer[frame_length:]
                    length, version, cmd, user_id, result = struct.unpack(
                        ">IBIII", frame[:header_length]
                    )
                    server.recorder.write(
                        {
                            "event": "frame",
                            "port": port,
                            "peer": f"{peer_host}:{peer_port}",
                            "length": length,
                            "version": version,
                            "cmd": cmd,
                            "user_id": user_id,
                            "result": result,
                            "body_hex": frame[header_length:].hex(),
                        }
                    )

                    clear_body = None
                    if port == 3200 or cmd >= 200:
                        clear_body = moly_decrypt(frame[header_length:])
                        server.recorder.write(
                            {
                                "event": "decrypted-frame",
                                "port": port,
                                "peer": f"{peer_host}:{peer_port}",
                                "cmd": cmd,
                                "user_id": user_id,
                                "body_size": len(clear_body),
                                "body_hex": clear_body.hex(),
                            }
                        )

                    response = None
                    if cmd == 101:
                        response = auth_code_response(user_id)
                    elif cmd == 103:
                        response = login_response(user_id, frame[header_length:])
                    elif cmd == 105:
                        response = recommended_servers_response(user_id)
                    elif cmd == 106:
                        response = all_servers_response(user_id)
                    elif cmd == 107:
                        response = create_mole_response(user_id, frame[header_length:])
                    elif cmd == 201:
                        self.user_id = user_id
                        self.map_id = 0
                        world_hub.set_user(self, user_id)
                        response = online_login_response(user_id, version)
                    elif cmd == 401 and clear_body is not None:
                        map_id, map_type = (
                            struct.unpack(">II", clear_body[:8])
                            if len(clear_body) >= 8
                            else (1, 0)
                        )
                        if self.map_id > 0 and self.map_id != map_id:
                            leave_old = packet(
                                402,
                                user_id,
                                moly_encrypt(struct.pack(">II", self.map_id, user_id)),
                                version=version,
                            )
                            world_hub.broadcast_to_map(self.map_id, leave_old, exclude_handler=self)
                        world_hub.enter_map(self, map_id, map_type)
                        response = packet(
                            401,
                            user_id,
                            moly_encrypt(scene_user_record(user_id, map_id, map_type, self.xpos, self.ypos)),
                            version=version,
                        )
                        # Broadcast player appearance to all other players in this scene
                        world_hub.broadcast_to_map(map_id, response, exclude_handler=self)
                    elif cmd == 402:
                        response = packet(402, user_id, moly_encrypt(struct.pack(">II", self.map_id, user_id)), version=version)
                        world_hub.broadcast_to_map(self.map_id, response, exclude_handler=self)
                    elif cmd == 405 and clear_body is not None:
                        map_id, map_type = (
                            struct.unpack(">II", clear_body[:8])
                            if len(clear_body) >= 8
                            else (1, 0)
                        )
                        response = packet(
                            405,
                            user_id,
                            moly_encrypt(scene_users_body(user_id, map_id, map_type, self.xpos, self.ypos)),
                            version=version,
                        )
                    elif cmd == 303 and clear_body is not None:
                        xpos, ypos, item, grid = (
                            struct.unpack(">IIII", clear_body[:16])
                            if len(clear_body) >= 16
                            else (480, 280, 0, 0)
                        )
                        self.xpos = xpos
                        self.ypos = ypos
                        response = packet(
                            303,
                            user_id,
                            moly_encrypt(struct.pack(">IIIII", user_id, xpos, ypos, item, grid)),
                            version=version,
                        )
                        world_hub.broadcast_to_map(self.map_id, response, exclude_handler=self)
                    elif clear_body is not None:
                        response = world_response(
                            cmd, user_id, version, clear_body
                        )
                        # Broadcast live actions to scene neighbors
                        if cmd in (302, 304, 305, 503) and response is not None:
                            world_hub.broadcast_to_map(self.map_id, response, exclude_handler=self)

                    if (
                        (port == 3200 or cmd >= 200)
                        and response is None
                        and cmd not in KNOWN_ONE_WAY_COMMANDS
                    ):
                        server.recorder.write(
                            {
                                "event": "unhandled-command",
                                "port": port,
                                "peer": f"{peer_host}:{peer_port}",
                                "cmd": cmd,
                                "user_id": user_id,
                                "body_hex": (clear_body or b"").hex(),
                            }
                        )

                    if response is not None:
                        self.send_raw(response)
                        server.recorder.write(
                            {
                                "event": "send-frame",
                                "port": port,
                                "peer": f"{peer_host}:{peer_port}",
                                "cmd": cmd,
                                "user_id": user_id,
                                "size": len(response),
                                "hex": response.hex(),
                            }
                        )
        except (TimeoutError, OSError) as error:
            server.recorder.write(
                {
                    "event": "socket-end",
                    "port": port,
                    "peer": f"{peer_host}:{peer_port}",
                    "reason": type(error).__name__,
                }
            )
        finally:
            self.is_alive = False
            if port == 3200 and self.user_id is not None and self.user_id >= 0:
                leave_pkt = packet(402, self.user_id, moly_encrypt(struct.pack(">II", self.map_id, self.user_id)))
                world_hub.broadcast_to_map(self.map_id, leave_pkt, exclude_handler=self)
                world_hub.unregister(self)
            server.recorder.write(
                {"event": "disconnect", "port": port, "peer": f"{peer_host}:{peer_port}"}
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--ports", type=int, nargs="+", default=[843, 1863, 3200])
    args = parser.parse_args()

    recorder = Recorder(args.log.resolve())
    servers = [ThreadedServer((args.host, port), recorder) for port in args.ports]
    threads = [
        threading.Thread(target=server.serve_forever, daemon=True) for server in servers
    ]
    for thread in threads:
        thread.start()
    recorder.write({"event": "listening", "host": args.host, "ports": args.ports})
    try:
        threads[0].join()
    except KeyboardInterrupt:
        pass
    finally:
        for server in servers:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    main()
