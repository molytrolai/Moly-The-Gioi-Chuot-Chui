import urllib.request
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.push_to_github import get_token
DOWNLOAD_DIR = PROJECT_ROOT / "web" / "download"
APK_PATH = DOWNLOAD_DIR / "Moly Thế Giới Chuột chũi.apk"
ZIP_PATH = DOWNLOAD_DIR / "Moly Thế Giới Chuột chũi.zip"

def main():
    token = get_token()
    if not token:
        print("[ERROR] Token not found.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Moly-Agent"
    }

    # 1. Create or get Release v1.0.0
    rel_url = "https://api.github.com/repos/molytrolai/Moly-The-Gioi-Chuot-Chui/releases"
    payload = {
        "tag_name": "v1.0.0",
        "target_commitish": "main",
        "name": "Moly - Thế Giới Chuột Chũi VN v1.0.0 (Bản Chính Thức)",
        "body": """## 🌟 Moly - Thế Giới Chuột Chũi VN — Bản Phát Hành Chính Thức v1.0.0

Chào mừng toàn thể Cư dân trở về với Vương quốc Chuột chũi Moly tuổi thơ!

### 🎮 Các phiên bản tải về:
- **📱 Android APK (13.7 MB):** Tải file `Moly-The-Gioi-Chuot-Chui.apk` cài đặt trực tiếp trên điện thoại Android.
- **💻 Windows Desktop (150 MB):** Tải file `Moly-The-Gioi-Chuot-Chui-Windows.zip`, giải nén và bấm `Choi-Game.bat` để trải nghiệm mượt mà với Ruffle Native siêu tốc.
- **🌐 Chơi trực tiếp trên Web:** Truy cập ngay cổng game: https://moly-the-gioi-chuot-chui.onrender.com

### ✨ Điểm nổi bật:
- Việt hóa 100% 257 bản đồ, UI thanh công cụ, hội thoại NPC, Siêu LaMu, Nông trại và Lâu đài Moly.
- Cơ sở dữ liệu đám mây Neon PostgreSQL đồng bộ dữ liệu thời gian thực.
""",
        "draft": False,
        "prerelease": False
    }

    print("[1/3] Creating Release v1.0.0 on GitHub...")
    req = urllib.request.Request(rel_url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            rel = json.loads(resp.read().decode("utf-8"))
            print(f"[OK] Release created: {rel.get('html_url')}")
            upload_url_tmpl = rel.get("upload_url", "")
    except urllib.error.HTTPError as e:
        if e.code == 422: # Already exists
            print("[INFO] Release v1.0.0 already exists, fetching existing...")
            req_get = urllib.request.Request("https://api.github.com/repos/molytrolai/Moly-The-Gioi-Chuot-Chui/releases/tags/v1.0.0", headers=headers)
            with urllib.request.urlopen(req_get) as resp_get:
                rel = json.loads(resp_get.read().decode("utf-8"))
                upload_url_tmpl = rel.get("upload_url", "")
        else:
            print(f"[ERROR] Failed to create release: {e.code} {e.read().decode('utf-8')}")
            sys.exit(1)

    # Base upload URL: remove "{?name,label}"
    base_upload_url = upload_url_tmpl.split("{")[0]

    # 2. Upload APK
    if APK_PATH.is_file():
        print(f"[2/3] Uploading Android APK ({APK_PATH.stat().st_size / (1024*1024):.1f} MB)...")
        apk_data = APK_PATH.read_bytes()
        upload_apk_url = f"{base_upload_url}?name=Moly-The-Gioi-Chuot-Chui.apk"
        apk_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.android.package-archive",
            "User-Agent": "Moly-Agent"
        }
        try:
            req_apk = urllib.request.Request(upload_apk_url, data=apk_data, headers=apk_headers, method="POST")
            with urllib.request.urlopen(req_apk) as resp_apk:
                print("[OK] APK uploaded successfully!")
        except Exception as err:
            print(f"[WARNING] APK upload error: {err}")

    # 3. Upload ZIP (150MB)
    if ZIP_PATH.is_file():
        print(f"[3/3] Uploading Windows Desktop ZIP ({ZIP_PATH.stat().st_size / (1024*1024):.1f} MB)...")
        zip_data = ZIP_PATH.read_bytes()
        upload_zip_url = f"{base_upload_url}?name=Moly-The-Gioi-Chuot-Chui-Windows.zip"
        zip_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/zip",
            "User-Agent": "Moly-Agent"
        }
        try:
            req_zip = urllib.request.Request(upload_zip_url, data=zip_data, headers=zip_headers, method="POST")
            with urllib.request.urlopen(req_zip) as resp_zip:
                print("[OK] Desktop ZIP uploaded successfully!")
        except Exception as err:
            print(f"[WARNING] Desktop ZIP upload error: {err}")

    print("\n=== GITHUB RELEASE COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
