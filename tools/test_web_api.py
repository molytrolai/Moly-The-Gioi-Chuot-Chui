import json
import urllib.request
import time

BASE_URL = "http://127.0.0.1:18080"

def post(endpoint, data):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP ERROR {e.code}: {body.encode('ascii', 'backslashreplace').decode('ascii')}")
        raise

def main():
    print("Testing Web HTTP APIs for Account Management...")

    # 1. Admin login with 00000000
    status, res = post("/api/user/login", {"identifier": "00000000", "password": "*"})
    assert status == 200 and res["ok"] is True
    acc = res["account"]
    assert acc["user_id"] == 0 and acc["display_id"] == "00000000" and acc["is_admin"] is True
    assert acc["sso_session"].startswith("00000000")
    print(f"  [PASS] 1. Admin login via '00000000': OK (ID: {acc['display_id']}, VIP {acc['vip_level']})")

    # 2. Admin login with 'admin'
    status, res = post("/api/user/login", {"identifier": "admin", "password": "*"})
    assert status == 200 and res["ok"] is True
    print("  [PASS] 2. Admin login via 'admin': OK")

    # 3. User Register
    u_name = f"mole_gamer_{int(time.time())}"
    status, res = post("/api/user/register", {
        "username": u_name,
        "password": "mypassword123",
        "fullname": "Lê Văn Mole",
        "nickname": "Chuột Nhí",
        "email": f"{u_name}@test.com",
        "birthday": "2008-05-20"
    })
    assert status == 200 and res["ok"] is True
    uid = res["user_id"]
    display_id = res["display_id"]
    assert 10000000 <= uid <= 99999999
    assert res["vip_level"] == 1
    assert res["sso_session"].startswith(f"{uid:08x}")
    print(f"  [PASS] 3. Register new user: OK (Random 8-digit ID: {display_id}, Username: {u_name})")

    # 4. User Login with username
    status, res = post("/api/user/login", {"identifier": u_name, "password": "mypassword123"})
    assert status == 200 and res["ok"] is True
    print(f"  [PASS] 4. User login via username '{u_name}': OK")

    # 5. User Login with Mole ID
    status, res = post("/api/user/login", {"identifier": str(uid), "password": "mypassword123"})
    assert status == 200 and res["ok"] is True
    print(f"  [PASS] 5. User login via random Mole ID '{uid}': OK")

    # 6. User Login with Email
    status, res = post("/api/user/login", {"identifier": f"{u_name}@test.com", "password": "mypassword123"})
    assert status == 200 and res["ok"] is True
    print(f"  [PASS] 6. User login via email '{u_name}@test.com': OK")

    # 7. Update profile
    status, res = post("/api/user/update_profile", {
        "user_id": uid,
        "fullname": "Lê Văn Mole Siêu Cấp",
        "nickname": "Mole Pro VIP",
        "birthday": "2007-01-01"
    })
    assert status == 200 and res["ok"] is True
    assert res["account"]["fullname"] == "Lê Văn Mole Siêu Cấp"
    assert res["account"]["username"] == u_name  # Username remains immutable!
    print("  [PASS] 7. Update profile: OK (Fullname updated, Username remains immutable)")

    # 8. Reset password with info
    status, res = post("/api/user/reset_password", {
        "identifier": u_name,
        "email": f"{u_name}@test.com",
        "birthday": "2007-01-01",
        "new_password": "brand_new_password_888"
    })
    assert status == 200 and res["ok"] is True
    print("  [PASS] 8. Reset password before login: OK")

    # 9. Login with new password
    status, res = post("/api/user/login", {"identifier": u_name, "password": "brand_new_password_888"})
    assert status == 200 and res["ok"] is True
    print("  [PASS] 9. Login with new reset password: OK")

    # 10. Recharge VIP
    status, res = post("/api/user/recharge_vip", {"user_id": uid, "amount": 20000})
    assert status == 200 and res["ok"] is True
    print(f"  [PASS] 10. Recharge VIP 20k: OK (Level: VIP {res['status']['vip_level']})")

    print("\n>>> ALL 10 WEB API TESTS PASSED 100%! <<<")

if __name__ == "__main__":
    main()
