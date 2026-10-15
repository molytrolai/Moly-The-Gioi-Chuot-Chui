import ctypes
from ctypes import wintypes
import subprocess
import sys

class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', wintypes.DWORD),
        ('Type', wintypes.DWORD),
        ('TargetName', wintypes.LPWSTR),
        ('Comment', wintypes.LPWSTR),
        ('LastWritten', wintypes.FILETIME),
        ('CredentialBlobSize', wintypes.DWORD),
        ('CredentialBlob', ctypes.POINTER(ctypes.c_byte)),
        ('Persist', wintypes.DWORD),
        ('AttributeCount', wintypes.DWORD),
        ('Attributes', ctypes.c_void_p),
        ('TargetAlias', wintypes.LPWSTR),
        ('UserName', wintypes.LPWSTR),
    ]

def get_token():
    advapi32 = ctypes.windll.advapi32
    CredReadW = advapi32.CredReadW
    CredReadW.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(CREDENTIAL))]
    CredReadW.restype = wintypes.BOOL

    pcred = ctypes.POINTER(CREDENTIAL)()
    target = 'GitHub - https://api.github.com/molytrolai'
    if CredReadW(target, 1, 0, ctypes.byref(pcred)):
        cred = pcred.contents
        raw_bytes = bytes(ctypes.string_at(cred.CredentialBlob, cred.CredentialBlobSize))
        token = raw_bytes.decode('utf-16-le', errors='ignore')
        if not token or not token.isascii():
            token = raw_bytes.decode('utf-8', errors='ignore')
        return token.strip()
    return None

def main():
    token = get_token()
    if not token:
        print("[ERROR] Token for molytrolai not found in Credential Manager.")
        sys.exit(1)

    print(f"[OK] Retrieved OAuth token for molytrolai (prefix: {token[:4]}..., length: {len(token)})")

    # Set remote URL with token
    auth_url = f"https://x-access-token:{token}@github.com/molytrolai/Moly-The-Gioi-Chuot-Chui.git"
    clean_url = "https://github.com/molytrolai/Moly-The-Gioi-Chuot-Chui.git"

    try:
        print("[1/3] Setting authenticated remote URL...")
        subprocess.run(["git", "remote", "set-url", "origin", auth_url], check=True)

        print("[2/3] Pushing main branch to GitHub...")
        result = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        if result.returncode != 0:
            print("[ERROR] git push failed!")
            sys.exit(result.returncode)
        print("[3/3] Push successful!")
    finally:
        print("[CLEANUP] Resetting remote URL to clean URL...")
        subprocess.run(["git", "remote", "set-url", "origin", clean_url], check=True)

if __name__ == "__main__":
    main()
