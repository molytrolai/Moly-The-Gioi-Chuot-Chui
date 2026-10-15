import subprocess
import urllib.request
import json
import sys

def get_token():
    p = subprocess.Popen(
        ['git', 'credential', 'fill'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = p.communicate('protocol=https\nhost=github.com\nusername=Vandaoaudio\n\n')
    for line in out.splitlines():
        if line.startswith('password='):
            return line.split('=', 1)[1]
    return None

def main():
    token = get_token()
    if not token:
        print("No token found for Vandaoaudio")
        sys.exit(1)

    req = urllib.request.Request(
        'https://api.github.com/user/repository_invitations',
        headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'User-Agent': 'Moly-Agent'
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            invitations = json.loads(resp.read().decode())
            print(f"Pending invitations count: {len(invitations)}")
            for inv in invitations:
                repo_name = inv.get('repository', {}).get('full_name')
                inv_id = inv.get('id')
                print(f"Found invitation {inv_id} for {repo_name}")
                if 'Moly-The-Gioi-Chuot-Chui' in repo_name:
                    accept_req = urllib.request.Request(
                        f'https://api.github.com/user/repository_invitations/{inv_id}',
                        headers={
                            'Authorization': f'Bearer {token}',
                            'Accept': 'application/vnd.github+json',
                            'User-Agent': 'Moly-Agent'
                        },
                        method='PATCH'
                    )
                    with urllib.request.urlopen(accept_req) as a_resp:
                        print(f"ACCEPTED invitation {inv_id} for {repo_name}! Status: {a_resp.status}")
    except Exception as e:
        print(f"Error checking invitations: {e}")

if __name__ == '__main__':
    main()
