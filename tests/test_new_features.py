import urllib.request
import json
import zipfile
import io
import time

base = 'http://127.0.0.1:18080'

# 1. Leaderboard
req = urllib.request.urlopen(f'{base}/api/leaderboard?limit=5')
data = json.loads(req.read().decode('utf-8'))
assert data['ok'] == True
assert len(data['leaderboard']['beans']) > 0
print('Endpoint /api/leaderboard: OK')

# 2. Newspaper
req = urllib.request.urlopen(f'{base}/api/newspaper/latest')
data = json.loads(req.read().decode('utf-8'))
assert data['ok'] == True
assert len(data['headlines']) == 3
print('Endpoint /api/newspaper/latest: OK')

# 3. OTP Send & Verify
req_data = json.dumps({'identifier': '81870789'}).encode('utf-8')
req = urllib.request.Request(f'{base}/api/otp/send', data=req_data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode('utf-8'))
assert data['ok'] == True
debug_code = data.get('debug_otp')
print('Endpoint /api/otp/send: OK. Masked:', data['masked_email'])

if debug_code:
    req_data = json.dumps({'user_id': data['user_id'], 'otp_code': debug_code, 'new_password': 'test_pwd_reset_123'}).encode('utf-8')
    req = urllib.request.Request(f'{base}/api/otp/verify_and_reset', data=req_data, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req)
    res_data = json.loads(resp.read().decode('utf-8'))
    assert res_data['ok'] == True
    print('Endpoint /api/otp/verify_and_reset: OK')

# 4. Admin Login & Session
admin_login = json.dumps({'username': '00000000', 'password': 'password', 'pin': '888888'}).encode('utf-8')
req = urllib.request.Request(f'{base}/api/admin/login', data=admin_login, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
adm = json.loads(resp.read().decode('utf-8'))
assert adm['ok'] == True
token = adm['token']
print('Admin Login: OK. Token:', token[:10] + '...')

headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

# 5. Email Config GET & POST
req = urllib.request.Request(f'{base}/api/admin/email_config', headers=headers)
data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
assert data['ok'] == True
print('Endpoint /api/admin/email_config GET: OK')

cfg_payload = json.dumps({'gmail_user': 'test_admin@gmail.com', 'app_password': 'abcd efgh ijkl mnop', 'sender_name': 'Moly Test'}).encode('utf-8')
req = urllib.request.Request(f'{base}/api/admin/email/config', data=cfg_payload, headers=headers)
data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
assert data['ok'] == True
print('Endpoint /api/admin/email/config POST: OK')

# 6. Admin Ban / Unban / Give Item
ban_payload = json.dumps({'user_id': 10000002, 'reason': 'Test Ban API'}).encode('utf-8')
req = urllib.request.Request(f'{base}/api/admin/user/ban', data=ban_payload, headers=headers)
data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
assert data['ok'] == True
print('Endpoint /api/admin/user/ban: OK')

unban_payload = json.dumps({'user_id': 10000002}).encode('utf-8')
req = urllib.request.Request(f'{base}/api/admin/user/unban', data=unban_payload, headers=headers)
data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
assert data['ok'] == True
print('Endpoint /api/admin/user/unban: OK')

give_payload = json.dumps({'user_id': 10000002, 'item_id': 12001, 'count': 1, 'is_cloth': True}).encode('utf-8')
req = urllib.request.Request(f'{base}/api/admin/user/give_item', data=give_payload, headers=headers)
data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
assert data['ok'] == True
print('Endpoint /api/admin/user/give_item: OK')

# 7. Backup Download (.ZIP)
req = urllib.request.Request(f'{base}/api/admin/backup?token={token}')
resp = urllib.request.urlopen(req)
assert resp.headers.get('Content-Type') == 'application/zip'
zip_bytes = resp.read()
assert len(zip_bytes) > 0
zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
print('Endpoint /api/admin/backup ZIP: OK. Files in zip:', len(zf.namelist()), zf.namelist()[:3])

print('\n========================================')
print('ALL 7 FULL-STACK API ENDPOINTS VERIFIED 100%!')
print('========================================')
