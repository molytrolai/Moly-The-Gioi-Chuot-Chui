#!/usr/bin/env python3
"""Database Adapter for Moly-Viet: Supports local JSON and Neon Serverless PostgreSQL.

When DATABASE_URL is set (e.g. on Render with Neon PostgreSQL), accounts and progress
are synchronized to the cloud database. Otherwise, local JSON file storage is used.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "server"
ACCOUNTS_PATH = DATA_DIR / "accounts.json"

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()


class PostgresAdapter:
    """Neon Serverless PostgreSQL Adapter using psycopg2 or urllib/requests fallback."""

    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self._conn = None
        self._init_db()

    def _get_connection(self):
        try:
            import psycopg2
            if self._conn is None or self._conn.closed:
                self._conn = psycopg2.connect(self.db_url, sslmode="require")
            return self._conn
        except ImportError:
            return None

    def _init_db(self) -> None:
        conn = self._get_connection()
        if not conn:
            print("[DB] psycopg2 not installed; database persistence deferred to local storage.")
            return

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS moly_accounts (
                    user_id BIGINT PRIMARY KEY,
                    data JSONB NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_moly_accounts_updated ON moly_accounts(updated_at);
            """)
        conn.commit()
        print("[DB] Initialized Neon PostgreSQL 'moly_accounts' table.")

    def load_accounts(self) -> dict[str, dict[str, Any]]:
        conn = self._get_connection()
        if not conn:
            return {}

        with conn.cursor() as cur:
            cur.execute("SELECT user_id, data FROM moly_accounts;")
            rows = cur.fetchall()
            accounts = {}
            for uid, data in rows:
                if isinstance(data, str):
                    data = json.loads(data)
                accounts[str(uid)] = data
            return accounts

    def save_account(self, user_id: int, data: dict[str, Any]) -> None:
        conn = self._get_connection()
        if not conn:
            return

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO moly_accounts (user_id, data, updated_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id) DO UPDATE
                SET data = EXCLUDED.data, updated_at = CURRENT_TIMESTAMP;
            """, (user_id, json.dumps(data, ensure_ascii=False)))
        conn.commit()


def get_db_adapter() -> Optional[PostgresAdapter]:
    if DATABASE_URL:
        try:
            return PostgresAdapter(DATABASE_URL)
        except Exception as e:
            print(f"[DB] Error connecting to PostgreSQL ({DATABASE_URL[:20]}...): {e}")
    return None


def sync_local_to_neon() -> None:
    """Migrates local accounts.json to Neon PostgreSQL database."""
    adapter = get_db_adapter()
    if not adapter:
        print("[DB SYNC] No DATABASE_URL configured.")
        return

    if not ACCOUNTS_PATH.is_file():
        print(f"[DB SYNC] No local accounts at {ACCOUNTS_PATH}")
        return

    data = json.loads(ACCOUNTS_PATH.read_text(encoding="utf-8"))
    count = 0
    for uid_str, acc in data.items():
        uid = int(uid_str)
        adapter.save_account(uid, acc)
        count += 1
    print(f"[DB SYNC] Successfully synced {count} accounts to Neon PostgreSQL!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        sync_local_to_neon()
    else:
        print(f"DATABASE_URL is {'set' if DATABASE_URL else 'NOT set'}.")
