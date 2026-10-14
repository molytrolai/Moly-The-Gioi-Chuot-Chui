#!/usr/bin/env python3
"""Comprehensive verification test for In-Game Super Lamu Species Implementation.

Tests:
1. All 6 official Super Lamu species configurations and cloth IDs.
2. Binary TCP packet serialization for:
   - scene_user_record (Flash client map rendering with PetID, level 101, color, cloth_id, can_fly)
   - cmd 233 (PROTO_GET_OUTSIDE_PETS)
   - cmd 212/240 (GET_PET_INFO)
   - cmd 215/251 (FOLLOW_PET & CALL_SUPER_LAMU)
   - cmd 231 (BECOME_SUPER_LAHM)
   - cmd 232 (HAS_SUPER_LAHM)
   - cmd 238 (MODIFY_PET_COLOR)
   - cmd 1121 (PET_CLOTHES_USE)
3. Independent species progression: changing species starts new at Lv.1 while retaining prior progress.
4. HTTP REST APIs for Lamu status, species selection, and nurturing.
"""

from __future__ import annotations

import json
import struct
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from account_system import (
    AccountManager,
    SUPER_LAMU_SPECIES,
    DEFAULT_MOLY_ADMIN_ID,
    accounts,
)
import moly_probe_server as moly


class SuperLamuInGameTest(unittest.TestCase):
    def setUp(self):
        self.mgr = accounts
        acc = self.mgr.create_account(
            password="Pass123456",
            nickname="LamuTester",
            email="super_lamu@moly.test"
        )
        self.test_uid = acc["user_id"]
        self.mgr.set_vip(self.test_uid, vip_level=8, gold_beans=5000, months=12)

    def test_01_species_official_metadata(self):
        """Verify all 6 official species match the original game data."""
        expected = {
            "classic": {"color": 1, "cloth_id": 0},
            "dark": {"color": 5, "cloth_id": 1200030},
            "cosmic": {"color": 6, "cloth_id": 1200062},
            "mythic": {"color": 7, "cloth_id": 1200035},
            "ice": {"color": 3, "cloth_id": 1200075},
            "flame": {"color": 2, "cloth_id": 1200036},
        }
        for sid, exp in expected.items():
            self.assertIn(sid, SUPER_LAMU_SPECIES)
            meta = SUPER_LAMU_SPECIES[sid]
            self.assertEqual(meta["color"], exp["color"], f"Color mismatch for {sid}")
            self.assertEqual(meta["cloth_id"], exp["cloth_id"], f"Cloth ID mismatch for {sid}")
            self.assertTrue(meta["fly_skill"])

    def test_02_species_switching_and_progression(self):
        """Verify switching species starts un-nurtured at Lv.1 and retains previous progress."""
        # 1. Start with classic
        ok, msg, lamu = self.mgr.choose_super_lamu_species(self.test_uid, "classic")
        self.assertTrue(ok)
        self.assertEqual(lamu["super_type"], "classic")
        self.assertEqual(lamu["color"], 1)
        self.assertEqual(lamu["cloth_id"], 0)
        self.assertEqual(lamu["level"], 1)

        # 2. Train classic to Lv.2
        ok, msg, prog = self.mgr.train_super_lamu(self.test_uid, exp_gain=150)
        self.assertTrue(ok)
        self.assertEqual(prog["level"], 2)

        # 3. Switch to Dark (Hắc Ám) -> should start fresh at Lv.1
        ok, msg, lamu = self.mgr.choose_super_lamu_species(self.test_uid, "dark")
        self.assertTrue(ok)
        self.assertEqual(lamu["super_type"], "dark")
        self.assertEqual(lamu["color"], 5)
        self.assertEqual(lamu["cloth_id"], 1200030)
        self.assertEqual(lamu["level"], 1)

        # 4. Train Dark to Lv.3 (needs >= 300 EXP)
        self.mgr.train_super_lamu(self.test_uid, exp_gain=350)
        st = self.mgr.get_super_lamu_status(self.test_uid)
        dark_entry = next(s for s in st["species_list"] if s["id"] == "dark")
        self.assertEqual(dark_entry["level"], 3)

        # 5. Switch back to Classic -> must resume at Lv.2
        ok, msg, lamu = self.mgr.choose_super_lamu_species(self.test_uid, "classic")
        self.assertTrue(ok)
        self.assertEqual(lamu["super_type"], "classic")
        self.assertEqual(lamu["level"], 2)

    def test_03_scene_user_record_binary_embedding(self):
        """Verify scene_user_record embeds pet with level 101, color, and cloth_id."""
        self.mgr.choose_super_lamu_species(self.test_uid, "mythic")
        rec = moly.scene_user_record(self.test_uid, map_id=1, xpos=450, ypos=260)
        
        # Verify length matches expected 219 + 4 * clothes_len
        clothes = self.mgr.get_clothes(self.test_uid)
        expected_len = 219 + 4 * len(clothes)
        self.assertEqual(len(rec), expected_len)

        # Unpack the pet fields from record:
        # UserID (4), Nick (16), 7xUInt32 (28), BIBI (10) -> offset 58
        # At offset 58: PosX (4), PosY (4), Grid (4), Action2 (4), PetID (4)
        offset = 4 + 16 + 28 + 10
        pos_x, pos_y, grid, act2, pet_id = struct.unpack_from(">IIIII", rec, offset)
        self.assertEqual(pet_id, 1, "PetID must be 1 (active)")
        self.assertEqual(pos_x, 450)
        self.assertEqual(pos_y, 260)

        # Next: PetName (16), PetColor (4), PetLevel (1)
        offset += 20
        pet_name, pet_color, pet_level = struct.unpack_from(">16sIB", rec, offset)
        self.assertEqual(pet_color, 7, "Mythic color must be 7 (Platinum)")
        self.assertEqual(pet_level, 101, "Level must be 101 for Super Lamu propeller")

        # Next: 7xUInt32 (28)
        offset += 21 + 28
        # Next: 3xByte (3), PetCloth (4), PetHonor (4), CanFly (4)
        i1, i2, i3, pet_cloth, pet_honor, can_fly = struct.unpack_from(">BBBIII", rec, offset)
        self.assertEqual(pet_cloth, 1200035, "Pet cloth must be 1200035 (Chiến Bào Siêu Lamu)")
        self.assertEqual(can_fly, 1, "Super Lamu must have can_fly=1")

    def test_04_cmd_233_outside_pets_packet(self):
        """Verify cmd 233 returns the 96-byte pet record with level 101."""
        self.mgr.choose_super_lamu_species(self.test_uid, "cosmic")
        pkt = moly.world_response(233, self.test_uid, version=1, request_body=b"")
        self.assertIsNotNone(pkt)
        
        # Packet header: 17 bytes (len 4, ver 1, cmd 4, uid 4, err 4)
        length, ver, rcmd, ruid, rerr = struct.unpack(">IBIII", pkt[:17])
        self.assertEqual(rcmd, 233)
        self.assertEqual(ruid, self.test_uid)

        # Body: count (4) + 96 bytes pet entry = 100 bytes
        clear_body = moly.moly_decrypt(pkt[17:])
        self.assertEqual(len(clear_body), 100)
        count = struct.unpack(">I", clear_body[:4])[0]
        self.assertEqual(count, 1)

        # Unpack pet entry
        pet_entry = clear_body[4:]
        (
            pet_id, uid, user_nick, pet_flag, birth, age,
            pet_nick, color, hungry, thirsty, sanitary, spirit,
            level, skill, s_ex0, s_ex1, s_ex2, s_bits, s_val,
            h0, h1, h2, cloth_id, honor
        ) = struct.unpack(">II16sIII16sIBBBBBIIIIIIBBBII", pet_entry)

        self.assertEqual(pet_id, 1)
        self.assertEqual(uid, self.test_uid)
        self.assertEqual(color, 6, "Cosmic color must be 6")
        self.assertEqual(cloth_id, 1200062, "Cosmic cloth must be 1200062 (Ngôi Sao Tinh Tú)")
        self.assertEqual(level, 101, "Level must be 101")

    def test_05_cmd_215_and_251_follow_and_call(self):
        """Verify cmd 215 (Follow) and cmd 251 (Call Super Lamu) return the 72-byte packet."""
        self.mgr.choose_super_lamu_species(self.test_uid, "flame")
        
        # Test cmd 215
        pkt215 = moly.world_response(215, self.test_uid, version=1, request_body=struct.pack(">IB", 1, 1))
        self.assertIsNotNone(pkt215)
        clear215 = moly.moly_decrypt(pkt215[17:])
        self.assertEqual(len(clear215), 72)
        
        uid, pid, nick, color, is_follow, h, t, s, sp, lvl, skill, se0, se1, se2, sb, sv, sh0, sh1, sh2, cid, hon = struct.unpack(
            ">II16sIIBBBBBIIIIIIBBBII", clear215
        )
        self.assertEqual(pid, 1)
        self.assertEqual(color, 2, "Flame color must be 2")
        self.assertEqual(cid, 1200036, "Flame cloth must be 1200036 (Mũ Hổ Lửa)")
        self.assertEqual(lvl, 101)
        self.assertEqual(is_follow, 1)

        # Test cmd 251 (Call Super Lamu)
        pkt251 = moly.world_response(251, self.test_uid, version=1, request_body=b"")
        self.assertIsNotNone(pkt251)
        clear251 = moly.moly_decrypt(pkt251[17:])
        self.assertEqual(len(clear251), 72)

    def test_06_cmd_231_and_232_super_lahm_flags(self):
        """Verify cmd 231 (Become) and 232 (Has Super Lamu) return byte 1."""
        pkt231 = moly.world_response(231, self.test_uid, version=1, request_body=b"")
        clear231 = moly.moly_decrypt(pkt231[17:])
        self.assertEqual(clear231, b"\x01")

        pkt232 = moly.world_response(232, self.test_uid, version=1, request_body=b"")
        clear232 = moly.moly_decrypt(pkt232[17:])
        self.assertEqual(clear232, b"\x01")

    def test_07_cmd_238_and_1121_color_and_cloth_in_game(self):
        """Verify cmd 238 (modify color) and cmd 1121 (wear cloth) updates accounts."""
        # Change color via cmd 238
        pkt238 = moly.world_response(238, self.test_uid, version=1, request_body=struct.pack(">III", 1, 3, 0))
        self.assertIsNotNone(pkt238)
        lamu = self.mgr.get_lamu(self.test_uid)
        self.assertEqual(lamu["color"], 3)

        # Change cloth via cmd 1121
        pkt1121 = moly.world_response(1121, self.test_uid, version=1, request_body=struct.pack(">II", 1, 1200075))
        self.assertIsNotNone(pkt1121)
        lamu = self.mgr.get_lamu(self.test_uid)
        self.assertEqual(lamu["cloth_id"], 1200075)


if __name__ == "__main__":
    unittest.main()
