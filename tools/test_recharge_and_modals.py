#!/usr/bin/env python3
"""Automated Verification Suite for Recharge System (Card & QR), Admin Management, and Modal UX."""

import json
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from account_system import accounts, recharges


def run_recharge_and_modal_tests(port: int = 18092):
    print("=" * 70)
    print("MOLY - THẾ GIỚI CHUỘT CHŨI VN: RECHARGE & MODAL UX VERIFICATION")
    print("=" * 70)

    archive_dir = PROJECT_ROOT / "archive" / "clients" / "capture"
    overrides_dir = PROJECT_ROOT / "archive" / "clients" / "local-overrides"
    mirror_dir = PROJECT_ROOT / "archive" / "clients" / "offline-mirror"
    proxy_cmd = [
        sys.executable,
        str(PROJECT_ROOT / "tools" / "capture_proxy.py"),
        "--port", str(port),
        "--archive", str(archive_dir),
        "--overrides", str(overrides_dir),
        "--mirror", str(mirror_dir),
    ]
    proc = subprocess.Popen(proxy_cmd)
    time.sleep(1.5)

    try:
        base_url = f"http://127.0.0.1:{port}"

        # 1. Verify Pages Serving & Title Branding
        print("\n[Step 1] Verifying Page Serving & Branding (Moly - Thế Giới Chuột Chũi VN)...")
        for page, expected_title in [
            ("/", "Moly - Thế Giới Chuột Chũi VN"),
            ("/play", "Moly - Thế Giới Chuột Chũi"),
            ("/admin", "Moly - Thế Giới Chuột Chũi VN"),
        ]:
            req = urllib.request.Request(f"{base_url}{page}", headers={"Host": "127.0.0.1"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                assert resp.status == 200
                html = resp.read().decode("utf-8")
                assert expected_title in html, f"Page {page} missing title: {expected_title}"
                assert "Moly Việt" not in html, f"Page {page} still contains 'Moly Việt'!"
                assert "Taomee" not in html, f"Page {page} still contains 'Taomee'!"
                assert "← Trở lại" in html, f"Page {page} missing '← Trở lại' button!"
                print(f"  [OK] Page {page}: 200 OK, branding verified, back buttons confirmed.")

        # 2. Verify Payment Public Config
        print("\n[Step 2] Testing GET /api/payment/config...")
        req = urllib.request.Request(f"{base_url}/api/payment/config", headers={"Host": "127.0.0.1"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            cfg_data = json.loads(resp.read().decode("utf-8"))
            assert "bank_name" in cfg_data
            assert "account_number" in cfg_data
            assert "qr_image_url" in cfg_data
            print(f"  [OK] Default payment config received: Bank={cfg_data.get('bank_name')}, STK={cfg_data.get('account_number')}")

        # 3. Create Test User
        print("\n[Step 3] Ensuring test user exists...")
        user = accounts.get_account_by_username("test_gamer_recharge")
        if not user:
            user = accounts.create_account(
                username="test_gamer_recharge",
                password="password123",
                nickname="Chuột Thử Nghiệm",
                fullname="Nguyễn Thử Nghiệm",
                email="test.gamer@gmail.com",
                birthday="2000-01-01",
                gold_beans=1000,
                vip_level=1
            )
        test_uid = user["user_id"]
        initial_beans = user.get("gold_beans", 0)
        initial_vip = user.get("vip_level", 0)
        print(f"  [OK] Test user {test_uid} ({user.get('nickname')}): {initial_beans} beans, VIP {initial_vip}")

        # 4. Submit Card Recharge Order (Method 1)
        print("\n[Step 4] Testing Method 1: Scratch Card Submission...")
        t_now = int(time.time() * 1000)
        card_payload = {
            "user_id": test_uid,
            "method": "card",
            "card_telco": "VIETTEL",
            "amount": 50000,
            "card_serial": f"VTT{t_now}",
            "card_code": f"PIN{t_now}"
        }
        req = urllib.request.Request(
            f"{base_url}/api/recharge/create",
            headers={"Content-Type": "application/json", "Host": "127.0.0.1"},
            data=json.dumps(card_payload).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            res = json.loads(resp.read().decode("utf-8"))
            assert res.get("ok") is True
            assert "5 - 15 phút" in res.get("message", "")
            card_order_id = res.get("order", {}).get("order_id")
            assert card_order_id is not None
            print(f"  [OK] Card order created: {card_order_id}, message contains 5-15 min notice")

        # 5. Submit QR Transfer Recharge Order (Method 2)
        print("\n[Step 5] Testing Method 2: QR Transfer Submission with Random Code...")
        # First generate random code
        req = urllib.request.Request(f"{base_url}/api/payment/generate_code", headers={"Host": "127.0.0.1"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            code_res = json.loads(resp.read().decode("utf-8"))
            transfer_code = code_res.get("code")
            assert transfer_code is not None
            print(f"  [OK] Generated unique transfer code: {transfer_code}")

        qr_payload = {
            "user_id": test_uid,
            "method": "qr",
            "amount": 100000,
            "transfer_code": transfer_code
        }
        req = urllib.request.Request(
            f"{base_url}/api/recharge/create",
            headers={"Content-Type": "application/json", "Host": "127.0.0.1"},
            data=json.dumps(qr_payload).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            res = json.loads(resp.read().decode("utf-8"))
            assert res.get("ok") is True
            assert "5 - 15 phút" in res.get("message", "")
            qr_order_id = res.get("order", {}).get("order_id")
            assert qr_order_id is not None
            print(f"  [OK] QR order created: {qr_order_id}, transfer_code={transfer_code}")

        # 6. Verify User Orders History
        print("\n[Step 6] Testing GET /api/recharge/orders?user_id=...")
        req = urllib.request.Request(f"{base_url}/api/recharge/orders?user_id={test_uid}", headers={"Host": "127.0.0.1"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            u_orders = json.loads(resp.read().decode("utf-8")).get("orders", [])
            order_ids = [o["order_id"] for o in u_orders]
            assert card_order_id in order_ids
            assert qr_order_id in order_ids
            print(f"  [OK] User order history returned {len(u_orders)} orders, both pending orders found")

        # 7. Admin Login & Authorization
        print("\n[Step 7] Testing Admin Login & Auth Token...")
        login_payload = {
            "username": "00000000",
            "password": "adminpassword",
            "pin": "888888"
        }
        req = urllib.request.Request(
            f"{base_url}/api/admin/login",
            headers={"Content-Type": "application/json", "Host": "127.0.0.1"},
            data=json.dumps(login_payload).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            admin_res = json.loads(resp.read().decode("utf-8"))
            token = admin_res.get("token")
            assert token is not None
            print(f"  [OK] Admin authenticated successfully, token obtained: {token[:12]}...")

        # 8. Admin Orders List & 15-Minute Countdown Check
        print("\n[Step 8] Testing GET /api/admin/recharge/orders...")
        req = urllib.request.Request(
            f"{base_url}/api/admin/recharge/orders",
            headers={"Authorization": f"Bearer {token}", "Host": "127.0.0.1"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            res_data = json.loads(resp.read().decode("utf-8"))
            all_orders = res_data.get("orders", res_data if isinstance(res_data, list) else [])
            assert len(all_orders) >= 2
            card_found = next((o for o in all_orders if o["order_id"] == card_order_id), None)
            qr_found = next((o for o in all_orders if o["order_id"] == qr_order_id), None)
            assert card_found is not None
            assert qr_found is not None
            assert "review_remaining_seconds" in card_found
            assert 0 <= card_found["review_remaining_seconds"] <= 900
            print(f"  [OK] Admin orders returned: 15-min countdown verified ({card_found['review_remaining_seconds']}s remaining)")

        # 9. Admin Customizes Payment Config (QR Code image URL)
        print("\n[Step 9] Testing Admin Custom QR Code & Bank Config Update...")
        cfg_update_payload = {
            "bank_name": "Vietcombank",
            "account_number": "999888777666",
            "account_holder": "ADMIN CHUOT CHUI VN",
            "qr_image_url": "https://moly-game.vn/assets/custom_admin_qr.png",
            "note": "Nạp tiền tự động duyệt trong 5 - 15 phút. Ghi đúng mã giao dịch!"
        }
        req = urllib.request.Request(
            f"{base_url}/api/admin/payment/config",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}", "Host": "127.0.0.1"},
            data=json.dumps(cfg_update_payload).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            cfg_res = json.loads(resp.read().decode("utf-8"))
            assert cfg_res.get("ok") is True

        # Verify updated config publicly
        req = urllib.request.Request(f"{base_url}/api/payment/config", headers={"Host": "127.0.0.1"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            new_cfg = json.loads(resp.read().decode("utf-8"))
            assert new_cfg.get("bank_name") == "Vietcombank"
            assert new_cfg.get("account_number") == "999888777666"
            assert new_cfg.get("qr_image_url") == "https://moly-game.vn/assets/custom_admin_qr.png"
            print("  [OK] Admin customized payment config & QR image URL successfully verified!")

        # 10. Admin Approves Card Order -> Verifies VIP & Bean awards
        print("\n[Step 10] Testing Admin Approval of Card Order...")
        approve_payload = {"order_id": card_order_id}
        req = urllib.request.Request(
            f"{base_url}/api/admin/recharge/approve",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}", "Host": "127.0.0.1"},
            data=json.dumps(approve_payload).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            app_res = json.loads(resp.read().decode("utf-8"))
            assert app_res.get("ok") is True
            print(f"  [OK] Admin approved card order {card_order_id}: {app_res.get('message')}")

        # Check user account updated
        updated_user = accounts.get_account(test_uid)
        expected_beans = initial_beans + (50000 // 100)
        assert updated_user.get("gold_beans") == expected_beans
        assert updated_user.get("vip_level") >= 2
        print(f"  [OK] User awarded beans: {initial_beans} -> {updated_user.get('gold_beans')}, VIP level: {updated_user.get('vip_level')}")

        # 11. Admin Rejects QR Order
        print("\n[Step 11] Testing Admin Rejection of Order with Reason...")
        reject_payload = {
            "order_id": qr_order_id,
            "reason": "Chưa nhận được giao dịch qua tài khoản ngân hàng"
        }
        req = urllib.request.Request(
            f"{base_url}/api/admin/recharge/reject",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}", "Host": "127.0.0.1"},
            data=json.dumps(reject_payload).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            rej_res = json.loads(resp.read().decode("utf-8"))
            assert rej_res.get("ok") is True
            print(f"  [OK] Admin rejected order {qr_order_id} successfully.")

        print("\n" + "=" * 70)
        print("ALL RECHARGE, ADMIN MANAGEMENT, AND MODAL UX TESTS PASSED! (11/11)")
        print("=" * 70)
        return True

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    success = run_recharge_and_modal_tests()
    sys.exit(0 if success else 1)
