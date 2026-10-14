#!/usr/bin/env python3
"""Unit tests for Moly-Viet Account System."""

from __future__ import annotations

import base64
import json
import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from account_system import (
    AccountManager,
    DEFAULT_MOLY_ADMIN_ID,
    GoogleOIDCService,
    hash_moly_password,
)


class AccountSystemTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.accounts_path = Path(self.temp_dir.name) / "accounts.json"
        self.oauth_path = Path(self.temp_dir.name) / "oauth.json"
        self.mgr = AccountManager(storage_path=self.accounts_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_admin_account_initialized(self) -> None:
        admin = self.mgr.get_account(DEFAULT_MOLY_ADMIN_ID)
        self.assertIsNotNone(admin)
        self.assertEqual(admin["nickname"], "Moly Admin")
        self.assertIn(admin["vip_level"], [8, 19])
        self.assertTrue(admin["is_admin"])
        # Check wildcard authentication
        ok, profile = self.mgr.authenticate(DEFAULT_MOLY_ADMIN_ID, "any-password")
        self.assertTrue(ok)
        self.assertIsNotNone(profile)

    def test_create_and_authenticate_player(self) -> None:
        new_acc = self.mgr.create_account(
            password="secret_password_123",
            nickname="Chuột Chũi",
            email="chui@example.com",
        )
        user_id = new_acc["user_id"]
        self.assertGreater(user_id, DEFAULT_MOLY_ADMIN_ID)
        self.assertEqual(new_acc["nickname"], "Chuột Chũi")

        # Authenticate with correct password
        ok, profile = self.mgr.authenticate(user_id, "secret_password_123")
        self.assertTrue(ok)
        self.assertEqual(profile["nickname"], "Chuột Chũi")

        # Authenticate with correct MD5(MD5(pwd)) hash
        pwd_hash = hash_moly_password("secret_password_123")
        ok, profile = self.mgr.authenticate(user_id, pwd_hash)
        self.assertTrue(ok)

        # Authenticate with wrong password
        fail, _ = self.mgr.authenticate(user_id, "wrong_pass")
        self.assertFalse(fail)

    def test_vip_and_beans_update(self) -> None:
        acc = self.mgr.create_account(password="pass1", nickname="VipPlayer")
        user_id = acc["user_id"]
        self.assertEqual(acc["vip_level"], 0)

        self.mgr.set_vip(user_id, vip_level=8, gold_beans=500000)
        updated = self.mgr.get_account(user_id)
        self.assertEqual(updated["vip_level"], 8)
        self.assertEqual(updated["gold_beans"], 500000)
        self.assertEqual(updated["vip_flags"], 33)

    def test_google_oidc_link_and_provision(self) -> None:
        oidc = GoogleOIDCService(config_path=self.oauth_path)
        auth_url = oidc.build_authorization_url()
        self.assertIn("accounts.google.com", auth_url)
        self.assertIn("response_type=code", auth_url)

        # Simulate Google identity callback
        google_sub = "google_user_998877"
        acc = oidc.process_google_identity(
            self.mgr,
            google_sub=google_sub,
            email="googleplayer@gmail.com",
            name="Google Mole",
        )
        self.assertIsNotNone(acc)
        self.assertEqual(acc["google_id"], google_sub)
        self.assertEqual(acc["email"], "googleplayer@gmail.com")

        # Calling again returns same account
        acc2 = oidc.process_google_identity(
            self.mgr, google_sub=google_sub
        )
        self.assertEqual(acc["user_id"], acc2["user_id"])

    def test_parse_id_token_payload(self) -> None:
        oidc = GoogleOIDCService(config_path=self.oauth_path)
        # Create mock JWT: header.payload.signature
        header = base64.urlsafe_b64encode(b'{"alg":"RS256"}').decode().rstrip("=")
        payload = base64.urlsafe_b64encode(
            b'{"sub":"g_123","email":"test@example.com","name":"Test User"}'
        ).decode().rstrip("=")
        sig = "mocksig"
        jwt = f"{header}.{payload}.{sig}"
        claims = oidc.parse_id_token_unverified(jwt)
        self.assertEqual(claims["sub"], "g_123")
        self.assertEqual(claims["email"], "test@example.com")

    def test_task_and_lamu_progression(self) -> None:
        acc = self.mgr.create_account(password="pass123", nickname="Player1")
        user_id = acc["user_id"]
        # Check default tasks and lamu
        tasks = self.mgr.get_tasks(user_id)
        self.assertIn("1", tasks)
        lamu = self.mgr.get_lamu(user_id)
        self.assertEqual(lamu["name"], "Bé LaMu")
        self.assertEqual(lamu["level"], 1)

        # Update task state
        self.mgr.set_task_state(user_id, task_id=667, status=2, step=1)
        tasks_updated = self.mgr.get_tasks(user_id)
        self.assertIn("667", tasks_updated)
        self.assertEqual(tasks_updated["667"]["status"], 2)

        # Update lamu
        self.mgr.update_lamu(user_id, {"level": 3, "hunger": 100, "is_super_lamu": True})
        lamu_updated = self.mgr.get_lamu(user_id)
        self.assertEqual(lamu_updated["level"], 3)
        self.assertTrue(lamu_updated["is_super_lamu"])

        # Update profession
        self.mgr.update_profession(user_id, "knight", level=2, exp=500)
        profs = self.mgr.get_professions(user_id)
        self.assertIn("knight", profs)
        self.assertEqual(profs["knight"]["level"], 2)


if __name__ == "__main__":
    unittest.main()
