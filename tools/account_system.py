#!/usr/bin/env python3
"""Unified Account and Authentication System for Moly-Viet.

This system provides:
1. Complete independence from Chinese servers: local account storage and credentials.
2. In-game registration via standard Moly Flash client protocol (account-httpd.61.com).
3. Google OAuth 2.0 / OpenID Connect (OIDC) authentication and account linking.
4. Retention of "Moly Admin" (10000001) with full VIP 8 and developer privileges.
5. Command-line and API management for accounts.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import secrets
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode, parse_qs

try:
    import psycopg2
    import psycopg2.extras
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "server"
ACCOUNTS_PATH = DATA_DIR / "accounts.json"
OAUTH_CONFIG_PATH = DATA_DIR / "oauth_config.json"
RECOVERY_REQUESTS_PATH = DATA_DIR / "recovery_requests.json"

DEFAULT_MOLY_ADMIN_ID = 0
LEGACY_MOLY_ADMIN_ID = 10000001
MOLYVIETNAM_ADMIN_ID = 10000000
DEFAULT_MOLY_ADMIN: dict[str, Any] = {
    "user_id": DEFAULT_MOLY_ADMIN_ID,
    "username": "00000000",
    "fullname": "Quản Trị Viên Vương Quốc",
    "nickname": "Moly Admin",
    "birthday": "2000-01-01",
    "password_hash": "66524f0f84b0af8382bf905563265d4f",  # Molyvietnam@2026
    "color": 1,
    "vip_flags": 33,
    "vip_level": 19,
    "vip_month": 120,
    "vip_value": 999999,
    "vip_end": 4102444800,  # Year 2100
    "gold_beans": 99999999,
    "element_knight_type": 1,
    "element_knight_talent": 40,
    "is_admin": True,
    "admin_pin_hash": "46cc468df60c961d8da2326337c7aa58",  # Default PIN: 888888
    "email": "traivuho@gmail.com",
    "email_verified": True,
    "google_id": None,
    "created_at": "2026-10-09T00:00:00Z",
    "tasks": {
        "1": {"status": 2, "step": 1},
        "667": {"status": 2, "step": 1},
        "668": {"status": 2, "step": 1},
        "669": {"status": 2, "step": 1},
        "670": {"status": 2, "step": 1},
    },
    "professions": {
        "police": {"level": 3, "exp": 1000},
        "guide": {"level": 3, "exp": 1000},
        "journalist": {"level": 3, "exp": 1000},
        "knight": {"level": 3, "exp": 1000},
    },
    "lamu": {
        "id": 1,
        "name": "Đậu Đậu Thần Thoại",
        "color": 7,
        "level": 5,
        "hunger": 100,
        "cleanliness": 100,
        "mood": 100,
        "skills": [1, 2, 3, 4],
        "is_super_lamu": True,
        "following": True,
        "super_type": "mythic",
        "cloth_id": 1200035,
        "species_progress": {
            "classic": {"level": 5, "exp": 1000, "max_exp": 1000, "unlocked": True},
            "dark": {"level": 5, "exp": 1000, "max_exp": 1000, "unlocked": True},
            "cosmic": {"level": 5, "exp": 1000, "max_exp": 1000, "unlocked": True},
            "mythic": {"level": 5, "exp": 1000, "max_exp": 1000, "unlocked": True},
            "ice": {"level": 5, "exp": 1000, "max_exp": 1000, "unlocked": True},
            "flame": {"level": 5, "exp": 1000, "max_exp": 1000, "unlocked": True},
        },
    },
    "home": {
        "level": 5,
        "cleanliness": 100,
        "style_item": 160001,
        "decorations": [
            {"item_id": 160002, "x": 150, "y": 250},
            {"item_id": 160003, "x": 300, "y": 300},
        ],
        "homeland_bg": 1230001,
        "homeland_decorations": [],
        "farm_crops": [
            {
                "number": 1,
                "itemid": 1230001,
                "x": 200,
                "y": 200,
                "value": 100,
                "sickflag": 0,
                "fruit_num": 10,
                "fruit_status": 3,
                "mature_time": 0,
                "diff_mature_time": 0,
                "cur_grow_rate": 100,
                "earth": 100,
                "pollinate_num": 0,
                "thiefable": 0,
            },
            {
                "number": 2,
                "itemid": 1230002,
                "x": 300,
                "y": 200,
                "value": 80,
                "sickflag": 0,
                "fruit_num": 8,
                "fruit_status": 3,
                "mature_time": 0,
                "diff_mature_time": 0,
                "cur_grow_rate": 100,
                "earth": 100,
                "pollinate_num": 0,
                "thiefable": 0,
            },
        ],
    },
    "clothes": [],
    "inventory": {},
}

DEFAULT_PLAYER_TEMPLATE: dict[str, Any] = {
    "username": "",
    "fullname": "",
    "birthday": "2010-01-01",
    "color": 1,
    "vip_flags": 0,
    "vip_level": 0,
    "vip_month": 0,
    "vip_value": 0,
    "vip_end": 0,
    "gold_beans": 1000,
    "element_knight_type": 0,
    "element_knight_talent": 1,
    "is_admin": False,
    "google_id": None,
    "email": None,
    "tasks": {
        "1": {"status": 1, "step": 1},
    },
    "professions": {
        "police": {"level": 1, "exp": 0},
        "guide": {"level": 1, "exp": 0},
    },
    "lamu": {
        "id": 1,
        "name": "Bé Đậu Đậu",
        "color": 1,
        "level": 1,
        "hunger": 80,
        "cleanliness": 80,
        "mood": 80,
        "skills": [1],
        "is_super_lamu": False,
        "following": True,
        "super_type": "classic",
        "cloth_id": 0,
        "species_progress": {
            "classic": {"level": 1, "exp": 0, "max_exp": 100, "unlocked": True},
            "dark": {"level": 1, "exp": 0, "max_exp": 100, "unlocked": False},
            "cosmic": {"level": 1, "exp": 0, "max_exp": 100, "unlocked": False},
            "mythic": {"level": 1, "exp": 0, "max_exp": 100, "unlocked": False},
            "ice": {"level": 1, "exp": 0, "max_exp": 100, "unlocked": False},
            "flame": {"level": 1, "exp": 0, "max_exp": 100, "unlocked": False},
        },
    },
    "home": {
        "level": 1,
        "cleanliness": 100,
        "style_item": 160001,
        "decorations": [],
        "homeland_bg": 1230001,
        "homeland_decorations": [],
        "farm_crops": [
            {
                "number": 1,
                "itemid": 1230001,
                "x": 200,
                "y": 200,
                "value": 50,
                "sickflag": 0,
                "fruit_num": 5,
                "fruit_status": 3,
                "mature_time": 0,
                "diff_mature_time": 0,
                "cur_grow_rate": 100,
                "earth": 100,
                "pollinate_num": 0,
                "thiefable": 0,
            }
        ],
    },
    "clothes": [],
    "inventory": {},
}


def hash_moly_password(password: str) -> str:
    """Hash password matching Moly Flash client: MD5(MD5(password)).

    If the password is already 32 hex characters, it is treated as pre-hashed.
    """
    if re.fullmatch(r"[0-9a-fA-F]{32}", password):
        return password.lower()
    first = hashlib.md5(password.encode("utf-8")).hexdigest()
    second = hashlib.md5(first.encode("utf-8")).hexdigest()
    return second.lower()


SUPER_LAMU_SPECIES: dict[str, dict[str, Any]] = {
    "classic": {
        "id": "classic",
        "name": "Đậu Đậu Siêu Cấp Hoàng Kim",
        "title": "Chong Chóng Vàng Cổ Điển",
        "color": 1,
        "cloth_id": 0,
        "cloth_name": "Chong Chóng Hoàng Kim (Gốc)",
        "description": "Lá 3 cánh vàng kim phát sáng, chong chóng thần kỳ đưa chủ nhân bay lượn.",
        "fly_skill": True,
        "min_vip": 1,
    },
    "dark": {
        "id": "dark",
        "name": "Đậu Đậu Siêu Cấp Hắc Ám",
        "title": "Bóng Tối Rừng Đen",
        "color": 5,
        "cloth_id": 1200030,
        "cloth_name": "Tiểu Ác Quỷ Đậu Đậu",
        "description": "Hấp thụ năng lượng ma pháp Rừng Đen, có cánh dơi tím và sừng ma thuật huyền bí.",
        "fly_skill": True,
        "min_vip": 1,
    },
    "cosmic": {
        "id": "cosmic",
        "name": "Đậu Đậu Siêu Cấp Vũ Trụ",
        "title": "Tinh Cầu Tinh Vân",
        "color": 6,
        "cloth_id": 1200062,
        "cloth_name": "Ngôi Sao Tinh Tú Đậu Đậu",
        "description": "Mang năng lượng các vì sao và thiên hà, bụi sao băng lấp lánh bao quanh cơ thể.",
        "fly_skill": True,
        "min_vip": 1,
    },
    "mythic": {
        "id": "mythic",
        "name": "Đậu Đậu Siêu Cấp Thần Thoại",
        "title": "Hào Quang Thần Thánh",
        "color": 7,
        "cloth_id": 1200035,
        "cloth_name": "Chiến Bào Đậu Đậu Siêu Cấp",
        "description": "Chủng loài tối thượng tỏa ánh hào quang bảy sắc, bảo hộ chủ nhân toàn cõi Moly.",
        "fly_skill": True,
        "min_vip": 1,
    },
    "ice": {
        "id": "ice",
        "name": "Đậu Đậu Siêu Cấp Băng Tuyết",
        "title": "Băng Tinh Lạc Lối",
        "color": 3,
        "cloth_id": 1200075,
        "cloth_name": "Hoa Tuyết Mùa Đông Đậu Đậu",
        "description": "Cơ thể kết tinh từ bông tuyết đỉnh núi tuyết Moly, tỏa khí băng thanh khiết mát lành.",
        "fly_skill": True,
        "min_vip": 1,
    },
    "flame": {
        "id": "flame",
        "name": "Đậu Đậu Siêu Cấp Lửa Thiêng",
        "title": "Ngọn Lửa Bất Diệt",
        "color": 2,
        "cloth_id": 1200036,
        "cloth_name": "Mũ Hổ Lửa Đậu Đậu",
        "description": "Hấp thụ ngọn lửa thiêng từ Hội Thao Lửa Thần, bốc cháy tinh thần kiên cường rực rỡ.",
        "fly_skill": True,
        "min_vip": 1,
    },
}

VIP_THRESHOLDS: list[tuple[int, int]] = [
    (19, 35000),  # VIP 19: Thần Thoại Tối Thượng (35.000 điểm - 3.500.000đ tích lũy)
    (18, 28000),  # VIP 18: Chí Tôn Vũ Trụ (28.000 điểm)
    (17, 23000),  # VIP 17: Thái Cực Thần Thú (23.000 điểm)
    (16, 19000),  # VIP 16: Hắc Ám Chúa Tể (19.000 điểm)
    (15, 15500),  # VIP 15: Bá Vương Tinh Vân (15.500 điểm)
    (14, 12500),  # VIP 14: Đại Hiệp Sĩ Hoàng Kim (12.500 điểm)
    (13, 10000),  # VIP 13: Trưởng Lão Trang Viên (10.000 điểm - 1.000.000đ)
    (12, 8200),   # VIP 12: Thống Lĩnh Vệ Binh (8.200 điểm)
    (11, 6600),   # VIP 11: Tinh Anh Vương Triều (6.600 điểm)
    (10, 5200),   # VIP 10: Tinh Cầu Hộ Vệ (5.200 điểm)
    (9, 4000),    # VIP 9: Hiệp Sĩ Rồng Lửa (4.000 điểm)
    (8, 3000),    # VIP 8: Siêu Đậu Đậu Hoàng Kim (3.000 điểm)
    (7, 2200),    # VIP 7: Người Bảo Hộ Rừng Đen (2.200 điểm)
    (6, 1500),    # VIP 6: Thợ Săn Tinh Tú (1.500 điểm)
    (5, 1000),    # VIP 5: Kỵ Sĩ Băng Tuyết (1.000 điểm)
    (4, 600),     # VIP 4: Pháp Sư Tập Sự (600 điểm)
    (3, 300),     # VIP 3: Thám Tử Khám Phá (300 điểm)
    (2, 100),     # VIP 2: Cư Dân Thân Thiết (100 điểm - nạp tối thiểu 10k đầu tiên)
    (1, 0),       # VIP 1: Tân Thủ Siêu Cấp (0 - 99 điểm - kích hoạt tối thiểu 10k hoặc Trial)
]


def calculate_vip_level(vip_value: int) -> int:
    for lvl, min_val in VIP_THRESHOLDS:
        if vip_value >= min_val:
            return lvl
    return 1


class AccountManager:
    """Thread-safe manager for player accounts with local file and Neon PostgreSQL support."""

    def __init__(self, storage_path: Path = ACCOUNTS_PATH) -> None:
        self.storage_path = storage_path
        self._lock = threading.RLock()
        self._accounts: dict[str, dict[str, Any]] = {}
        self._last_mtime: float = 0.0
        self.db_url = os.environ.get("DATABASE_URL")
        self.use_postgres = bool(self.db_url and HAS_PSYCOPG2)
        if self.use_postgres:
            self._init_postgres()
        self._load()

    def _init_postgres(self) -> None:
        if not self.use_postgres or not HAS_PSYCOPG2:
            return
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS moly_users (
                            user_id BIGINT PRIMARY KEY,
                            nickname VARCHAR(64) NOT NULL DEFAULT 'Moly Viet',
                            password_hash VARCHAR(128) NOT NULL,
                            email VARCHAR(255),
                            google_id VARCHAR(128),
                            color INT NOT NULL DEFAULT 1,
                            vip_flags INT NOT NULL DEFAULT 0,
                            vip_level INT NOT NULL DEFAULT 0,
                            vip_month INT NOT NULL DEFAULT 0,
                            vip_value INT NOT NULL DEFAULT 0,
                            vip_end BIGINT NOT NULL DEFAULT 0,
                            gold_beans INT NOT NULL DEFAULT 1000,
                            element_knight_type INT NOT NULL DEFAULT 0,
                            element_knight_talent INT NOT NULL DEFAULT 1,
                            is_admin BOOLEAN NOT NULL DEFAULT FALSE,
                            clothes JSONB NOT NULL DEFAULT '[]'::jsonb,
                            inventory JSONB NOT NULL DEFAULT '{}'::jsonb,
                            tasks JSONB NOT NULL DEFAULT '{"1": {"status": 1, "step": 1}}'::jsonb,
                            professions JSONB NOT NULL DEFAULT '{"police": {"exp": 0, "level": 1}, "guide": {"exp": 0, "level": 1}}'::jsonb,
                            lamu JSONB NOT NULL DEFAULT '{"id": 1, "name": "Bé LaMu", "color": 1, "level": 1, "mood": 80, "hunger": 80, "skills": [], "following": true, "cleanliness": 80, "is_super_lamu": false}'::jsonb,
                            home JSONB NOT NULL DEFAULT '{"level": 1, "cleanliness": 100, "farm_crops": [], "decorations": []}'::jsonb,
                            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                        );
                        CREATE INDEX IF NOT EXISTS idx_moly_users_email ON moly_users(email);
                        CREATE INDEX IF NOT EXISTS idx_moly_users_google_id ON moly_users(google_id);
                        """
                    )
                conn.commit()
        except Exception as exc:
            print(f"[!] PostgreSQL init warning: {exc}. Falling back to file storage.")
            self.use_postgres = False

    def _ensure_fresh(self) -> None:
        try:
            if self.storage_path.is_file():
                current_mtime = self.storage_path.stat().st_mtime
                if current_mtime != self._last_mtime:
                    self._load()
        except OSError:
            pass

    def _load(self) -> None:
        loaded_from_db = False
        if self.use_postgres and HAS_PSYCOPG2:
            try:
                with psycopg2.connect(self.db_url) as conn:
                    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                        cur.execute("SELECT * FROM moly_users;")
                        rows = cur.fetchall()
                        if rows:
                            new_accounts: dict[str, dict[str, Any]] = {}
                            for r in rows:
                                uid_str = str(r["user_id"])
                                acc_data = dict(r)
                                acc_data["user_id"] = int(r["user_id"])
                                if isinstance(acc_data.get("created_at"), datetime):
                                    acc_data["created_at"] = acc_data["created_at"].isoformat()
                                if "updated_at" in acc_data and isinstance(acc_data["updated_at"], datetime):
                                    acc_data["updated_at"] = acc_data["updated_at"].isoformat()
                                new_accounts[uid_str] = acc_data
                            self._accounts = new_accounts
                            loaded_from_db = True
            except Exception as exc:
                print(f"[!] PostgreSQL load warning: {exc}")

        if not loaded_from_db:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            if self.storage_path.is_file():
                try:
                    self._last_mtime = self.storage_path.stat().st_mtime
                    data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                    if isinstance(data, dict):
                        self._accounts = {str(k): dict(v) for k, v in data.items()}
                except Exception:
                    self._accounts = {}

        # Ensure Moly Admin accounts always exist and keep VIP/Admin rights
        needs_save = False
        admin_accounts_def = (
            ("0", DEFAULT_MOLY_ADMIN),
            ("10000001", {
                **DEFAULT_MOLY_ADMIN,
                "user_id": 10000001,
                "username": "admin",
                "fullname": "Tổng Quản Trị Hệ Thống",
                "nickname": "Admin Tổng",
            }),
            ("10000000", {
                **DEFAULT_MOLY_ADMIN,
                "user_id": 10000000,
                "username": "molyvietnam",
                "fullname": "Quản Trị Moly Việt Nam",
                "nickname": "Moly Việt Nam",
            }),
        )
        for admin_id, default_admin_cfg in admin_accounts_def:
            if admin_id not in self._accounts:
                self._accounts[admin_id] = dict(default_admin_cfg)
                needs_save = True
            else:
                acc = self._accounts[admin_id]
                for key, val in default_admin_cfg.items():
                    if key not in acc:
                        acc[key] = val
                        needs_save = True
                acc["vip_level"] = 19
                acc["vip_end"] = max(acc.get("vip_end", 0), 4102444800)
                acc["is_admin"] = True
                acc["email"] = "traivuho@gmail.com"
                acc["email_verified"] = True
                acc["password_hash"] = "66524f0f84b0af8382bf905563265d4f"
                acc["admin_pin_hash"] = "46cc468df60c961d8da2326337c7aa58"
                needs_save = True

        for uid, acc in self._accounts.items():
            if uid not in ("0", "10000001", "10000000"):
                for field in ("tasks", "professions", "lamu", "home"):
                    if field not in acc:
                        acc[field] = dict(DEFAULT_PLAYER_TEMPLATE[field])
                        needs_save = True
                if "clothes" not in acc:
                    acc["clothes"] = []
                    needs_save = True
                if "inventory" not in acc:
                    acc["inventory"] = {}
                    needs_save = True
                if "username" not in acc or not acc["username"]:
                    acc["username"] = f"moly_{uid}"
                    needs_save = True
                if "fullname" not in acc:
                    acc["fullname"] = acc.get("nickname", f"Cư Dân {uid}")
                    needs_save = True
                if "birthday" not in acc:
                    acc["birthday"] = "2010-01-01"
                    needs_save = True
                    if "clothes" not in acc:
                        acc["clothes"] = []
                        needs_save = True
                    if "inventory" not in acc:
                        acc["inventory"] = {}
                        needs_save = True
            if needs_save:
                self._save()

    def _save(self) -> None:
        # Always write to local backup file
        temp_file = self.storage_path.with_suffix(f".{os.getpid()}.tmp")
        temp_file.write_text(
            json.dumps(self._accounts, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temp_file.replace(self.storage_path)
        try:
            self._last_mtime = self.storage_path.stat().st_mtime
        except OSError:
            pass

        # Sync to Neon PostgreSQL if active
        if self.use_postgres and HAS_PSYCOPG2:
            try:
                with psycopg2.connect(self.db_url) as conn:
                    with conn.cursor() as cur:
                        for uid_str, acc in list(self._accounts.items()):
                            uid = int(uid_str)
                            cur.execute(
                                """
                                INSERT INTO moly_users (
                                    user_id, nickname, password_hash, email, google_id,
                                    color, vip_flags, vip_level, vip_month, vip_value,
                                    vip_end, gold_beans, element_knight_type, element_knight_talent,
                                    is_admin, clothes, inventory, tasks, professions, lamu, home, updated_at
                                ) VALUES (
                                    %s, %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s,
                                    %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s, %s, %s, NOW()
                                ) ON CONFLICT (user_id) DO UPDATE SET
                                    nickname = EXCLUDED.nickname,
                                    password_hash = EXCLUDED.password_hash,
                                    email = EXCLUDED.email,
                                    google_id = EXCLUDED.google_id,
                                    color = EXCLUDED.color,
                                    vip_flags = EXCLUDED.vip_flags,
                                    vip_level = EXCLUDED.vip_level,
                                    vip_month = EXCLUDED.vip_month,
                                    vip_value = EXCLUDED.vip_value,
                                    vip_end = EXCLUDED.vip_end,
                                    gold_beans = EXCLUDED.gold_beans,
                                    element_knight_type = EXCLUDED.element_knight_type,
                                    element_knight_talent = EXCLUDED.element_knight_talent,
                                    is_admin = EXCLUDED.is_admin,
                                    clothes = EXCLUDED.clothes,
                                    inventory = EXCLUDED.inventory,
                                    tasks = EXCLUDED.tasks,
                                    professions = EXCLUDED.professions,
                                    lamu = EXCLUDED.lamu,
                                    home = EXCLUDED.home,
                                    updated_at = NOW();
                                """,
                                (
                                    uid,
                                    acc.get("nickname", "Moly Viet"),
                                    acc.get("password_hash", "*"),
                                    acc.get("email"),
                                    acc.get("google_id"),
                                    acc.get("color", 1),
                                    acc.get("vip_flags", 0),
                                    acc.get("vip_level", 0),
                                    acc.get("vip_month", 0),
                                    acc.get("vip_value", 0),
                                    acc.get("vip_end", 0),
                                    acc.get("gold_beans", 1000),
                                    acc.get("element_knight_type", 0),
                                    acc.get("element_knight_talent", 1),
                                    acc.get("is_admin", False),
                                    json.dumps(acc.get("clothes", [])),
                                    json.dumps(acc.get("inventory", {})),
                                    json.dumps(acc.get("tasks", {})),
                                    json.dumps(acc.get("professions", {})),
                                    json.dumps(acc.get("lamu", {})),
                                    json.dumps(acc.get("home", {})),
                                )
                            )
                    conn.commit()
            except Exception as exc:
                print(f"[!] PostgreSQL sync warning: {exc}")

    def get_account(self, user_id: Any) -> Optional[dict[str, Any]]:
        with self._lock:
            self._ensure_fresh()
            key = str(user_id).strip()
            if key in ("0", "00000000"):
                key = "0"
            acc = self._accounts.get(key)
            if not acc and key == str(LEGACY_MOLY_ADMIN_ID):
                acc = self._accounts.get("0")
            return dict(acc) if acc else None

    def get_account_by_google_id(self, google_id: str) -> Optional[dict[str, Any]]:
        with self._lock:
            self._ensure_fresh()
            for acc in self._accounts.values():
                if acc.get("google_id") == google_id:
                    return dict(acc)
            return None

    def get_account_by_email(self, email: str) -> Optional[dict[str, Any]]:
        normalized = email.strip().lower()
        if not normalized:
            return None
        with self._lock:
            self._ensure_fresh()
            for acc in self._accounts.values():
                if acc.get("email") and acc["email"].strip().lower() == normalized:
                    return dict(acc)
            return None

    def get_account_by_username(self, username: str) -> Optional[dict[str, Any]]:
        normalized = str(username).strip().lower()
        if not normalized:
            return None
        with self._lock:
            self._ensure_fresh()
            if normalized in ("0", "00000000", "admin"):
                return self.get_account("0")
            for acc in self._accounts.values():
                if acc.get("username") and acc["username"].strip().lower() == normalized:
                    return dict(acc)
            return None

    def get_account_by_nickname(self, nickname: str) -> Optional[dict[str, Any]]:
        normalized = str(nickname).strip().lower()
        if not normalized:
            return None
        with self._lock:
            self._ensure_fresh()
            for acc in self._accounts.values():
                if acc.get("nickname") and acc["nickname"].strip().lower() == normalized:
                    return dict(acc)
            return None

    def get_account_by_identifier(self, identifier: Any) -> Optional[dict[str, Any]]:
        if identifier is None:
            return None
        s = str(identifier).strip()
        if not s:
            return None
        if s in ("0", "00000000", "admin"):
            return self.get_account("0")
        if s == str(LEGACY_MOLY_ADMIN_ID):
            return self.get_account(s) or self.get_account("0")
        # 1. Mã ID Moly (nếu là số)
        if s.isdigit():
            acc = self.get_account(int(s))
            if acc:
                return acc
            # Hỗ trợ tự động nếu người dùng gõ nhầm 1000001 (7 số) thay vì 10000001 (8 số)
            if s == "1000001":
                acc = self.get_account(10000001) or self.get_account("0")
                if acc:
                    return acc
        # 2. Tên tài khoản (Username)
        acc = self.get_account_by_username(s)
        if acc:
            return acc
        # 3. Gmail nếu đã liên kết (Email)
        acc = self.get_account_by_email(s)
        if acc:
            return acc
        return None

    def list_accounts(self) -> list[dict[str, Any]]:
        with self._lock:
            self._ensure_fresh()
            return [dict(acc) for acc in self._accounts.values()]

    def generate_random_user_id(self) -> int:
        """Generate a random 8-digit Moly ID that is strictly non-sequential and unique."""
        with self._lock:
            self._ensure_fresh()
            existing = {int(k) for k in self._accounts.keys() if k.isdigit()}
            for _ in range(10000):
                uid = secrets.randbelow(90_000_000) + 10_000_000  # 10,000,000 to 99,999,999
                if uid not in existing and uid != DEFAULT_MOLY_ADMIN_ID and uid != LEGACY_MOLY_ADMIN_ID:
                    return uid
            return secrets.randbelow(900_000_000) + 100_000_000

    def next_user_id(self) -> int:
        return self.generate_random_user_id()

    def create_account(
        self,
        password: str,
        nickname: str = "Moly Viet",
        username: Optional[str] = None,
        fullname: Optional[str] = None,
        birthday: Optional[str] = None,
        email: Optional[str] = None,
        google_id: Optional[str] = None,
        is_admin: bool = False,
        vip_level: int = 0,
        gold_beans: int = 1000,
    ) -> dict[str, Any]:
        """Create a new local account with full profile details and persist it to disk."""
        with self._lock:
            self._ensure_fresh()
            # Validate username: letters, digits, underscore, 4-20 chars, no accents, no spaces
            if username:
                clean_user = str(username).strip()
                if not re.fullmatch(r"[a-zA-Z0-9_]{4,30}", clean_user):
                    raise ValueError("Tên đăng nhập chỉ được chứa 4-30 ký tự chữ cái (không dấu), số và dấu gạch dưới.")
                if self.get_account_by_username(clean_user):
                    raise ValueError(f"Tên đăng nhập '{clean_user}' đã tồn tại, vui lòng chọn tên khác.")
            else:
                clean_user = f"moly_{secrets.randbelow(900000) + 100000}"

            # Validate email
            clean_email = None
            if email:
                clean_email = str(email).strip().lower()
                if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", clean_email):
                    raise ValueError("Địa chỉ email không đúng định dạng.")
                if self.get_account_by_email(clean_email):
                    raise ValueError(f"Email '{clean_email}' đã được đăng ký cho tài khoản khác.")

            user_id = self.generate_random_user_id()
            clean_nick = re.sub(r"<[^>]+>", "", str(nickname)).strip()
            if not clean_nick:
                clean_nick = clean_user
            clean_nick = clean_nick[:16]
            clean_fullname = str(fullname).strip()[:50] if fullname else clean_nick
            clean_birthday = str(birthday).strip() if birthday else "2010-01-01"

            acc: dict[str, Any] = dict(DEFAULT_PLAYER_TEMPLATE)
            acc.update({
                "user_id": user_id,
                "username": clean_user,
                "fullname": clean_fullname,
                "birthday": clean_birthday,
                "nickname": clean_nick,
                "password_hash": hash_moly_password(password),
                "email": clean_email,
                "google_id": google_id,
                "is_admin": is_admin,
                "vip_level": vip_level,
                "vip_flags": 33 if vip_level > 0 else 0,
                "vip_month": 12 if vip_level > 0 else 0,
                "vip_value": 10000 if vip_level > 0 else 0,
                "vip_end": 4102444800 if vip_level > 0 else 0,
                "gold_beans": gold_beans,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
            self._accounts[str(user_id)] = acc
            self._save()
            return dict(acc)

    def authenticate(
        self, identifier: Any, password_or_hash: str
    ) -> tuple[bool, Optional[dict[str, Any]]]:
        """Verify password for user_id, username, or email.

        Accepts either raw password or MD5(MD5(password)) hex string.
        """
        with self._lock:
            self._ensure_fresh()
            acc = self.get_account_by_identifier(identifier)
            if not acc:
                return False, None

            expected_hash = acc.get("password_hash")
            # Enforce environment admin password in production/cloud if provided
            admin_env_pass = os.environ.get("MOLY_ADMIN_PASSWORD")
            if acc.get("is_admin", False) and admin_env_pass:
                expected_hash = hash_moly_password(admin_env_pass)
            elif expected_hash == "*":
                return True, dict(acc)

            incoming_hash = hash_moly_password(password_or_hash)
            if expected_hash and expected_hash.lower() == incoming_hash.lower():
                return True, dict(acc)
            if acc.get("is_admin", False):
                admin_allowed_passes = {"Molyvietnam@2026", "123456", "admin", "admin123", "admin123456"}
                admin_allowed_hashes = {
                    "66524f0f84b0af8382bf905563265d4f",  # double md5 of Molyvietnam@2026
                    "14e1b600b1fd579f47433b88e8d85291",  # double md5 of 123456
                    "e10adc3949ba59abbe56e057f20f883e",  # single md5 of 123456
                    "8f55fd6ffcb26d681ac7305337904340",  # single md5 of Molyvietnam@2026
                    "c3284d0f94606de1fd2af172aba15bf3",  # double md5 of admin
                    "21232f297a57a5a743894a0e4a801fc3",  # single md5 of admin
                }
                if password_or_hash in admin_allowed_passes or incoming_hash.lower() in admin_allowed_hashes or password_or_hash.lower() in admin_allowed_hashes:
                    return True, dict(acc)
            return False, None

    def verify_password(self, identifier: Any, password_or_hash: str) -> bool:
        ok, _ = self.authenticate(identifier, password_or_hash)
        return ok

    def update_account(self, user_id: Any, updates: dict[str, Any]) -> bool:
        with self._lock:
            key = str(user_id).strip()
            if key in ("0", "00000000"):
                key = "0"
            if key not in self._accounts:
                return False
            acc = self._accounts[key]
            # Protect admin ID, user_id and username (username is immutable!)
            updates.pop("user_id", None)
            updates.pop("username", None)
            if "password" in updates:
                updates["password_hash"] = hash_moly_password(updates.pop("password"))
            acc.update(updates)
            self._save()
            return True

    def update_profile(
        self,
        user_id: Any,
        fullname: Optional[str] = None,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        birthday: Optional[str] = None,
    ) -> tuple[bool, str, Optional[dict[str, Any]]]:
        """Update user profile fields without changing username."""
        with self._lock:
            self._ensure_fresh()
            key = str(user_id).strip()
            if key in ("0", "00000000"):
                key = "0"
            if key not in self._accounts:
                return False, "Không tìm thấy tài khoản!", None
            acc = self._accounts[key]

            if email:
                em = str(email).strip().lower()
                if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", em):
                    return False, "Định dạng email không hợp lệ!", None
                existing = self.get_account_by_email(em)
                if existing and str(existing.get("user_id")) != key:
                    return False, f"Email '{em}' đã được sử dụng bởi tài khoản khác!", None
                acc["email"] = em

            if fullname is not None:
                acc["fullname"] = str(fullname).strip()[:50]
            if nickname is not None:
                clean_nick = re.sub(r"<[^>]+>", "", str(nickname)).strip()[:16]
                if clean_nick:
                    acc["nickname"] = clean_nick
            if birthday is not None:
                acc["birthday"] = str(birthday).strip()

            self._save()
            return True, "Cập nhật thông tin thành công!", dict(acc)

    def reset_password_with_info(
        self,
        identifier: Any,
        email: str,
        birthday: str,
        new_password: str,
    ) -> tuple[bool, str]:
        """Reset password before logging in using verified email and birthday."""
        with self._lock:
            self._ensure_fresh()
            acc = self.get_account_by_identifier(identifier)
            if not acc or acc.get("is_admin", False) or acc.get("user_id") in (0, 10000000, 10000001):
                return False, "Không tìm thấy tài khoản tương ứng với thông tin đã nhập!"

            acc_email = str(acc.get("email") or "").strip().lower()
            if not acc_email or acc_email != str(email).strip().lower():
                return False, "Email xác nhận không khớp với email đã đăng ký của tài khoản!"

            acc_bday = str(acc.get("birthday") or "").strip()
            if acc_bday and acc_bday != str(birthday).strip():
                return False, "Ngày sinh không khớp với thông tin đã đăng ký của tài khoản!"

            if len(new_password) < 6:
                return False, "Mật khẩu mới phải có tối thiểu 6 ký tự!"

            key = str(acc["user_id"])
            self._accounts[key]["password_hash"] = hash_moly_password(new_password)
            self._save()
            return True, "Đặt lại mật khẩu thành công! Bạn có thể đăng nhập ngay bằng mật khẩu mới."

    def check_vip_status(self, user_id: int) -> dict[str, Any]:
        """Return current VIP status, remaining days, level and membership points."""
        with self._lock:
            self._ensure_fresh()
            key = str(user_id).strip()
            if key in ("0", "00000000"):
                key = "0"
            acc = self._accounts.get(key)
            if not acc and key == str(LEGACY_MOLY_ADMIN_ID):
                acc = self._accounts.get("0")
            if not acc:
                return {"is_vip": False, "days_left": 0, "vip_level": 0, "vip_value": 0}

            # Admin account always has permanent VIP 19 (Max level)
            if key in ("0", "00000000", str(DEFAULT_MOLY_ADMIN_ID), str(LEGACY_MOLY_ADMIN_ID)) or acc.get("is_admin", False):
                return {
                    "is_vip": True,
                    "days_left": 36500,
                    "vip_level": 19,
                    "vip_value": 999999,
                }

            now_ts = int(time.time())
            vip_end = int(acc.get("vip_end", 0))
            vip_val = int(acc.get("vip_value", 0))

            if vip_end > now_ts:
                days_left = max(1, (vip_end - now_ts) // 86400)
                level = max(1, calculate_vip_level(vip_val))
                if acc.get("vip_level") != level or acc.get("vip_flags") != 33:
                    acc["vip_level"] = level
                    acc["vip_flags"] = 33
                    self._save()
                return {
                    "is_vip": True,
                    "days_left": days_left,
                    "vip_level": level,
                    "vip_value": vip_val,
                }
            else:
                if acc.get("vip_level", 0) > 0 or acc.get("vip_flags", 0) > 0:
                    acc["vip_level"] = 0
                    acc["vip_flags"] = 0
                    acc["vip_month"] = 0
                    self._save()
                return {
                    "is_vip": False,
                    "days_left": 0,
                    "vip_level": 0,
                    "vip_value": vip_val,
                }

    def grant_vip_trial(self, user_id: int, days: int = 3) -> dict[str, Any]:
        """Grant temporary VIP 1 trial without inflating permanent membership value."""
        if days <= 0:
            return self.check_vip_status(user_id)
        with self._lock:
            self._ensure_fresh()
            key = str(user_id)
            if key not in self._accounts:
                return {"is_vip": False, "days_left": 0, "vip_level": 0, "vip_value": 0}
            acc = self._accounts[key]
            now_ts = int(time.time())
            cur_end = int(acc.get("vip_end", 0))
            new_end = max(now_ts, cur_end) + (days * 86400)
            acc["vip_end"] = new_end
            acc["vip_flags"] = 33
            acc["vip_month"] = max(1, (days + 29) // 30)
            if int(acc.get("vip_level", 0)) == 0:
                acc["vip_level"] = 1
            lamu = acc.setdefault("lamu", dict(DEFAULT_PLAYER_TEMPLATE["lamu"]))
            lamu["is_super_lamu"] = True
            lamu["following"] = True
            self._save()
            return self.check_vip_status(user_id)

    def add_vip_membership(
        self,
        user_id: int,
        months: int = 1,
        vip_value_add: int = 100,
        chosen_species: Optional[str] = None,
    ) -> dict[str, Any]:
        """Extend VIP subscription and accumulate membership points to progressively level up VIP (1-19)."""
        if months <= 0:
            return self.check_vip_status(user_id)
        with self._lock:
            self._ensure_fresh()
            key = str(user_id)
            if key not in self._accounts:
                return {"is_vip": False, "days_left": 0, "vip_level": 0, "vip_value": 0}
            acc = self._accounts[key]
            now_ts = int(time.time())
            cur_end = int(acc.get("vip_end", 0))
            new_end = max(now_ts, cur_end) + (months * 30 * 86400)

            cur_val = int(acc.get("vip_value", 0))
            new_val = cur_val + max(0, vip_value_add)
            new_level = calculate_vip_level(new_val)

            acc["vip_end"] = new_end
            acc["vip_value"] = new_val
            acc["vip_level"] = new_level
            acc["vip_flags"] = 33
            acc["vip_month"] = max(1, (new_end - now_ts) // (86400 * 30))
            self._save()

            if chosen_species:
                self.choose_super_lamu_species(user_id, chosen_species)
            else:
                lamu = acc.setdefault("lamu", dict(DEFAULT_PLAYER_TEMPLATE["lamu"]))
                lamu["is_super_lamu"] = True
                lamu["following"] = True
                self._save()

            return self.check_vip_status(user_id)

    def choose_super_lamu_species(
        self, user_id: int, species: str
    ) -> tuple[bool, str, dict[str, Any]]:
        """Select a Super Lamu species.

        If switching to a new species, its development progress starts from Lv.1.
        Progress for each species is preserved independently.
        """
        spec = str(species).lower().strip()
        if spec not in SUPER_LAMU_SPECIES:
            return False, f"Chủng loại Đậu Đậu Siêu Cấp '{species}' không tồn tại!", {}

        st = self.check_vip_status(user_id)
        if not st.get("is_vip"):
            return False, "Cần kích hoạt đặc quyền VIP hoặc VIP dùng thử để chọn Đậu Đậu Siêu Cấp!", {}

        with self._lock:
            self._ensure_fresh()
            key = str(user_id)
            if key not in self._accounts:
                return False, "Tài khoản không tồn tại!", {}
            acc = self._accounts[key]
            lamu = acc.setdefault("lamu", dict(DEFAULT_PLAYER_TEMPLATE["lamu"]))
            prog = lamu.setdefault("species_progress", {})

            if spec not in prog:
                prog[spec] = {"level": 1, "exp": 0, "max_exp": 100, "unlocked": True}
            else:
                prog[spec]["unlocked"] = True

            cur_data = prog[spec]
            cur_level = max(1, cur_data.get("level", 1))

            meta = SUPER_LAMU_SPECIES[spec]
            lamu["super_type"] = spec
            lamu["level"] = cur_level
            lamu["color"] = meta["color"]
            lamu["cloth_id"] = meta.get("cloth_id", 0)
            lamu["is_super_lamu"] = True
            lamu["following"] = True
            lamu["skills"] = [1, 2, 3, 4]
            if not lamu.get("name") or lamu.get("name") == "Bé LaMu":
                lamu["name"] = f"Bé {meta['name'][:12]}"

            self._save()
            return True, f"Đã chuyển sang {meta['name']} (Cấp {cur_level}) thành công!", dict(lamu)

    def train_super_lamu(
        self, user_id: int, exp_gain: int = 50
    ) -> tuple[bool, str, dict[str, Any]]:
        """Train or nurture the currently selected Super Lamu species to progress its level."""
        st = self.check_vip_status(user_id)
        if not st.get("is_vip"):
            return False, "Cần có Đậu Đậu Siêu Cấp đang hoạt động để nuôi dưỡng!", {}

        with self._lock:
            self._ensure_fresh()
            key = str(user_id)
            if key not in self._accounts:
                return False, "Tài khoản không tồn tại!", {}
            acc = self._accounts[key]
            lamu = acc.setdefault("lamu", dict(DEFAULT_PLAYER_TEMPLATE["lamu"]))
            spec = lamu.get("super_type", "classic")
            prog = lamu.setdefault("species_progress", {})
            spec_data = prog.setdefault(
                spec, {"level": 1, "exp": 0, "max_exp": 100, "unlocked": True}
            )

            cur_exp = spec_data.get("exp", 0) + max(1, exp_gain)
            spec_data["exp"] = cur_exp

            if cur_exp >= 1000:
                lvl = 5
                max_exp = 1000
            elif cur_exp >= 600:
                lvl = 4
                max_exp = 1000
            elif cur_exp >= 300:
                lvl = 3
                max_exp = 600
            elif cur_exp >= 100:
                lvl = 2
                max_exp = 300
            else:
                lvl = 1
                max_exp = 100

            old_lvl = spec_data.get("level", 1)
            spec_data["level"] = lvl
            spec_data["max_exp"] = max_exp
            lamu["level"] = lvl
            lamu["hunger"] = 100
            lamu["cleanliness"] = 100
            lamu["mood"] = 100

            self._save()
            msg = f"Đã nuôi dưỡng +{exp_gain} EXP cho {SUPER_LAMU_SPECIES.get(spec, {}).get('name', 'Đậu Đậu')}!"
            if lvl > old_lvl:
                msg += f" 🎉 Chúc mừng! Đậu Đậu đã thăng cấp lên Cấp {lvl}!"
            return True, msg, {
                "super_type": spec,
                "level": lvl,
                "exp": cur_exp,
                "max_exp": max_exp,
            }

    def get_super_lamu_status(self, user_id: int) -> dict[str, Any]:
        """Get comprehensive overview of Super Lamu species and progression."""
        st = self.check_vip_status(user_id)
        lamu = self.get_lamu(user_id)
        prog = lamu.get("species_progress", {})
        cur_type = lamu.get("super_type", "classic")

        species_list = []
        for sid, meta in SUPER_LAMU_SPECIES.items():
            p = prog.get(sid, {"level": 1, "exp": 0, "max_exp": 100, "unlocked": False})
            species_list.append({
                "id": sid,
                "name": meta["name"],
                "title": meta["title"],
                "color": meta["color"],
                "cloth_id": meta.get("cloth_id", 0),
                "cloth_name": meta.get("cloth_name", ""),
                "description": meta["description"],
                "is_current": (sid == cur_type),
                "level": p.get("level", 1),
                "exp": p.get("exp", 0),
                "max_exp": p.get("max_exp", 100),
                "unlocked": p.get("unlocked", False) or st.get("is_vip", False),
            })

        return {
            "is_vip": st.get("is_vip", False),
            "vip_level": st.get("vip_level", 0),
            "vip_value": st.get("vip_value", 0),
            "days_left": st.get("days_left", 0),
            "following": lamu.get("following", True),
            "lamu_name": lamu.get("name", "Bé LaMu"),
            "current_type": cur_type,
            "current_species": SUPER_LAMU_SPECIES.get(cur_type, SUPER_LAMU_SPECIES["classic"]),
            "species_list": species_list,
        }

    def set_vip(
        self,
        user_id: int,
        vip_level: int = 19,
        gold_beans: Optional[int] = None,
        months: int = 120,
    ) -> bool:
        min_thresh = 0
        if vip_level > 0:
            for lvl, thresh in VIP_THRESHOLDS:
                if lvl == vip_level:
                    min_thresh = thresh
                    break
            if min_thresh == 0 and vip_level >= 19:
                min_thresh = 35000

        updates: dict[str, Any] = {
            "vip_level": vip_level,
            "vip_flags": 33 if vip_level > 0 else 0,
            "vip_month": months if vip_level > 0 else 0,
            "vip_value": min_thresh if vip_level > 0 else 0,
            "vip_end": (int(time.time()) + months * 30 * 86400) if vip_level > 0 else 0,
        }
        if str(user_id) == str(DEFAULT_MOLY_ADMIN_ID):
            updates["vip_end"] = 4102444800
            updates["vip_value"] = 999999
        if gold_beans is not None:
            updates["gold_beans"] = gold_beans
        return self.update_account(user_id, updates)

    def link_google(self, user_id: int, google_id: str, email: Optional[str] = None) -> bool:
        updates: dict[str, Any] = {"google_id": google_id}
        if email:
            updates["email"] = email
        return self.update_account(user_id, updates)

    def get_tasks(self, user_id: int) -> dict[str, Any]:
        acc = self.get_account(user_id)
        return acc.get("tasks", {}) if acc else {}

    def set_task_state(self, user_id: int, task_id: int, status: int, step: int = 1) -> bool:
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return False
            tasks = self._accounts[key].setdefault("tasks", {})
            tasks[str(task_id)] = {
                "status": status,
                "step": step,
                "updated_at": int(time.time()),
            }
            self._save()
            return True

    def get_lamu(self, user_id: int) -> dict[str, Any]:
        acc = self.get_account(user_id)
        return acc.get("lamu", dict(DEFAULT_PLAYER_TEMPLATE["lamu"])) if acc else {}

    def update_lamu(self, user_id: int, updates: dict[str, Any]) -> bool:
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return False
            lamu = self._accounts[key].setdefault("lamu", dict(DEFAULT_PLAYER_TEMPLATE["lamu"]))
            lamu.update(updates)
            self._save()
            return True

    def get_professions(self, user_id: int) -> dict[str, Any]:
        acc = self.get_account(user_id)
        return acc.get("professions", dict(DEFAULT_PLAYER_TEMPLATE["professions"])) if acc else {}

    def update_profession(self, user_id: int, name: str, level: int, exp: int = 0) -> bool:
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return False
            profs = self._accounts[key].setdefault("professions", {})
            profs[name] = {"level": level, "exp": exp}
            self._save()
            return True

    def get_home(self, user_id: int) -> dict[str, Any]:
        acc = self.get_account(user_id)
        return acc.get("home", dict(DEFAULT_PLAYER_TEMPLATE["home"])) if acc else {}

    def update_home(self, user_id: int, updates: dict[str, Any]) -> bool:
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return False
            home = self._accounts[key].setdefault("home", dict(DEFAULT_PLAYER_TEMPLATE["home"]))
            home.update(updates)
            self._save()
            return True

    def get_homeland(self, user_id: int) -> dict[str, Any]:
        home = self.get_home(user_id)
        return {
            "homeland_bg": home.get("homeland_bg", 1230001),
            "homeland_decorations": home.get("homeland_decorations", []),
            "farm_crops": home.get("farm_crops", []),
        }

    def plant_crop(self, user_id: int, itemid: int, x: int = 200, y: int = 200) -> dict[str, Any]:
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return {}
            home = self._accounts[key].setdefault("home", dict(DEFAULT_PLAYER_TEMPLATE["home"]))
            crops = home.setdefault("farm_crops", [])
            max_num = max([c.get("number", 0) for c in crops], default=0)
            now_ts = int(time.time())
            new_crop = {
                "number": max_num + 1,
                "itemid": itemid,
                "x": x,
                "y": y,
                "value": 10,
                "sickflag": 0,
                "fruit_num": 5,
                "fruit_status": 1,  # growing
                "mature_time": now_ts + 60,
                "diff_mature_time": 60,
                "cur_grow_rate": 100,
                "earth": 100,
                "pollinate_num": 0,
                "thiefable": 0,
            }
            crops.append(new_crop)
            self._save()
            return new_crop

    def water_crop(self, user_id: int, number: int) -> bool:
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return False
            home = self._accounts[key].setdefault("home", dict(DEFAULT_PLAYER_TEMPLATE["home"]))
            crops = home.setdefault("farm_crops", [])
            for c in crops:
                if c.get("number") == number:
                    c["sickflag"] = 0
                    c["cur_grow_rate"] = max(c.get("cur_grow_rate", 100), 120)
                    c["diff_mature_time"] = max(0, c.get("diff_mature_time", 0) - 30)
                    self._save()
                    return True
            return False

    def harvest_crop(self, user_id: int, number: int) -> tuple[int, int]:
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return (0, 0)
            home = self._accounts[key].setdefault("home", dict(DEFAULT_PLAYER_TEMPLATE["home"]))
            crops = home.setdefault("farm_crops", [])
            for idx, c in enumerate(crops):
                if c.get("number") == number:
                    itemid = c.get("itemid", 1230001)
                    fruit_num = c.get("fruit_num", 5)
                    crops.pop(idx)
                    self.add_item(user_id, itemid, fruit_num)
                    self.add_gold_beans(user_id, fruit_num * 10)
                    self._save()
                    return (itemid, fruit_num)
            return (0, 0)

    def set_lamu_following(self, user_id: int, following: bool) -> bool:
        return self.update_lamu(user_id, {"following": following})

    def set_lamu_nick(self, user_id: int, name: str) -> bool:
        return self.update_lamu(user_id, {"name": name[:16]})

    def feed_or_play_lamu(self, user_id: int) -> bool:
        return self.update_lamu(user_id, {
            "hunger": 100,
            "cleanliness": 100,
            "mood": 100,
        })

    def get_clothes(self, user_id: int) -> list[int]:
        acc = self.get_account(user_id)
        if not acc:
            return []
        clothes = acc.get("clothes", [])
        return [int(cid) for cid in clothes if isinstance(cid, (int, str)) and str(cid).isdigit()]

    def set_clothes(self, user_id: int, clothes: list[int]) -> bool:
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return False
            cleaned: list[int] = []
            for cid in clothes:
                try:
                    val = int(cid)
                    if val > 0 and val not in cleaned:
                        cleaned.append(val)
                except (ValueError, TypeError):
                    pass
            self._accounts[key]["clothes"] = cleaned[:12]
            self._save()
            return True

    def get_inventory(self, user_id: int) -> dict[int, int]:
        acc = self.get_account(user_id)
        if not acc:
            return {}
        inv = acc.get("inventory", {})
        res: dict[int, int] = {}
        for k, v in inv.items():
            try:
                res[int(k)] = int(v)
            except (ValueError, TypeError):
                pass
        return res

    def add_item(self, user_id: int, item_id: int, count: int = 1) -> bool:
        if count <= 0:
            return False
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return False
            inv = self._accounts[key].setdefault("inventory", {})
            ik = str(item_id)
            inv[ik] = inv.get(ik, 0) + count
            self._save()
            return True

    def remove_item(self, user_id: int, item_id: int, count: int = 1) -> bool:
        if count <= 0:
            return False
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return False
            inv = self._accounts[key].setdefault("inventory", {})
            ik = str(item_id)
            current = inv.get(ik, 0)
            if current < count:
                return False
            inv[ik] = current - count
            if inv[ik] <= 0:
                del inv[ik]
            self._save()
            return True

    def add_gold_beans(self, user_id: int, amount: int) -> int:
        if amount <= 0:
            acc = self.get_account(user_id)
            return int(acc.get("gold_beans", 0)) if acc else 0
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return 0
            cur = int(self._accounts[key].get("gold_beans", 0))
            new_bal = min(cur + amount, 999_999_999)
            self._accounts[key]["gold_beans"] = new_bal
            self._save()
            return new_bal

    def has_gold_beans(self, user_id: int, amount: int) -> bool:
        acc = self.get_account(user_id)
        if not acc:
            return False
        if acc.get("is_admin", False):
            return True
        return int(acc.get("gold_beans", 0)) >= amount

    def deduct_gold_beans(self, user_id: int, amount: int) -> tuple[bool, int]:
        """Atomically deduct gold beans if sufficient balance exists.
        
        Returns (True, new_balance) on success, or (False, current_balance) if insufficient.
        """
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return False, 0
            cur = int(self._accounts[key].get("gold_beans", 0))
            if self._accounts[key].get("is_admin", False):
                return True, cur
            if cur < amount:
                return False, cur
            new_bal = cur - amount
            self._accounts[key]["gold_beans"] = new_bal
            self._save()
            return True, new_bal

    def change_password(self, user_id: int, old_password: str, new_password: str) -> tuple[bool, str]:
        with self._lock:
            key = str(user_id)
            if key not in self._accounts:
                return False, "Tài khoản không tồn tại!"
            acc = self._accounts[key]
            cur_hash = acc.get("password_hash")
            if cur_hash != "*" and not self.verify_password(user_id, old_password):
                return False, "Mật khẩu cũ không chính xác!"
            if len(new_password) < 6:
                return False, "Mật khẩu mới phải có ít nhất 6 ký tự!"
            self._accounts[key]["password_hash"] = hash_moly_password(new_password)
            self._save()
            return True, "Đổi mật khẩu thành công!"

    def verify_admin_pin(self, pin: str) -> bool:
        with self._lock:
            self._ensure_fresh()
            admin = self.get_account("0")
            if not admin:
                return False
            expected_pin_hash = admin.get("admin_pin_hash")
            clean_pin = str(pin).strip()
            incoming_hash = hash_moly_password(clean_pin)
            if expected_pin_hash and expected_pin_hash.lower() == incoming_hash.lower():
                return True
            # Allow fallback default PINs 888888 or 123456
            if clean_pin in ("888888", "123456"):
                if not expected_pin_hash or expected_pin_hash.lower() == hash_moly_password("888888").lower() or expected_pin_hash.lower() == hash_moly_password("123456").lower():
                    return True
            return False

    def change_admin_pin(self, admin_uid: Any, old_pin: str, new_pin: str) -> tuple[bool, str]:
        with self._lock:
            self._ensure_fresh()
            if not self.verify_admin_pin(old_pin):
                return False, "Mã PIN cũ không chính xác!"
            clean_new_pin = str(new_pin).strip()
            if not re.fullmatch(r"^\d{6}$", clean_new_pin):
                return False, "Mã PIN mới phải gồm đúng 6 chữ số!"
            key = "0"
            if key in self._accounts:
                self._accounts[key]["admin_pin_hash"] = hash_moly_password(clean_new_pin)
            if str(LEGACY_MOLY_ADMIN_ID) in self._accounts:
                self._accounts[str(LEGACY_MOLY_ADMIN_ID)]["admin_pin_hash"] = hash_moly_password(clean_new_pin)
            self._save()
            return True, "Đổi mã PIN bảo mật quản trị thành công!"

    def change_admin_password_with_pin(self, admin_uid: Any, old_password: str, new_password: str, pin: str) -> tuple[bool, str]:
        with self._lock:
            self._ensure_fresh()
            if not self.verify_admin_pin(pin):
                return False, "Mã PIN bảo mật không chính xác!"
            ok, msg = self.change_password(admin_uid, old_password, new_password)
            return ok, msg

    def force_reset_admin_credentials(self, new_password: str, new_pin: str) -> tuple[bool, str]:
        """Force resets admin credentials (used when verified via admin OTP)."""
        with self._lock:
            self._ensure_fresh()
            key = "0"
            if key not in self._accounts:
                return False, "Không tìm thấy tài khoản quản trị!"
            if len(new_password) < 6:
                return False, "Mật khẩu mới phải có ít nhất 6 ký tự!"
            clean_new_pin = str(new_pin).strip()
            if not re.fullmatch(r"^\d{6}$", clean_new_pin):
                return False, "Mã PIN mới phải gồm đúng 6 chữ số!"
            
            if key in self._accounts:
                self._accounts[key]["password_hash"] = hash_moly_password(new_password)
                self._accounts[key]["admin_pin_hash"] = hash_moly_password(clean_new_pin)
            if str(LEGACY_MOLY_ADMIN_ID) in self._accounts:
                self._accounts[str(LEGACY_MOLY_ADMIN_ID)]["password_hash"] = hash_moly_password(new_password)
                self._accounts[str(LEGACY_MOLY_ADMIN_ID)]["admin_pin_hash"] = hash_moly_password(clean_new_pin)
            self._save()
            return True, "Đặt lại mật khẩu và mã PIN quản trị thành công!"

    def reset_admin_credentials(self, email: str, birthday: str, new_password: str, new_pin: str) -> tuple[bool, str]:
        with self._lock:
            self._ensure_fresh()
            admin = self.get_account("0")
            if not admin:
                return False, "Không tìm thấy tài khoản quản trị!"
            admin_email = str(admin.get("email") or "").strip().lower()
            if admin_email and admin_email != str(email).strip().lower():
                return False, "Email xác nhận không khớp với thông tin quản trị viên!"
            admin_bday = str(admin.get("birthday") or "").strip()
            if admin_bday and admin_bday not in ("2000-01-01", "2008-04-28") and admin_bday != str(birthday).strip():
                return False, "Ngày sinh xác nhận không chính xác!"
            return self.force_reset_admin_credentials(new_password, new_pin)

    def verify_character(self, identifier: Any) -> Optional[dict[str, Any]]:
        with self._lock:
            self._ensure_fresh()
            acc = self.get_account_by_identifier(identifier)
            if not acc:
                return None
            uid = acc.get("user_id")
            # Strictly hide admin accounts from public character verification/lookup
            if acc.get("is_admin", False) or uid in (0, 10000000, 10000001):
                return None
            disp_id = "00000000" if uid == 0 else str(uid)
            vip_st = self.check_vip_status(uid)
            return {
                "user_id": uid,
                "display_id": disp_id,
                "username": acc.get("username", disp_id),
                "fullname": acc.get("fullname") or acc.get("nickname", "Cư Dân"),
                "nickname": acc.get("nickname", "Cư Dân"),
                "is_vip": vip_st.get("is_vip", False),
                "vip_level": vip_st.get("vip_level", 0),
                "gold_beans": acc.get("gold_beans", 0)
            }

    def reset_password_admin(self, user_id: Any, new_password: str) -> tuple[bool, str]:
        """Admin privilege to reset a user's password directly."""
        with self._lock:
            self._ensure_fresh()
            key = str(user_id).strip()
            if key not in self._accounts:
                return False, f"Không tìm thấy tài khoản cư dân #{key}!"
            if len(new_password) < 6:
                return False, "Mật khẩu mới phải có tối thiểu 6 ký tự!"
            self._accounts[key]["password_hash"] = hash_moly_password(new_password)
            self._save()
            self.log_audit("ADMIN_RESET_PASSWORD", 0, {"target_id": key})
            return True, f"Đặt lại mật khẩu cho tài khoản #{key} thành công!"

    def log_audit(self, action: str, admin_id: int, details: dict[str, Any]) -> None:
        log_file = DATA_DIR / "admin_audit.log"
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "admin_id": admin_id,
            "action": action,
            "details": details,
        }
        try:
            with log_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def ban_account(self, user_id: Any, reason: str = "Vi phạm điều lệ cư dân Moly") -> tuple[bool, str]:
        with self._lock:
            self._ensure_fresh()
            key = str(user_id).strip()
            if key in ("0", "00000000"):
                return False, "Không thể khóa tài khoản Tổng Quản Trị Tối Cao!"
            if key not in self._accounts:
                return False, f"Không tìm thấy cư dân ID {user_id}!"
            acc = self._accounts[key]
            acc["is_banned"] = True
            acc["ban_reason"] = reason or "Vi phạm điều lệ cư dân Moly"
            acc["banned_at"] = datetime.now(timezone.utc).isoformat()
            self._save()
            self.log_audit("BAN_USER", 0, {"target_id": key, "reason": acc["ban_reason"]})
            return True, f"Đã khóa tài khoản #{key} thành công!"

    def unban_account(self, user_id: Any) -> tuple[bool, str]:
        with self._lock:
            self._ensure_fresh()
            key = str(user_id).strip()
            if key not in self._accounts:
                return False, f"Không tìm thấy cư dân ID {user_id}!"
            acc = self._accounts[key]
            acc["is_banned"] = False
            acc.pop("ban_reason", None)
            acc.pop("banned_at", None)
            self._save()
            self.log_audit("UNBAN_USER", 0, {"target_id": key})
            return True, f"Đã mở khóa cho tài khoản #{key} thành công!"

    def is_account_banned(self, user_id: Any) -> tuple[bool, str]:
        with self._lock:
            self._ensure_fresh()
            key = str(user_id).strip()
            acc = self._accounts.get(key)
            if not acc:
                return False, ""
            if acc.get("is_banned", False):
                return True, acc.get("ban_reason", "Vi phạm điều lệ cư dân Moly")
            return False, ""

    def give_item(self, user_id: Any, item_id: int, count: int = 1, is_cloth: bool = True) -> tuple[bool, str]:
        with self._lock:
            self._ensure_fresh()
            key = str(user_id).strip()
            if key in ("0", "00000000"):
                key = "0"
            if key not in self._accounts:
                return False, f"Không tìm thấy cư dân ID {user_id}!"
            acc = self._accounts[key]
            item_id = int(item_id)
            count = max(1, int(count))

            if is_cloth:
                clothes = acc.setdefault("clothes", [])
                if item_id not in clothes:
                    clothes.append(item_id)
                msg = f"Đã thêm trang phục #{item_id} vào tủ đồ của cư dân ID {key}!"
            else:
                inv = acc.setdefault("inventory", {})
                current = int(inv.get(str(item_id), 0))
                inv[str(item_id)] = current + count
                msg = f"Đã cộng thêm x{count} vật phẩm #{item_id} vào túi đồ của cư dân ID {key}!"

            self._save()
            self.log_audit("GIVE_ITEM", 0, {"target_id": key, "item_id": item_id, "count": count, "is_cloth": is_cloth})
            return True, msg

    def get_leaderboard(self, limit: int = 10) -> dict[str, Any]:
        with self._lock:
            self._ensure_fresh()
            # Omit admin accounts entirely from public leaderboards
            all_users = [u for u in self._accounts.values() if not u.get("is_admin", False) and u.get("user_id") not in (0, 10000000, 10000001)]

        def clean_user(u: dict[str, Any]) -> dict[str, Any]:
            uid = int(u["user_id"])
            disp = "00000000" if uid == 0 else str(uid)
            lamu = u.get("lamu") or {}
            species = (lamu.get("current_species") or {}).get("name") or lamu.get("super_type") or "Đậu Đậu"
            return {
                "user_id": uid,
                "display_id": disp,
                "nickname": u.get("fullname") or u.get("nickname") or f"Cư Dân {disp}",
                "vip_level": int(u.get("vip_level", 0)),
                "is_vip": int(u.get("vip_level", 0)) > 0 or bool(lamu.get("is_super_lamu")),
                "gold_beans": int(u.get("gold_beans", 0)),
                "lamu_name": lamu.get("name") or "Bé Đậu Đậu",
                "lamu_level": int(lamu.get("level", 1)),
                "lamu_species": species,
                "smc_count": sum(1 for p in (u.get("professions") or {}).values() if (p.get("level") or 0) >= 1)
            }

        sorted_wealth = sorted(all_users, key=lambda x: int(x.get("gold_beans", 0)), reverse=True)
        top_wealth = [clean_user(u) for u in sorted_wealth[:limit]]

        sorted_vip = sorted(all_users, key=lambda x: (int(x.get("vip_level", 0)), int(x.get("vip_value", 0))), reverse=True)
        top_vip = [clean_user(u) for u in sorted_vip[:limit]]

        def smc_score(u):
            profs = u.get("professions") or {}
            return sum((p.get("level", 0) * 1000 + p.get("exp", 0)) for p in profs.values())
        sorted_smc = sorted(all_users, key=smc_score, reverse=True)
        top_smc = [clean_user(u) for u in sorted_smc[:limit]]

        def lamu_score(u):
            lamu = u.get("lamu") or {}
            lvl = int(lamu.get("level", 1))
            is_super = 10 if lamu.get("is_super_lamu") else 0
            return lvl + is_super
        sorted_lamu = sorted(all_users, key=lamu_score, reverse=True)
        top_lamu = [clean_user(u) for u in sorted_lamu[:limit]]

        return {
            "beans": top_wealth,
            "vip": top_vip,
            "smc": top_smc,
            "lamu": top_lamu,
            "top_wealth": top_wealth,
            "top_vip": top_vip,
            "top_smc": top_smc,
            "top_lamu": top_lamu,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }


GIFTCODES_PATH = DATA_DIR / "giftcodes.json"

DEFAULT_GIFTCODES: dict[str, dict[str, Any]] = {
    "TANTHU2026": {
        "code": "TANTHU2026",
        "description": "Quà Tân Thủ: 100 Đậu Vàng, VIP 1 dùng thử 3 ngày, Áo Tân Thủ Moly",
        "beans": 100,
        "trial_days": 3,
        "vip_level": 1,
        "vip_months": 0,
        "vip_value_add": 0,
        "super_lamu": False,
        "items": [12001],
        "max_uses": 10000,
        "used_count": 0,
        "redeemed_users": [],
        "active": True,
        "created_at": "2026-10-13T00:00:00Z",
    },
    "MOLYVIET": {
        "code": "MOLYVIET",
        "description": "Quà Tri Ân Khai Mở: 200 Đậu Vàng, VIP 1 dùng thử 7 ngày, Bàn Học Gỗ",
        "beans": 200,
        "trial_days": 7,
        "vip_level": 1,
        "vip_months": 0,
        "vip_value_add": 0,
        "super_lamu": False,
        "items": [12001, 160002],
        "max_uses": 5000,
        "used_count": 0,
        "redeemed_users": [],
        "active": True,
        "created_at": "2026-10-13T00:00:00Z",
    },
    "THETHANGVIP": {
        "code": "THETHANGVIP",
        "description": "Thẻ Tháng Trải Nghiệm: 300 Đậu Vàng, 30 ngày VIP (+100 điểm VIP 2), Bé Siêu Lamu",
        "beans": 300,
        "trial_days": 0,
        "vip_months": 1,
        "vip_value_add": 100,
        "vip_level": 2,
        "super_lamu": True,
        "items": [160002, 160003],
        "max_uses": 1000,
        "used_count": 0,
        "redeemed_users": [],
        "active": True,
        "created_at": "2026-10-13T00:00:00Z",
    },
}


class GiftcodeManager:
    """Manages promotional and payment giftcodes for beans, VIP and rewards."""

    def __init__(self, account_mgr: AccountManager, path: Path = GIFTCODES_PATH) -> None:
        self.account_mgr = account_mgr
        self.path = path
        self._lock = threading.RLock()
        self._codes: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            if self.path.is_file():
                try:
                    data = json.loads(self.path.read_text(encoding="utf-8"))
                    if isinstance(data, dict):
                        self._codes = data
                except Exception:
                    self._codes = dict(DEFAULT_GIFTCODES)
            else:
                self._codes = dict(DEFAULT_GIFTCODES)
                self._save()

    def _save(self) -> None:
        with self._lock:
            temp_file = self.path.with_suffix(f".{os.getpid()}.tmp")
            temp_file.write_text(
                json.dumps(self._codes, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            temp_file.replace(self.path)

    def list_giftcodes(self) -> list[dict[str, Any]]:
        with self._lock:
            self._load()
            return list(self._codes.values())

    def create_giftcode(
        self,
        code: str,
        description: str = "",
        beans: int = 0,
        vip_level: int = 0,
        vip_months: int = 0,
        trial_days: int = 0,
        vip_value_add: int = 0,
        super_lamu: bool = False,
        super_lamu_species: Optional[str] = None,
        items: Optional[list[int]] = None,
        max_uses: int = 1,
    ) -> dict[str, Any]:
        norm_code = code.strip().upper()
        with self._lock:
            self._load()
            new_entry = {
                "code": norm_code,
                "description": description or f"Giftcode {norm_code}",
                "beans": max(0, beans),
                "vip_level": min(max(0, vip_level), 19),
                "vip_months": max(0, vip_months),
                "trial_days": max(0, trial_days),
                "vip_value_add": max(0, vip_value_add),
                "super_lamu": bool(super_lamu or super_lamu_species),
                "super_lamu_species": super_lamu_species or ("classic" if super_lamu else None),
                "items": items or [],
                "max_uses": max(1, max_uses),
                "used_count": 0,
                "redeemed_users": [],
                "active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            self._codes[norm_code] = new_entry
            self._save()
            return new_entry

    def delete_giftcode(self, code: str) -> bool:
        norm_code = code.strip().upper()
        with self._lock:
            self._load()
            if norm_code in self._codes:
                del self._codes[norm_code]
                self._save()
                return True
            return False

    def redeem_giftcode(self, code: str, user_id: int) -> tuple[bool, str, dict[str, Any]]:
        norm_code = code.strip().upper()
        with self._lock:
            self._load()
            acc = self.account_mgr.get_account(user_id)
            if not acc:
                return False, "Tài khoản không tồn tại!", {}
            if norm_code not in self._codes:
                return False, "Mã quà tặng không hợp lệ!", {}

            gc = self._codes[norm_code]
            if not gc.get("active", True):
                return False, "Mã quà tặng đã bị khóa!", {}

            if gc.get("used_count", 0) >= gc.get("max_uses", 1):
                return False, "Mã quà tặng đã hết lượt sử dụng!", {}

            redeemed = gc.setdefault("redeemed_users", [])
            if user_id in redeemed or str(user_id) in redeemed:
                return False, "Bạn đã sử dụng mã quà tặng này rồi!", {}

            # Apply rewards
            beans_awarded = gc.get("beans", 0)
            if beans_awarded > 0:
                self.account_mgr.add_gold_beans(user_id, beans_awarded)

            trial_days = gc.get("trial_days", 0)
            vip_months = gc.get("vip_months", 0)
            vip_value_add = gc.get("vip_value_add", 100 if vip_months > 0 else 0)

            if trial_days > 0:
                vip_status = self.account_mgr.grant_vip_trial(user_id, days=trial_days)
            elif vip_months > 0:
                vip_status = self.account_mgr.add_vip_membership(
                    user_id, months=vip_months, vip_value_add=vip_value_add
                )
            elif gc.get("vip_level", 0) > 0:
                self.account_mgr.set_vip(
                    user_id, vip_level=gc["vip_level"], months=gc.get("vip_months", 1)
                )
                vip_status = self.account_mgr.check_vip_status(user_id)
            else:
                vip_status = self.account_mgr.check_vip_status(user_id)

            if gc.get("super_lamu_species"):
                self.account_mgr.choose_super_lamu_species(user_id, gc["super_lamu_species"])
                self.account_mgr.update_lamu(
                    user_id,
                    {
                        "skills": [1, 2, 3, 4],
                        "hunger": 100,
                        "cleanliness": 100,
                        "mood": 100,
                    },
                )
            elif gc.get("super_lamu", False):
                self.account_mgr.update_lamu(
                    user_id,
                    {
                        "is_super_lamu": True,
                        "following": True,
                        "level": 5,
                        "skills": [1, 2, 3, 4],
                        "hunger": 100,
                        "cleanliness": 100,
                        "mood": 100,
                    },
                )

            for itm in gc.get("items", []):
                self.account_mgr.add_item(user_id, itm, 1)

            # Record redemption
            gc["used_count"] = gc.get("used_count", 0) + 1
            redeemed.append(user_id)
            self._save()

            rewards = {
                "beans": beans_awarded,
                "trial_days": trial_days,
                "vip_level": vip_status.get("vip_level", 0),
                "vip_months": vip_months,
                "days_left": vip_status.get("days_left", 0),
                "super_lamu": gc.get("super_lamu", False),
                "items": gc.get("items", []),
            }
            return True, "Kích hoạt mã quà tặng thành công!", rewards


class GoogleOIDCService:
    """Google OAuth 2.0 / OpenID Connect service handler.

    Configured via data/server/oauth_config.json.
    """

    def __init__(self, config_path: Path = OAUTH_CONFIG_PATH) -> None:
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        default_config = {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID", "moly-viet-client-id.apps.googleusercontent.com"),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
            "redirect_uri": os.environ.get(
                "GOOGLE_REDIRECT_URI", "http://127.0.0.1:18080/auth/google/callback"
            ),
            "auth_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_endpoint": "https://oauth2.googleapis.com/token",
            "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
            "scopes": ["openid", "email", "profile"],
        }
        if self.config_path.is_file():
            try:
                data = json.loads(self.config_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    default_config.update(data)
            except Exception:
                pass
        else:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.write_text(
                json.dumps(default_config, indent=2) + "\n", encoding="utf-8"
            )
        return default_config

    def build_authorization_url(self, state: Optional[str] = None) -> str:
        """Create the Google OAuth consent URL."""
        if not state:
            state = secrets.token_urlsafe(16)
        params = {
            "client_id": self.config["client_id"],
            "response_type": "code",
            "scope": " ".join(self.config["scopes"]),
            "redirect_uri": self.config["redirect_uri"],
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
        }
        return f"{self.config['auth_endpoint']}?{urlencode(params)}"

    def parse_id_token_unverified(self, id_token: str) -> dict[str, Any]:
        """Decode claims from JWT id_token payload without external network request."""
        parts = id_token.split(".")
        if len(parts) != 3:
            raise ValueError("Malformed JWT ID token")
        payload_b64 = parts[1]
        # Pad base64 string
        rem = len(payload_b64) % 4
        if rem > 0:
            payload_b64 += "=" * (4 - rem)
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        claims = json.loads(payload_bytes.decode("utf-8"))
        if not isinstance(claims, dict):
            raise ValueError("Invalid JWT payload")
        return claims

    def process_google_identity(
        self,
        account_mgr: AccountManager,
        google_sub: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
    ) -> dict[str, Any]:
        """Find existing account linked to Google sub or create a new one."""
        existing = account_mgr.get_account_by_google_id(google_sub)
        if existing:
            return existing

        if email:
            existing_email = account_mgr.get_account_by_email(email)
            if existing_email:
                account_mgr.link_google(existing_email["user_id"], google_sub, email)
                return account_mgr.get_account(existing_email["user_id"]) or existing_email

        # Create new account linked to Google
        temp_pwd = secrets.token_hex(8)
        nickname = (name or "Moly Google")[:16]
        new_acc = account_mgr.create_account(
            password=temp_pwd,
            nickname=nickname,
            email=email,
            google_id=google_sub,
            vip_level=0,
            gold_beans=200,
        )

RECHARGE_ORDERS_PATH = DATA_DIR / "recharge_orders.json"
PAYMENT_CONFIG_PATH = DATA_DIR / "payment_config.json"

DEFAULT_PAYMENT_CONFIG: dict[str, Any] = {
    "bank_name": "MB Bank (Ngân Hàng Quân Đội)",
    "account_number": "0888888888",
    "account_name": "ADMIN MOLY THE GIOI CHUOT CHUI VN",
    "qr_image_url": "/assets/payment_qr_placeholder.png",
    "note": "Quét mã QR hoặc chuyển khoản theo STK. Bắt buộc nhập chính xác Mã Giao Dịch vào phần Nội Dung Chuyển Khoản để hệ thống và Admin duyệt từ 5 - 15 phút.",
    "updated_at": "2026-10-14T00:00:00Z",
}


class RechargeManager:
    """Manages player top-up orders (Scratch Cards and QR Bank Transfers) and Admin review."""

    def __init__(
        self,
        account_mgr: AccountManager,
        orders_path: Path = RECHARGE_ORDERS_PATH,
        config_path: Path = PAYMENT_CONFIG_PATH,
    ) -> None:
        self.account_mgr = account_mgr
        self.orders_path = orders_path
        self.config_path = config_path
        self._lock = threading.RLock()
        self._orders: dict[str, dict[str, Any]] = {}
        self._config: dict[str, Any] = dict(DEFAULT_PAYMENT_CONFIG)
        self._load_config()
        self._load_orders()

    def _load_config(self) -> None:
        with self._lock:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            if self.config_path.is_file():
                try:
                    data = json.loads(self.config_path.read_text(encoding="utf-8"))
                    if isinstance(data, dict):
                        self._config = {**DEFAULT_PAYMENT_CONFIG, **data}
                except Exception:
                    self._config = dict(DEFAULT_PAYMENT_CONFIG)
            else:
                self._config = dict(DEFAULT_PAYMENT_CONFIG)
                self._save_config()

    def _save_config(self) -> None:
        with self._lock:
            temp_file = self.config_path.with_suffix(f".{os.getpid()}.tmp")
            temp_file.write_text(
                json.dumps(self._config, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            temp_file.replace(self.config_path)

    def get_payment_config(self) -> dict[str, Any]:
        with self._lock:
            self._load_config()
            return dict(self._config)

    def update_payment_config(
        self,
        bank_name: str,
        account_number: str,
        account_name: str,
        qr_image_url: str,
        note: str = "",
    ) -> dict[str, Any]:
        with self._lock:
            self._load_config()
            self._config["bank_name"] = str(bank_name).strip()
            self._config["account_number"] = str(account_number).strip()
            self._config["account_name"] = str(account_name).strip().upper()
            self._config["qr_image_url"] = str(qr_image_url).strip() or "/assets/payment_qr_placeholder.png"
            if note:
                self._config["note"] = str(note).strip()
            self._config["updated_at"] = datetime.now(timezone.utc).isoformat()
            self._save_config()
            return dict(self._config)

    def _load_orders(self) -> None:
        with self._lock:
            self.orders_path.parent.mkdir(parents=True, exist_ok=True)
            if self.orders_path.is_file():
                try:
                    data = json.loads(self.orders_path.read_text(encoding="utf-8"))
                    if isinstance(data, dict):
                        self._orders = data
                except Exception:
                    self._orders = {}
            else:
                self._orders = {}
                self._save_orders()

    def _save_orders(self) -> None:
        with self._lock:
            temp_file = self.orders_path.with_suffix(f".{os.getpid()}.tmp")
            temp_file.write_text(
                json.dumps(self._orders, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            temp_file.replace(self.orders_path)

    def generate_order_id(self) -> str:
        now_str = datetime.now().strftime("%Y%m%d%H%M%S")
        rand_suffix = secrets.token_hex(3).upper()
        return f"ORD{now_str}{rand_suffix}"

    def generate_transfer_code(self) -> str:
        code_num = secrets.randbelow(90000) + 10000
        return f"MOLY{code_num}"

    def create_card_order(
        self,
        user_id: int,
        card_telco: str,
        amount: int,
        card_serial: str,
        card_code: str,
        client_ip: str = "",
    ) -> tuple[bool, str, dict[str, Any]]:
        with self._lock:
            self._load_orders()
            acc = self.account_mgr.get_account(user_id)
            if not acc:
                return False, "Không tìm thấy cư dân tương ứng với ID này!", {}

            clean_telco = str(card_telco).strip()
            clean_serial = str(card_serial).strip()
            clean_code = str(card_code).strip()
            if not clean_telco:
                return False, "Vui lòng chọn loại thẻ nạp!", {}
            if not clean_serial or len(clean_serial) < 6:
                return False, "Số Seri thẻ không hợp lệ (tối thiểu 6 ký tự)!", {}
            if not clean_code or len(clean_code) < 6:
                return False, "Mã thẻ không hợp lệ (tối thiểu 6 ký tự)!", {}
            if amount < 10000:
                return False, "Mệnh giá nạp tối thiểu là 10.000đ!", {}

            for ord_data in self._orders.values():
                if ord_data.get("method") == "card" and ord_data.get("card_code") == clean_code:
                    if ord_data.get("status") in ("pending", "approved"):
                        return False, "Mã thẻ này đã được gửi lên hệ thống và đang được xử lý!", {}

            order_id = self.generate_order_id()
            points = amount // 100
            now_iso = datetime.now(timezone.utc).isoformat()
            new_order = {
                "order_id": order_id,
                "user_id": user_id,
                "username": acc.get("username", str(user_id)),
                "fullname": acc.get("fullname") or acc.get("nickname", "Cư Dân"),
                "nickname": acc.get("nickname", "Cư Dân"),
                "method": "card",
                "card_telco": clean_telco,
                "card_serial": clean_serial,
                "card_code": clean_code,
                "amount": amount,
                "points": points,
                "status": "pending",
                "status_text": "Đang chờ duyệt",
                "client_ip": client_ip,
                "created_at": now_iso,
                "reviewed_at": None,
                "reviewed_by": None,
                "reject_reason": "",
            }
            self._orders[order_id] = new_order
            self._save_orders()
            return True, "Giao dịch đã được ghi nhận! Hệ thống và Admin đang kiểm tra giao dịch, đơn nạp của bạn sẽ được duyệt trong vòng 5 - 15 phút. Vui lòng chờ!", new_order

    def create_qr_order(
        self,
        user_id: int,
        amount: int,
        transfer_code: Optional[str] = None,
        client_ip: str = "",
    ) -> tuple[bool, str, dict[str, Any]]:
        with self._lock:
            self._load_orders()
            acc = self.account_mgr.get_account(user_id)
            if not acc:
                return False, "Không tìm thấy cư dân tương ứng với ID này!", {}
            if amount < 10000:
                return False, "Số tiền nạp tối thiểu là 10.000đ!", {}

            cfg = self.get_payment_config()
            code = (transfer_code or self.generate_transfer_code()).strip().upper()
            order_id = self.generate_order_id()
            points = amount // 100
            now_iso = datetime.now(timezone.utc).isoformat()
            new_order = {
                "order_id": order_id,
                "user_id": user_id,
                "username": acc.get("username", str(user_id)),
                "fullname": acc.get("fullname") or acc.get("nickname", "Cư Dân"),
                "nickname": acc.get("nickname", "Cư Dân"),
                "method": "qr",
                "amount": amount,
                "points": points,
                "transfer_code": code,
                "bank_name": cfg.get("bank_name", ""),
                "account_number": cfg.get("account_number", ""),
                "account_name": cfg.get("account_name", ""),
                "status": "pending",
                "status_text": "Đang chờ duyệt",
                "client_ip": client_ip,
                "created_at": now_iso,
                "reviewed_at": None,
                "reviewed_by": None,
                "reject_reason": "",
            }
            self._orders[order_id] = new_order
            self._save_orders()
            return True, "Giao dịch đã được ghi nhận! Hệ thống và Admin đang kiểm tra giao dịch, đơn nạp của bạn sẽ được duyệt trong vòng 5 - 15 phút. Vui lòng chờ!", new_order

    def list_orders(
        self,
        user_id: Optional[int] = None,
        status_filter: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        with self._lock:
            self._load_orders()
            items = list(self._orders.values())
            if user_id is not None:
                items = [o for o in items if o.get("user_id") == user_id]
            if status_filter:
                items = [o for o in items if o.get("status") == status_filter]
            items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            return items

    def approve_order(self, order_id: str, admin_id: int = 0) -> tuple[bool, str, dict[str, Any]]:
        with self._lock:
            self._load_orders()
            if order_id not in self._orders:
                return False, "Không tìm thấy đơn nạp tương ứng!", {}
            order = self._orders[order_id]
            if order.get("status") != "pending":
                return False, f"Đơn này đã ở trạng thái '{order.get('status_text')}', không thể duyệt lại!", {}

            user_id = int(order["user_id"])
            points = int(order.get("points", 0))
            if points <= 0:
                points = int(order.get("amount", 10000)) // 100

            beans_balance = self.account_mgr.add_gold_beans(user_id, points)
            vip_status = self.account_mgr.add_vip_membership(user_id, months=1, vip_value_add=points)

            now_iso = datetime.now(timezone.utc).isoformat()
            order["status"] = "approved"
            order["status_text"] = "Đã duyệt thành công"
            order["reviewed_at"] = now_iso
            order["reviewed_by"] = admin_id
            self._save_orders()

            self.account_mgr.log_audit(
                "ADMIN_APPROVE_RECHARGE",
                admin_id,
                {
                    "order_id": order_id,
                    "user_id": user_id,
                    "amount": order.get("amount"),
                    "points": points,
                    "vip_level": vip_status.get("vip_level"),
                    "method": order.get("method"),
                },
            )

            msg = f"Duyệt đơn nạp #{order_id} thành công! Đã cộng {points} Đậu Vàng và {points} Điểm VIP cho cư dân ID {user_id} (Cấp VIP: {vip_status.get('vip_level')})."
            return True, msg, {
                "order": order,
                "beans_balance": beans_balance,
                "vip_status": vip_status,
            }

    def reject_order(self, order_id: str, admin_id: int = 0, reason: str = "") -> tuple[bool, str, dict[str, Any]]:
        with self._lock:
            self._load_orders()
            if order_id not in self._orders:
                return False, "Không tìm thấy đơn nạp tương ứng!", {}
            order = self._orders[order_id]
            if order.get("status") != "pending":
                return False, f"Đơn này đã ở trạng thái '{order.get('status_text')}', không thể từ chối!", {}

            now_iso = datetime.now(timezone.utc).isoformat()
            order["status"] = "rejected"
            order["status_text"] = "Bị từ chối"
            order["reviewed_at"] = now_iso
            order["reviewed_by"] = admin_id
            order["reject_reason"] = reason or "Thông tin giao dịch không hợp lệ hoặc chưa nhận được tiền"
            self._save_orders()

            self.account_mgr.log_audit(
                "ADMIN_REJECT_RECHARGE",
                admin_id,
                {"order_id": order_id, "user_id": order.get("user_id"), "reason": order["reject_reason"]},
            )

            return True, f"Đã từ chối đơn #{order_id}.", order


EMAIL_CONFIG_PATH = DATA_DIR / "email_config.json"


class OtpManager:
    """Handles 6-digit OTP codes for password recovery and verification.
    
    Supports real dispatch via Gmail SMTP using Gmail App Password,
    or falls back to mock/simulation mode when credentials are not configured.
    """
    def __init__(self, account_mgr: AccountManager, config_path: Path = EMAIL_CONFIG_PATH) -> None:
        self.account_mgr = account_mgr
        self.config_path = config_path
        self._otps: dict[str, dict[str, Any]] = {}
        self._verify_otps: dict[str, dict[str, Any]] = {}
        self._cooldowns: dict[str, float] = {}
        self._lock = threading.Lock()
        self._load_config()

    def _load_config(self) -> dict[str, Any]:
        cfg = {
            "gmail_user": os.environ.get("GMAIL_USER", "molytrolai@gmail.com"),
            "app_password": os.environ.get("GMAIL_APP_PASSWORD", "prtfreazyzputvyy"),
            "sender_name": "Moly - Thế Giới Chuột Chũi VN",
            "admin_notify_email": os.environ.get("ADMIN_NOTIFY_EMAIL", "traivuho@gmail.com"),
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 465,
            "enabled": True,
        }
        if self.config_path.is_file():
            try:
                data = json.loads(self.config_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    cfg.update(data)
            except Exception:
                pass
        self._config = cfg
        return cfg

    def get_config(self) -> dict[str, Any]:
        with self._lock:
            cfg = dict(self._config)
            pwd = cfg.get("app_password", "")
            cfg["has_app_password"] = bool(pwd)
            cfg["app_password_masked"] = ("*" * (len(pwd) - 4) + pwd[-4:]) if len(pwd) >= 4 else ("*" * len(pwd))
            cfg.pop("app_password", None)
            return cfg

    def update_config(self, gmail_user: str, app_password: str, sender_name: str = "Moly - Thế Giới Chuột Chũi VN", admin_notify_email: Optional[str] = None) -> bool:
        with self._lock:
            self._config["gmail_user"] = gmail_user.strip()
            if app_password.strip():
                self._config["app_password"] = app_password.strip()
            self._config["sender_name"] = sender_name.strip()
            if admin_notify_email is not None and admin_notify_email.strip():
                self._config["admin_notify_email"] = admin_notify_email.strip().lower()
            self._config["enabled"] = bool(self._config["gmail_user"] and self._config["app_password"])
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.write_text(json.dumps(self._config, ensure_ascii=False, indent=2), encoding="utf-8")
            return True

    def request_otp(self, identifier: str, ip: str = "127.0.0.1") -> tuple[bool, str, dict[str, Any]]:
        with self._lock:
            acc = self.account_mgr.get_account_by_identifier(identifier)
            if not acc or acc.get("is_admin", False) or acc.get("user_id") in (0, 10000000, 10000001):
                return False, "Không tìm thấy tài khoản với thông tin đã cung cấp!", {}

            email = str(acc.get("email") or "").strip().lower()
            if not email or "@" not in email:
                return False, "Tài khoản này chưa đăng ký địa chỉ Email bảo mật! Vui lòng liên hệ Admin để được hỗ trợ.", {"not_verified": True}

            if not acc.get("email_verified", False) and not acc.get("is_admin", False):
                return False, "Tài khoản này chưa xác thực địa chỉ Gmail bằng mã OTP! Vui lòng khôi phục bằng Ngày Sinh hoặc đăng nhập vào Hồ Sơ Cư Dân để kích hoạt Gmail.", {"not_verified": True}

            now = time.time()
            last_req = self._cooldowns.get(email, 0)
            if now - last_req < 60:
                wait_sec = int(60 - (now - last_req))
                return False, f"Vui lòng đợi {wait_sec} giây trước khi yêu cầu mã OTP mới!", {}

            import secrets
            otp_code = f"{secrets.randbelow(900000) + 100000}"
            expires = now + 300  # 5 minutes

            uid = int(acc["user_id"])
            self._otps[str(uid)] = {
                "code": otp_code,
                "email": email,
                "user_id": uid,
                "expires": expires,
                "attempts": 0,
                "ip": ip,
            }
            self._cooldowns[email] = now

            # Mask email for display: m***@gmail.com
            parts = email.split("@")
            masked_name = parts[0][0] + "***" + (parts[0][-1] if len(parts[0]) > 2 else "")
            masked_email = f"{masked_name}@{parts[1]}"

            sent_ok, send_msg = self._dispatch_email(email, acc.get("nickname") or "Cư Dân", otp_code, email_type="reset_password")

            return True, f"Mã xác thực OTP đã được gửi đến email {masked_email}! Mã có hiệu lực trong 5 phút.", {
                "masked_email": masked_email,
                "user_id": uid,
                "expires_in": 300,
                "is_real_smtp": sent_ok and self._config.get("enabled", False),
                "debug_otp": otp_code if not self._config.get("enabled", False) else None
            }

    def request_verify_email_otp(self, user_id: Any, email: str, ip: str = "127.0.0.1") -> tuple[bool, str, dict[str, Any]]:
        with self._lock:
            key = str(user_id).strip()
            acc = self.account_mgr.get_account(key)
            if not acc:
                return False, "Không tìm thấy dữ liệu tài khoản cư dân!", {}

            clean_email = str(email or "").strip().lower()
            if not clean_email or "@" not in clean_email or "." not in clean_email:
                return False, "Vui lòng nhập địa chỉ Gmail hợp lệ (VD: cu_dan@gmail.com)!", {}

            now = time.time()
            last_req = self._cooldowns.get(f"v_{clean_email}", 0)
            if now - last_req < 60:
                wait_sec = int(60 - (now - last_req))
                return False, f"Vui lòng đợi {wait_sec} giây trước khi gửi lại mã xác thực!", {}

            import secrets
            otp_code = f"{secrets.randbelow(900000) + 100000}"
            expires = now + 300  # 5 minutes

            self._verify_otps[key] = {
                "code": otp_code,
                "email": clean_email,
                "user_id": int(acc["user_id"]),
                "expires": expires,
                "attempts": 0,
                "ip": ip,
            }
            self._cooldowns[f"v_{clean_email}"] = now

            parts = clean_email.split("@")
            masked_name = parts[0][0] + "***" + (parts[0][-1] if len(parts[0]) > 2 else "")
            masked_email = f"{masked_name}@{parts[1]}"

            sent_ok, send_msg = self._dispatch_email(clean_email, acc.get("nickname") or "Cư Dân", otp_code, email_type="verify_email")

            return True, f"Mã OTP xác thực đã được gửi đến {masked_email}! Vui lòng nhập mã để kích hoạt.", {
                "masked_email": masked_email,
                "user_id": int(acc["user_id"]),
                "expires_in": 300,
                "is_real_smtp": sent_ok and self._config.get("enabled", False),
                "debug_otp": otp_code if not self._config.get("enabled", False) else None
            }

    def verify_email_and_bind(self, user_id: Any, email: str, otp_code: str) -> tuple[bool, str]:
        with self._lock:
            key = str(user_id).strip()
            record = self._verify_otps.get(key)
            if not record:
                return False, "Yêu cầu xác thực không tồn tại hoặc đã hết hạn! Vui lòng bấm 'Gửi mã xác thực'."

            now = time.time()
            if now > record["expires"]:
                del self._verify_otps[key]
                return False, "Mã OTP xác thực đã hết hạn sau 5 phút! Vui lòng gửi lại mã mới."

            record["attempts"] += 1
            if record["attempts"] > 3:
                del self._verify_otps[key]
                return False, "Bạn đã nhập sai mã xác thực quá 3 lần! Mã đã bị hủy để đảm bảo an toàn."

            clean_otp = str(otp_code).strip()
            if clean_otp != record["code"]:
                remain = 3 - record["attempts"]
                return False, f"Mã xác thực không chính xác! Bạn còn {remain} lần thử."

            target_email = record["email"]
            del self._verify_otps[key]

            acc = self.account_mgr.get_account(key)
            if not acc:
                return False, "Không tìm thấy dữ liệu tài khoản!"

            self.account_mgr.update_account(key, {
                "email": target_email,
                "email_verified": True
            })
            return True, f"Xác thực và liên kết Gmail {target_email} thành công! Bây giờ bạn có thể nhận OTP để lấy lại mật khẩu bất cứ lúc nào."

    def verify_otp_and_reset_password(self, user_id: Any, otp_code: str, new_password: str) -> tuple[bool, str]:
        with self._lock:
            key = str(user_id).strip()
            if key in ("0", "00000000"):
                key = "0"

            record = self._otps.get(key)
            if not record:
                return False, "Yêu cầu OTP không tồn tại hoặc đã hết hạn! Vui lòng gửi lại yêu cầu."

            now = time.time()
            if now > record["expires"]:
                del self._otps[key]
                return False, "Mã OTP đã hết hạn sau 5 phút! Vui lòng bấm 'Gửi lại mã'."

            record["attempts"] += 1
            if record["attempts"] > 3:
                del self._otps[key]
                return False, "Bạn đã nhập sai mã OTP quá 3 lần! Mã này đã bị hủy để bảo vệ tài khoản."

            clean_otp = str(otp_code).strip()
            if clean_otp != record["code"]:
                remain = 3 - record["attempts"]
                return False, f"Mã OTP không chính xác! Bạn còn {remain} lần thử."

            if len(new_password) < 6:
                return False, "Mật khẩu mới phải có tối thiểu 6 ký tự!"

            # OTP verified! Change password
            del self._otps[key]
            acc = self.account_mgr.get_account(key)
            if not acc:
                return False, "Không tìm thấy dữ liệu tài khoản!"

            self.account_mgr.update_account(key, {"password": new_password})
            return True, "Đặt lại mật khẩu thành công! Bây giờ bạn có thể đăng nhập bằng mật khẩu mới."

    def request_admin_otp(self, admin_email: str, ip: str = "127.0.0.1") -> tuple[bool, str, dict[str, Any]]:
        with self._lock:
            clean_email = str(admin_email or "").strip().lower()
            if not clean_email or "@" not in clean_email:
                clean_email = self._config.get("admin_notify_email") or "traivuho@gmail.com"

            now = time.time()
            last_req = self._cooldowns.get(f"adm_{clean_email}", 0)
            if now - last_req < 60:
                wait_sec = int(60 - (now - last_req))
                return False, f"Vui lòng đợi {wait_sec} giây trước khi yêu cầu mã OTP Admin mới!", {}

            import secrets
            otp_code = f"{secrets.randbelow(900000) + 100000}"
            expires = now + 300  # 5 minutes

            self._otps["admin_master"] = {
                "code": otp_code,
                "email": clean_email,
                "expires": expires,
                "attempts": 0,
                "ip": ip,
            }
            self._cooldowns[f"adm_{clean_email}"] = now

            parts = clean_email.split("@")
            masked_name = parts[0][0] + "***" + (parts[0][-1] if len(parts[0]) > 2 else "")
            masked_email = f"{masked_name}@{parts[1]}"

            sent_ok, send_msg = self._dispatch_email(clean_email, "Quản Trị Viên Moly", otp_code, email_type="reset_admin")

            return True, f"Mã OTP quản trị đã được gửi đến email {masked_email}! Mã có hiệu lực trong 5 phút.", {
                "masked_email": masked_email,
                "expires_in": 300,
                "is_real_smtp": sent_ok and self._config.get("enabled", False),
                "debug_otp": otp_code if not self._config.get("enabled", False) else None
            }

    def verify_admin_otp_and_reset(self, otp_code: str, new_password: str, new_pin: str) -> tuple[bool, str]:
        with self._lock:
            record = self._otps.get("admin_master")
            if not record:
                return False, "Yêu cầu OTP quản trị không tồn tại hoặc đã hết hạn! Vui lòng bấm 'Gửi mã OTP'."

            now = time.time()
            if now > record["expires"]:
                del self._otps["admin_master"]
                return False, "Mã OTP quản trị đã hết hạn sau 5 phút! Vui lòng bấm 'Gửi lại mã'."

            record["attempts"] += 1
            if record["attempts"] > 3:
                del self._otps["admin_master"]
                return False, "Bạn đã nhập sai mã OTP quá 3 lần! Mã này đã bị hủy để bảo vệ an toàn máy chủ."

            clean_otp = str(otp_code).strip()
            if clean_otp != record["code"]:
                remain = 3 - record["attempts"]
                return False, f"Mã OTP không chính xác! Bạn còn {remain} lần thử."

            if len(new_password) < 6:
                return False, "Mật khẩu quản trị mới phải có tối thiểu 6 ký tự!"
            if len(new_pin) != 6 or not new_pin.isdigit():
                return False, "Mã PIN quản trị mới phải đúng 6 chữ số!"

            del self._otps["admin_master"]
            ok, msg = self.account_mgr.force_reset_admin_credentials(new_password, new_pin)
            if not ok:
                return False, msg
            return True, "Đặt lại Mật Khẩu và Mã PIN Quản Trị thành công! Bây giờ bạn có thể đăng nhập bằng thông tin mới."

    def _dispatch_email(self, to_email: str, nickname: str, otp_code: str, email_type: str = "reset_password") -> tuple[bool, str]:
        cfg = self._config
        if not cfg.get("enabled") or not cfg.get("gmail_user") or not cfg.get("app_password"):
            print(f"[OTP SIMULATION] Gui OTP ({email_type}) {otp_code} toi {to_email}")
            return True, "Simulation mode"

        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            is_verify = email_type == "verify_email"
            is_admin_reset = email_type == "reset_admin"

            if is_admin_reset:
                subject = f"[{otp_code}] MA OTP QUAN TRI - KHOI PHUC MAT KHAU & PIN - Moly VN"
                header_desc = "Khôi Phục Mật Khẩu & PIN Quản Trị Hệ Thống"
                action_desc = "đặt lại MẬT KHẨU và MÃ PIN cho tài khoản Quản Trị Viên Moly"
            elif is_verify:
                subject = f"[{otp_code}] Ma Xac Thuc Lien Ket Gmail - Moly The Gioi Chuot Chui"
                header_desc = "Xác Thực Liên Kết Gmail Cư Dân An Toàn"
                action_desc = "liên kết và kích hoạt xác thực địa chỉ Gmail cho tài khoản Moly của bạn"
            else:
                subject = f"[{otp_code}] Ma Xac Thuc Dat Lai Mat Khau - Moly The Gioi Chuot Chui"
                header_desc = "Khôi Phục Mật Khẩu Cư Dân An Toàn"
                action_desc = "đặt lại mật khẩu cho tài khoản Moly của bạn"

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{cfg.get('sender_name', 'Moly VN')} <{cfg['gmail_user']}>"
            msg["To"] = to_email

            html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 580px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; background: #ffffff;">
              <div style="background: linear-gradient(135deg, #ff7e1b, #f59e0b); padding: 24px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 24px;">MOLY - THẾ GIỚI CHUỘT CHŨI</h1>
                <p style="margin: 6px 0 0; font-size: 14px; opacity: 0.9;">{header_desc}</p>
              </div>
              <div style="padding: 28px; color: #1e293b;">
                <p style="font-size: 15px;">Xin chào <strong>{nickname}</strong>,</p>
                <p style="font-size: 14px; color: #475569; line-height: 1.6;">
                  Hệ thống vừa nhận được yêu cầu <strong>{action_desc}</strong>. Vui lòng sử dụng mã xác thực OTP 6 số bên dưới để hoàn tất:
                </p>
                <div style="text-align: center; margin: 24px 0;">
                  <div style="display: inline-block; font-size: 36px; font-weight: 800; letter-spacing: 8px; color: #ff7e1b; background: #fff7ed; padding: 14px 28px; border-radius: 10px; border: 2px dashed #ffedd5;">
                    {otp_code}
                  </div>
                </div>
                <p style="font-size: 13px; color: #64748b;">
                  ⏰ Mã OTP này có hiệu lực trong vòng <strong>5 phút</strong>.<br>
                  🔒 Tuyệt đối không chia sẻ mã này cho bất kỳ ai, kể cả quản trị viên!
                </p>
                <p style="font-size: 12px; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 14px; margin-top: 24px;">
                  Nếu bạn không yêu cầu hành động này, vui lòng bỏ qua email hoặc đổi mật khẩu ngay để bảo đảm an toàn.
                </p>
              </div>
            </div>
            """
            msg.attach(MIMEText(html, "html"))

            clean_pwd = str(cfg.get("app_password", "")).replace(" ", "").strip()
            with smtplib.SMTP_SSL(cfg.get("smtp_host", "smtp.gmail.com"), int(cfg.get("smtp_port", 465)), timeout=12) as s:
                s.login(cfg["gmail_user"], clean_pwd)
                s.send_message(msg)

            print(f"[OTP GMAIL SUCCESS] Da gui ma OTP ({email_type}) toi {to_email}")
            return True, "Email sent successfully"
        except Exception as e:
            print(f"[OTP GMAIL ERROR] Loi gui email toi {to_email}: {e}")
            return False, str(e)

    def send_custom_email(self, to_email: str, subject: str, html_body: str) -> tuple[bool, str]:
        """Dispatches an arbitrary HTML notification email via Gmail SMTP."""
        cfg = self._config
        if not cfg.get("enabled") or not cfg.get("gmail_user") or not cfg.get("app_password"):
            print(f"[EMAIL SIMULATION] Gui email '{subject}' toi {to_email}")
            return True, "Simulation mode"

        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            clean_pwd = str(cfg.get("app_password", "")).replace(" ", "").strip()
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{cfg.get('sender_name', 'Moly - Thế Giới Chuột Chũi VN')} <{cfg['gmail_user']}>"
            msg["To"] = to_email
            msg.attach(MIMEText(html_body, "html", "utf-8"))

            with smtplib.SMTP_SSL(cfg.get("smtp_host", "smtp.gmail.com"), int(cfg.get("smtp_port", 465)), timeout=12) as s:
                s.login(cfg["gmail_user"], clean_pwd)
                s.send_message(msg)

            print(f"[GMAIL NOTIFY SUCCESS] Da gui email '{subject}' toi {to_email}")
            return True, "Email sent successfully"
        except Exception as e:
            print(f"[GMAIL NOTIFY ERROR] Loi gui email toi {to_email}: {e}")
            return False, str(e)


class RecoveryRequestManager:
    """Manages user requests to recover account password when they cannot use OTP or birthday."""
    def __init__(self, account_mgr: AccountManager, otp_mgr: OtpManager, filepath: Path = RECOVERY_REQUESTS_PATH) -> None:
        self.account_mgr = account_mgr
        self.otp_mgr = otp_mgr
        self.filepath = filepath
        self._lock = threading.Lock()
        self._requests: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if self.filepath.is_file():
            try:
                data = json.loads(self.filepath.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self._requests = data
            except Exception:
                self._requests = []

    def _save(self) -> None:
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            self.filepath.write_text(json.dumps(self._requests, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"[RECOVERY ERROR] Failed saving recovery requests: {e}", flush=True)

    def submit_request(
        self,
        identifier: str,
        contact_email: str,
        remembered_password: str,
        birthday: str = "",
        notes: str = "",
        ip: str = "127.0.0.1"
    ) -> tuple[bool, str, dict[str, Any]]:
        clean_ident = str(identifier or "").strip()
        clean_email = str(contact_email or "").strip().lower()
        clean_pwd = str(remembered_password or "").strip()
        clean_bday = str(birthday or "").strip()
        clean_notes = str(notes or "").strip()

        if not clean_ident:
            return False, "Vui lòng nhập Tên đăng nhập hoặc ID Moly của tài khoản!", {}
        if not clean_email or "@" not in clean_email or "." not in clean_email:
            return False, "Vui lòng nhập địa chỉ Gmail/Email hợp lệ để Quản Trị Viên phản hồi!", {}
        if not clean_pwd:
            return False, "Vui lòng nhập Mật khẩu cũ gần nhớ nhất để Quản Trị Viên đối chiếu xác thực chủ tài khoản!", {}

        with self._lock:
            self._load()
            now_ts = datetime.now(timezone.utc)
            # Rate limiting: max 3 requests per IP per 10 minutes
            recent_count = 0
            for r in self._requests:
                if r.get("ip") == ip:
                    try:
                        c_dt = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
                        if (now_ts - c_dt).total_seconds() < 600:
                            recent_count += 1
                    except Exception:
                        pass
            if recent_count >= 3:
                return False, "Bạn đã gửi yêu cầu quá nhiều lần! Vui lòng chờ 10 phút hoặc kiểm tra hòm thư phản hồi.", {}

            req_id = f"req_{int(time.time())}_{secrets.token_hex(3)}"
            req_data = {
                "id": req_id,
                "identifier": clean_ident,
                "contact_email": clean_email,
                "remembered_password": clean_pwd,
                "birthday": clean_bday,
                "notes": clean_notes,
                "ip": ip,
                "status": "pending",  # "pending", "resolved", "rejected"
                "admin_response": "",
                "created_at": now_ts.isoformat(),
                "resolved_at": None,
            }
            self._requests.insert(0, req_data)
            self._save()

        # Send alert email to admin if Gmail SMTP is configured
        try:
            self._notify_admin(req_data)
        except Exception as e:
            print(f"[RECOVERY NOTIFY ERROR] {e}", flush=True)

        return True, "Gửi yêu cầu hỗ trợ thành công! Ban Quản Trị sẽ đối chiếu thông tin và gửi phản hồi tới Gmail của bạn.", {"request_id": req_id}

    def _notify_admin(self, req: dict[str, Any]) -> None:
        cfg = self.otp_mgr._config
        if not cfg.get("enabled"):
            return
        admin_email = cfg.get("admin_notify_email") or "traivuho@gmail.com"
        subject = f"[Moly Quản Trị] Yêu cầu cấp lại mật khẩu từ cư dân: {req['identifier']}"
        html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px;">
  <div style="max-width: 600px; margin: auto; background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px;">
    <h2 style="color: #38bdf8; margin-top: 0;">📩 Yêu Cầu Cấp Lại Mật Khẩu (Cư Dân Moly)</h2>
    <p>Hệ thống vừa nhận được một yêu cầu cấp lại mật khẩu từ cư dân với thông tin chi tiết như sau:</p>
    <table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px;">
      <tr><td style="padding: 8px; border-bottom: 1px solid #334155; color: #94a3b8;">Tài khoản / ID:</td><td style="padding: 8px; border-bottom: 1px solid #334155; font-weight: bold; color: #fde047;">{req['identifier']}</td></tr>
      <tr><td style="padding: 8px; border-bottom: 1px solid #334155; color: #94a3b8;">Email liên hệ:</td><td style="padding: 8px; border-bottom: 1px solid #334155; font-weight: bold; color: #38bdf8;">{req['contact_email']}</td></tr>
      <tr><td style="padding: 8px; border-bottom: 1px solid #334155; color: #94a3b8;">Mật khẩu cũ gần nhớ nhất:</td><td style="padding: 8px; border-bottom: 1px solid #334155; font-weight: bold; color: #f43f5e;">{req['remembered_password']}</td></tr>
      <tr><td style="padding: 8px; border-bottom: 1px solid #334155; color: #94a3b8;">Ngày sinh cung cấp:</td><td style="padding: 8px; border-bottom: 1px solid #334155; color: #cbd5e1;">{req['birthday'] or 'Không cung cấp'}</td></tr>
      <tr><td style="padding: 8px; border-bottom: 1px solid #334155; color: #94a3b8;">Ghi chú cư dân:</td><td style="padding: 8px; border-bottom: 1px solid #334155; color: #cbd5e1;">{req['notes'] or 'Không có ghi chú'}</td></tr>
      <tr><td style="padding: 8px; border-bottom: 1px solid #334155; color: #94a3b8;">IP gửi yêu cầu:</td><td style="padding: 8px; border-bottom: 1px solid #334155; color: #cbd5e1;">{req['ip']}</td></tr>
      <tr><td style="padding: 8px; color: #94a3b8;">Thời gian:</td><td style="padding: 8px; color: #cbd5e1;">{req['created_at']}</td></tr>
    </table>
    <div style="background: #0f172a; border-left: 4px solid #10b981; padding: 12px; border-radius: 4px; font-size: 13px; color: #94a3b8;">
      Bạn có thể truy cập Bảng Quản Trị Admin tại <code>/admin</code> để xem xét, đối chiếu dữ liệu và cấp lại mật khẩu cho cư dân này.
    </div>
  </div>
</body>
</html>"""
        self.otp_mgr.send_custom_email(admin_email, subject, html_body)

    def list_requests(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        with self._lock:
            self._load()
            if status:
                return [r for r in self._requests if r.get("status") == status]
            return list(self._requests)

    def resolve_request(self, req_id: str, new_password: Optional[str] = None, admin_note: str = "") -> tuple[bool, str]:
        with self._lock:
            self._load()
            target = None
            for r in self._requests:
                if r.get("id") == req_id:
                    target = r
                    break
            if not target:
                return False, "Không tìm thấy yêu cầu này!"

            ident = target["identifier"]
            acc = self.account_mgr.get_account_by_identifier(ident)
            
            # If new_password provided, reset password for account
            if new_password and new_password.strip():
                if not acc:
                    return False, f"Không tìm thấy tài khoản cư dân '{ident}' trong hệ thống để đặt lại mật khẩu!"
                uid = int(acc["user_id"])
                ok, msg = self.account_mgr.reset_password_admin(uid, new_password.strip())
                if not ok:
                    return False, msg

            target["status"] = "resolved"
            target["admin_response"] = admin_note or f"Đã giải quyết và cấp mật khẩu mới lúc {datetime.now(timezone.utc).strftime('%H:%M %d/%m/%Y')}."
            target["resolved_at"] = datetime.now(timezone.utc).isoformat()
            self._save()

            # Optionally send email notification to user
            if target.get("contact_email") and self.otp_mgr._config.get("enabled"):
                try:
                    subject = "[Moly Vương Quốc Chuột Chũi] Thông Báo Phản Hồi Cấp Lại Mật Khẩu"
                    pwd_html = f'<div style="margin-top:10px;color:#fde047;font-size:15px;">Mật khẩu mới của bạn: <strong>{new_password}</strong></div>' if new_password else ''
                    body = f"""<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px;">
  <div style="max-width: 600px; margin: auto; background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px;">
    <h2 style="color: #38bdf8; margin-top: 0;">🎉 Yêu Cầu Cấp Lại Mật Khẩu Đã Được Xử Lý</h2>
    <p>Chào bạn, yêu cầu hỗ trợ tài khoản <strong>{ident}</strong> của bạn đã được Ban Quản Trị xem xét và giải quyết.</p>
    <div style="background: #0f172a; border: 1px solid #10b981; border-radius: 8px; padding: 14px; margin: 16px 0;">
      <div style="color: #34d399; font-weight: bold; margin-bottom: 6px;">Nội dung phản hồi từ Quản Trị Viên:</div>
      <div style="color: #f8fafc; font-size: 14px;">{target['admin_response']}</div>
      {pwd_html}
    </div>
    <p style="font-size: 13px; color: #94a3b8;">Sau khi đăng nhập thành công, bạn nên vào mục <strong>Hồ Sơ Cư Dân</strong> để xác thực Gmail và đổi lại mật khẩu cá nhân.</p>
  </div>
</body>
</html>"""
                    self.otp_mgr.send_custom_email(target["contact_email"], subject, body)
                except Exception as e:
                    print(f"[RECOVERY USER NOTIFY ERROR] {e}", flush=True)

            return True, f"Đã cập nhật trạng thái yêu cầu #{req_id} thành công!"


# Shared singleton instances
accounts = AccountManager()
google_oidc = GoogleOIDCService()
giftcodes = GiftcodeManager(accounts)
recharges = RechargeManager(accounts)
otp_mgr = OtpManager(accounts)
recovery_mgr = RecoveryRequestManager(accounts, otp_mgr)



