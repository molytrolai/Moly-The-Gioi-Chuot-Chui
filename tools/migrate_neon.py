#!/usr/bin/env python3
"""Run SQL migration script on Neon PostgreSQL database via HTTP SQL API."""

import urllib.request
import urllib.error
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CONN_URI = "postgresql://neondb_owner:npg_QUak1c0dzVqy@ep-autumn-bar-a1n8y84y.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
ENDPOINT = "https://ep-autumn-bar-a1n8y84y.ap-southeast-1.aws.neon.tech/sql"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_FILE = PROJECT_ROOT / "deploy" / "neon_schema.sql"

def execute_query(query: str):
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={
            "Neon-Connection-String": CONN_URI,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    print("=== MIGRATING NEON POSTGRESQL DATABASE ===")
    sql_script = SCHEMA_FILE.read_text(encoding="utf-8")

    # The schema consists of 4 statements:
    # 1. CREATE TABLE IF NOT EXISTS moly_users
    # 2. CREATE INDEX idx_moly_users_email
    # 3. CREATE INDEX idx_moly_users_google_id
    # 4. INSERT INTO moly_users
    raw_statements = [
        """CREATE TABLE IF NOT EXISTS moly_users (
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
    home JSONB NOT NULL DEFAULT '{"level": 1, "cleanliness": 100, "style_item": 160001, "farm_crops": [], "decorations": [], "homeland_bg": 1230001, "homeland_decorations": []}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
)""",
        "CREATE INDEX IF NOT EXISTS idx_moly_users_email ON moly_users(email)",
        "CREATE INDEX IF NOT EXISTS idx_moly_users_google_id ON moly_users(google_id)",
        """INSERT INTO moly_users (
    user_id,
    nickname,
    password_hash,
    email,
    color,
    vip_flags,
    vip_level,
    vip_month,
    vip_value,
    vip_end,
    gold_beans,
    element_knight_type,
    element_knight_talent,
    is_admin,
    clothes,
    inventory,
    tasks,
    professions,
    lamu,
    home
) VALUES (
    10000001,
    'Moly Admin',
    '*',
    'admin@moly.viet',
    1,
    33,
    19,
    120,
    999999,
    4102444800,
    999999,
    1,
    40,
    TRUE,
    '[]'::jsonb,
    '{}'::jsonb,
    '{"1": {"step": 1, "status": 2}, "667": {"step": 1, "status": 2}, "668": {"step": 1, "status": 2}, "669": {"step": 1, "status": 2}, "670": {"step": 1, "status": 2}}'::jsonb,
    '{"guide": {"exp": 1000, "level": 3}, "ninja": {"exp": 1000, "level": 3}, "police": {"exp": 1000, "level": 3}, "knight": {"exp": 1000, "level": 3}, "journalist": {"exp": 1000, "level": 3}}'::jsonb,
    '{"id": 1, "name": "LaMu Thần Thoại", "color": 1, "level": 5, "mood": 100, "hunger": 100, "skills": [1, 2, 3, 4], "following": true, "cleanliness": 100, "is_super_lamu": true}'::jsonb,
    '{"level": 5, "cleanliness": 100, "style_item": 160001, "decorations": [{"item_id": 160002, "x": 150, "y": 250}, {"item_id": 160003, "x": 300, "y": 300}], "homeland_bg": 1230001, "homeland_decorations": [], "farm_crops": [{"number": 1, "itemid": 1230001, "x": 200, "y": 200, "value": 100, "sickflag": 0, "fruit_num": 10, "fruit_status": 3, "mature_time": 0, "diff_mature_time": 0, "cur_grow_rate": 100, "earth": 100, "pollinate_num": 0, "thiefable": 0}]}'::jsonb
) ON CONFLICT (user_id) DO UPDATE SET
    vip_level = 19,
    vip_end = 4102444800,
    is_admin = TRUE"""
    ]

    for idx, stmt in enumerate(raw_statements, 1):
        print(f"Executing statement {idx}/{len(raw_statements)}...")
        try:
            res = execute_query(stmt)
            print(f"  [OK] Statement {idx} executed: command = {res.get('command')}")
        except urllib.error.HTTPError as e:
            print(f"  [ERROR] Statement {idx} failed: {e.read().decode('utf-8')}")
            sys.exit(1)

    print("\nVerifying moly_users in Neon...")
    res = execute_query("SELECT user_id, nickname, is_admin, vip_level, gold_beans FROM moly_users;")
    print("Moly Users in Neon DB:", res.get("rows"))
    print("\n=== NEON DATABASE MIGRATION COMPLETED SUCCESSFULLY! ===")

if __name__ == "__main__":
    main()
