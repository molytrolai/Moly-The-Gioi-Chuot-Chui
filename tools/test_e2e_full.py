import urllib.request
import json
import random
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE = 'http://127.0.0.1:18080'

def post_json(path, data):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def run_tests():
    suffix = str(random.randint(1000, 9999))
    uname = f'moly_hero_{suffix}'
    email = f'hero_{suffix}@gmail.com'

    print('1. Testing registration with full user info...')
    reg_data = {
        'username': uname,
        'fullname': 'Nguyễn Hoàng Moly',
        'nickname': 'Hiệp Sĩ Moly',
        'email': email,
        'birthday': '2005-06-15',
        'password': 'Password123'
    }
    res = post_json('/api/user/register', reg_data)
    print('  Register response:', res['message'])
    assert res['ok'] is True, 'Registration failed'
    uid = res['user_id']
    assert 10000000 <= uid <= 99999999, f'ID must be 8-digit random: {uid}'
    print(f'  Generated random ID: {uid} (non-incremental)')

    print('2. Testing login by username...')
    login_uname = post_json('/api/user/login', {'identifier': uname, 'password': 'Password123'})
    assert login_uname['ok'] is True
    assert login_uname['account']['fullname'] == 'Nguyễn Hoàng Moly'
    print('  Login by username OK')

    print('3. Testing login by email...')
    login_em = post_json('/api/user/login', {'identifier': email, 'password': 'Password123'})
    assert login_em['ok'] is True
    print('  Login by email OK')

    print('4. Testing login by User ID...')
    login_uid = post_json('/api/user/login', {'identifier': str(uid), 'password': 'Password123'})
    assert login_uid['ok'] is True
    print('  Login by User ID OK')

    print('5. Testing update profile (fullname, birthday, nickname)...')
    up_res = post_json('/api/user/update_profile', {
        'user_id': uid,
        'fullname': 'Nguyễn Hoàng Moly Đệ Nhất',
        'nickname': 'Siêu Cư Dân',
        'email': email,
        'birthday': '2005-06-15'
    })
    assert up_res['ok'] is True
    print('  Profile updated OK')

    print('6. Testing change password inside account settings...')
    chg_res = post_json('/api/user/change_password', {
        'user_id': uid,
        'old_password': 'Password123',
        'new_password': 'NewPassword456'
    })
    assert chg_res['ok'] is True
    print('  Password changed inside OK')

    print('7. Testing password reset before login (forgot password)...')
    reset_res = post_json('/api/user/reset_password', {
        'identifier': uname,
        'email': email,
        'birthday': '2005-06-15',
        'new_password': 'ResetPassword789'
    })
    assert reset_res['ok'] is True
    print('  Password reset before login OK')

    print('8. Verifying login with newly reset password...')
    login_new = post_json('/api/user/login', {'identifier': uname, 'password': 'ResetPassword789'})
    assert login_new['ok'] is True
    print('  Login with reset password OK')

    print('9. Testing Admin login (Full 0: 00000000)...')
    admin_login = post_json('/api/user/login', {'identifier': '00000000', 'password': 'admin'})
    assert admin_login['ok'] is True
    assert admin_login['account']['user_id'] == 0
    assert admin_login['account']['username'] == '00000000'
    assert admin_login['account']['vip_level'] == 19
    print(f'  Admin login OK: ID={admin_login["account"]["user_id"]}, VIP={admin_login["account"]["vip_level"]}')

    print('10. Testing VIP & Beans recharge...')
    rec_res = post_json('/api/user/recharge_vip', {'user_id': uid, 'amount': 10000})
    assert rec_res['ok'] is True
    inf_res = post_json('/api/user/get_info', {'user_id': uid})
    assert inf_res['account']['vip_level'] >= 2
    assert inf_res['account']['vip_value'] >= 100
    print(f'  Recharge OK: VIP Level={inf_res["account"]["vip_level"]}, VIP Points={inf_res["account"]["vip_value"]}')

    print('\n=============================================')
    print(' ALL 10 TESTS PASSED WITH 100% SUCCESS!')
    print('=============================================')

if __name__ == '__main__':
    run_tests()
