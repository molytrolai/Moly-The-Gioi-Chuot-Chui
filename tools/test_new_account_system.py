import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))
from account_system import accounts, DEFAULT_MOLY_ADMIN_ID, LEGACY_MOLY_ADMIN_ID

def main():
    print("Testing New Account System & Admin 0 Configuration...")

    # 1. Admin account checks
    admin0 = accounts.get_account(0)
    assert admin0 is not None, "Admin 0 not found"
    assert admin0["user_id"] == 0, f"Admin ID is {admin0['user_id']}, expected 0"
    assert admin0["username"] == "00000000", f"Admin username is {admin0.get('username')}, expected 00000000"
    assert admin0["is_admin"] is True, "Admin 0 is not admin"
    assert admin0["vip_level"] == 19, "Admin 0 is not VIP 19"
    print("  [PASS] 1. Admin 0 account verified: user_id=0, username=00000000, VIP 19")

    # 2. Authentication with 0, 00000000, admin
    ok1, _ = accounts.authenticate("0", "*")
    ok2, _ = accounts.authenticate("00000000", "*")
    ok3, _ = accounts.authenticate("admin", "*")
    ok4, _ = accounts.authenticate(0, "*")
    assert ok1 and ok2 and ok3 and ok4, f"Admin auth failed: {ok1}, {ok2}, {ok3}, {ok4}"
    print("  [PASS] 2. Admin multi-identifier authentication verified (0, 00000000, admin)")

    # 3. Create account with random ID & username validation
    import time
    u_test = f"testuser_{int(time.time())}"
    acc = accounts.create_account(
        password="secretpassword123",
        username=u_test,
        fullname="Nguyễn Văn Test",
        nickname="Chuột Chũi Dũng Cảm",
        email=f"{u_test}@gmail.com",
        birthday="2005-08-15",
        gold_beans=1000
    )
    uid = acc["user_id"]
    assert 10000000 <= uid <= 99999999, f"UID {uid} not in 8-digit range"
    assert acc["username"] == u_test
    assert acc["fullname"] == "Nguyễn Văn Test"
    assert acc["birthday"] == "2005-08-15"
    print(f"  [PASS] 3. Account created with random 8-digit ID: {uid} (Username: {u_test})")

    # 4. Authentication using username, ID, and email
    ok_u, _ = accounts.authenticate(u_test, "secretpassword123")
    ok_i, _ = accounts.authenticate(uid, "secretpassword123")
    ok_e, _ = accounts.authenticate(f"{u_test}@gmail.com", "secretpassword123")
    assert ok_u and ok_i and ok_e, "User multi-identifier auth failed"
    print("  [PASS] 4. User auth via username, ID, and email verified")

    # 5. Immutable username check
    accounts.update_account(uid, {"username": "hacked_name", "fullname": "Tên Mới Đã Sửa"})
    acc_check = accounts.get_account(uid)
    assert acc_check["username"] == u_test, "Username was incorrectly changed!"
    assert acc_check["fullname"] == "Tên Mới Đã Sửa", "Fullname update failed"
    print("  [PASS] 5. Username immutability verified (username cannot be changed)")

    # 6. Update profile
    ok_up, msg_up, acc_up = accounts.update_profile(uid, fullname="Họ Tên Cập Nhật", nickname="Biệt Danh Mới", birthday="2004-12-30")
    assert ok_up and acc_up["fullname"] == "Họ Tên Cập Nhật" and acc_up["birthday"] == "2004-12-30"
    print("  [PASS] 6. Profile update verified (Fullname, Nickname, Birthday)")

    # 7. Password reset before login
    ok_res, msg_res = accounts.reset_password_with_info(u_test, f"{u_test}@gmail.com", "2004-12-30", "new_secure_pwd_999")
    assert ok_res, f"Reset password failed: {msg_res}"
    ok_new, _ = accounts.authenticate(u_test, "new_secure_pwd_999")
    assert ok_new, "Auth with new reset password failed"
    print("  [PASS] 7. Forgot password reset before login verified")

    print("\n>>> ALL 7 NEW ACCOUNT CAPABILITIES VERIFIED 100% SUCCEEDED! <<<")

if __name__ == "__main__":
    main()
