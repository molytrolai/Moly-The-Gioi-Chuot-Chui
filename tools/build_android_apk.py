#!/usr/bin/env python3
"""Builds the standalone Android APK for Moly - The Gioi Chuot Chui.

Outputs: web/download/Moly Thế Giới Chuột chũi.apk
Uses Android SDK build-tools 35.0.1 and JDK 21.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANDROID_DIR = PROJECT_ROOT / "android"
OUTPUT_DIR = PROJECT_ROOT / "web" / "download"
APK_OUTPUT = OUTPUT_DIR / "Moly Thế Giới Chuột chũi.apk"

SDK_ROOT = Path(r"C:\Users\Admin\AppData\Local\Android\Sdk")
BUILD_TOOLS = SDK_ROOT / "build-tools" / "35.0.1"
PLATFORM_JAR = SDK_ROOT / "platforms" / "android-35" / "android.jar"

AAPT2 = BUILD_TOOLS / "aapt2.exe"
D8 = BUILD_TOOLS / "d8.bat"
ZIPALIGN = BUILD_TOOLS / "zipalign.exe"
APKSIGNER = BUILD_TOOLS / "apksigner.bat"

KEYSTORE_PATH = ANDROID_DIR / "molyviet-release.jks"
KEY_ALIAS = "molyviet"
KEY_PASS = "molyviet2026"


def setup_project_structure() -> None:
    print("[*] Setting up Android project structure...")
    res_dir = ANDROID_DIR / "src" / "main" / "res"
    values_dir = res_dir / "values"
    values_dir.mkdir(parents=True, exist_ok=True)

    # 1. AndroidManifest.xml (Minimal permissions: INTERNET & ACCESS_NETWORK_STATE only - no popup prompts)
    manifest_path = ANDROID_DIR / "src" / "main" / "AndroidManifest.xml"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.molyviet.thegioichuotchui"
    android:versionCode="2"
    android:versionName="1.1.0">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:label="@string/app_name"
        android:icon="@mipmap/ic_launcher"
        android:theme="@style/AppTheme"
        android:hardwareAccelerated="true"
        android:usesCleartextTraffic="true"
        android:largeHeap="true">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="sensorLandscape"
            android:configChanges="orientation|screenSize|keyboardHidden|smallestScreenSize|screenLayout"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
    manifest_path.write_text(manifest_content, encoding="utf-8")

    # 2. strings.xml & styles.xml
    (values_dir / "strings.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Moly Thế Giới Chuột chũi</string>
</resources>
""", encoding="utf-8")

    (values_dir / "styles.xml").write_text("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="@android:style/Theme.NoTitleBar.Fullscreen">
        <item name="android:windowBackground">@android:color/black</item>
        <item name="android:windowFullscreen">true</item>
        <item name="android:windowContentOverlay">@null</item>
    </style>
</resources>
""", encoding="utf-8")

    # 3. Generate launcher icons from logo-square.png
    logo_path = PROJECT_ROOT / "web" / "assets" / "logo-square.png"
    if logo_path.is_file():
        img = Image.open(logo_path)
        icon_sizes = {
            "mipmap-mdpi": (48, 48),
            "mipmap-hdpi": (72, 72),
            "mipmap-xhdpi": (96, 96),
            "mipmap-xxhdpi": (144, 144),
            "mipmap-xxxhdpi": (192, 192),
        }
        for folder, size in icon_sizes.items():
            folder_path = res_dir / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            resized = img.resize(size, Image.Resampling.LANCZOS)
            resized.save(folder_path / "ic_launcher.png", format="PNG")
        print("  -> Generated app icons in mipmap folders.")

    # 4. MainActivity.java
    java_dir = ANDROID_DIR / "src" / "main" / "java" / "com" / "molyviet" / "thegioichuotchui"
    java_dir.mkdir(parents=True, exist_ok=True)
    main_activity = """package com.molyviet.thegioichuotchui;

import android.app.Activity;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView webView;
    private static final String ONLINE_URL = "https://molyvn.onrender.com/play.html";
    private static final String OFFLINE_URL = "file:///android_asset/offline.html";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);

        setImmersiveMode();

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setMediaPlaybackRequiresUserGesture(false);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                if (failingUrl != null && failingUrl.startsWith("http")) {
                    view.loadUrl(OFFLINE_URL);
                }
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request != null && request.isForMainFrame()) {
                    view.loadUrl(OFFLINE_URL);
                }
            }
        });
        webView.setWebChromeClient(new WebChromeClient());

        // Load live synchronized game world directly
        webView.loadUrl(ONLINE_URL);
    }

    private void setImmersiveMode() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            getWindow().getDecorView().setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                    | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                    | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                    | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    | View.SYSTEM_UI_FLAG_FULLSCREEN
                    | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
        }
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            setImmersiveMode();
        }
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
"""
    (java_dir / "MainActivity.java").write_text(main_activity, encoding="utf-8")
    print("  -> Created MainActivity.java with Immersive Mode and WebAssembly WebView.")


def setup_mobile_assets() -> None:
    print("[*] Preparing mobile assets in android/src/main/assets...")
    assets_dir = ANDROID_DIR / "src" / "main" / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Copy ruffle wasm bundle
    ruffle_src = PROJECT_ROOT / "web" / "static" / "ruffle"
    ruffle_dst = assets_dir / "static" / "ruffle"
    if ruffle_dst.exists():
        shutil.rmtree(ruffle_dst)
    shutil.copytree(ruffle_src, ruffle_dst)

    # Copy assets (logos)
    logo_dst = assets_dir / "assets"
    logo_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy(PROJECT_ROOT / "web" / "assets" / "logo-square.png", logo_dst / "logo-square.png")
    shutil.copy(PROJECT_ROOT / "web" / "assets" / "logo-horizontal.png", logo_dst / "logo-horizontal.png")

    # Offline retry page
    offline_html = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Moly VN - Kết Nối Máy Chủ</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 100vw; height: 100vh;
      background: #0f172a;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #f8fafc;
      text-align: center;
      padding: 24px;
    }
    .logo {
      width: 80px; height: 80px;
      border-radius: 18px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.4);
      margin-bottom: 16px;
    }
    h2 { font-size: 20px; font-weight: 800; color: #ff7e1b; margin-bottom: 8px; }
    p { font-size: 14px; color: #94a3b8; max-width: 420px; line-height: 1.5; margin-bottom: 24px; }
    .btn-retry {
      background: linear-gradient(135deg, #ff7e1b, #ea580c);
      color: #ffffff;
      border: none;
      padding: 12px 32px;
      font-size: 15px;
      font-weight: 700;
      border-radius: 9999px;
      cursor: pointer;
      box-shadow: 0 6px 16px rgba(234, 88, 12, 0.4);
    }
  </style>
</head>
<body>
  <img src="assets/logo-square.png" alt="Moly" class="logo">
  <h2>VƯƠNG QUỐC CHUỘT CHŨI (MOLY VN)</h2>
  <p>Không thể kết nối đến máy chủ trực tuyến. Vui lòng kiểm tra lại kết nối WiFi hoặc dữ liệu 4G/5G trên điện thoại và nhấn Thử Lại nhé!</p>
  <button class="btn-retry" onclick="window.location.href='https://molyvn.onrender.com/play.html'">🔄 THỬ LẠI KẾT NỐI</button>
</body>
</html>
"""
    (assets_dir / "offline.html").write_text(offline_html, encoding="utf-8")

    # Mobile play HTML (standalone local fallback)
    mobile_html = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Moly Mobile</title>
  <script src="static/ruffle/ruffle.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body {
      width: 100%; height: 100%;
      background: #000000;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    #game-container {
      width: 100vw;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    #moly-player {
      width: 100% !important;
      height: 100% !important;
    }
    #loading {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: #0f172a;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12px;
      color: #94a3b8;
      font-family: sans-serif;
      font-size: 14px;
      z-index: 99;
    }
    #loading img {
      width: 80px; height: 80px;
      border-radius: 18px;
    }
    .spinner {
      width: 28px; height: 28px;
      border: 3px solid rgba(255,255,255,0.2);
      border-top-color: #ff7e1b;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <div id="loading">
    <img src="assets/logo-square.png" alt="Moly">
    <div class="spinner"></div>
    <div>Đang kết nối Vương Quốc Chuột Chũi Moly VN...</div>
  </div>
  <div id="game-container"></div>

  <script>
    window.RufflePlayer = window.RufflePlayer || {};
    const SERVER_HOST = "molyvn.onrender.com";
    window.RufflePlayer.config = {
      letterbox: "on",
      allowScriptAccess: true,
      scale: "showAll",
      socketProxy: [
        { host: "127.0.0.1", port: 1863, proxyUrl: `wss://${SERVER_HOST}/ws/1863` },
        { host: "127.0.0.1", port: 3200, proxyUrl: `wss://${SERVER_HOST}/ws/3200` },
        { host: "123.206.131.236", port: 1863, proxyUrl: `wss://${SERVER_HOST}/ws/1863` },
        { host: "123.206.131.63", port: 3200, proxyUrl: `wss://${SERVER_HOST}/ws/3200` }
      ]
    };

    window.addEventListener("DOMContentLoaded", () => {
      const container = document.getElementById("game-container");
      const loading = document.getElementById("loading");
      try {
        const ruffle = window.RufflePlayer.newest();
        const player = ruffle.createPlayer();
        player.id = "moly-player";
        container.appendChild(player);

        player.load({
          url: `https://${SERVER_HOST}/Client.swf?v=20261017_apk`,
          parameters: {}
        }).then(() => {
          setTimeout(() => { loading.style.display = "none"; }, 800);
        }).catch(err => {
          loading.innerText = "Lỗi tải game: " + err;
        });
      } catch (err) {
        loading.innerText = "Lỗi Ruffle: " + err;
      }
    });
  </script>
</body>
</html>
"""
    (assets_dir / "mobile.html").write_text(mobile_html, encoding="utf-8")
    print("  -> Prepared mobile assets.")


def compile_and_build_apk() -> None:
    build_dir = ANDROID_DIR / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    res_compiled = build_dir / "compiled_res.zip"
    gen_dir = build_dir / "gen"
    gen_dir.mkdir(parents=True, exist_ok=True)
    bin_dir = build_dir / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    res_dir = ANDROID_DIR / "src" / "main" / "res"
    manifest_path = ANDROID_DIR / "src" / "main" / "AndroidManifest.xml"
    assets_dir = ANDROID_DIR / "src" / "main" / "assets"

    # Step 1: AAPT2 compile
    print("[Step 1] AAPT2 compile resources...")
    cmd_compile = [
        str(AAPT2),
        "compile",
        "--dir", str(res_dir),
        "-o", str(res_compiled),
    ]
    subprocess.check_call(cmd_compile)

    # Step 2: AAPT2 link
    print("[Step 2] AAPT2 link...")
    unaligned_apk = bin_dir / "unaligned.apk"
    cmd_link = [
        str(AAPT2),
        "link",
        "-I", str(PLATFORM_JAR),
        "-A", str(assets_dir),
        "--manifest", str(manifest_path),
        "--java", str(gen_dir),
        "-o", str(unaligned_apk),
        "--auto-add-overlay",
        str(res_compiled),
    ]
    subprocess.check_call(cmd_link)

    # Step 3: Compile Java with javac
    print("[Step 3] Compiling Java classes with javac...")
    classes_dir = build_dir / "classes"
    classes_dir.mkdir(parents=True, exist_ok=True)

    java_sources = list((ANDROID_DIR / "src" / "main" / "java").rglob("*.java")) + list(gen_dir.rglob("*.java"))
    cmd_javac = [
        "javac",
        "-encoding", "utf-8",
        "-source", "1.8",
        "-target", "1.8",
        "-cp", str(PLATFORM_JAR),
        "-d", str(classes_dir),
    ] + [str(p) for p in java_sources]
    subprocess.check_call(cmd_javac)

    # Step 4: D8 convert .class to classes.dex
    print("[Step 4] D8 dexing classes...")
    class_files = [str(p) for p in classes_dir.rglob("*.class")]
    dex_output = build_dir / "dex"
    dex_output.mkdir(parents=True, exist_ok=True)
    cmd_d8 = [
        str(D8),
        "--output", str(dex_output),
        "--lib", str(PLATFORM_JAR),
    ] + class_files
    subprocess.check_call(cmd_d8, shell=True)

    # Step 5: Add classes.dex into unaligned.apk
    print("[Step 5] Adding classes.dex to APK...")
    dex_file = dex_output / "classes.dex"
    with zipfile.ZipFile(unaligned_apk, "a") as zf:
        zf.write(dex_file, "classes.dex")

    # Step 6: Zipalign APK
    print("[Step 6] Running zipalign...")
    aligned_apk = bin_dir / "aligned.apk"
    if aligned_apk.exists():
        aligned_apk.unlink()
    cmd_align = [
        str(ZIPALIGN),
        "-f",
        "4",
        str(unaligned_apk),
        str(aligned_apk),
    ]
    subprocess.check_call(cmd_align)

    # Step 7: Create release keystore if needed
    if not KEYSTORE_PATH.exists():
        print("[Step 7] Generating release keystore...")
        cmd_key = [
            "keytool",
            "-genkeypair",
            "-v",
            "-keystore", str(KEYSTORE_PATH),
            "-alias", KEY_ALIAS,
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-storepass", KEY_PASS,
            "-keypass", KEY_PASS,
            "-dname", "CN=MolyViet, OU=Gaming, O=MolyViet, L=Hanoi, ST=Hanoi, C=VN",
        ]
        subprocess.check_call(cmd_key)

    # Step 8: Sign APK with apksigner
    print("[Step 8] Signing APK with apksigner...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    signed_apk = bin_dir / "signed.apk"
    if signed_apk.exists():
        signed_apk.unlink()

    cmd_sign = [
        str(APKSIGNER),
        "sign",
        "--ks", str(KEYSTORE_PATH),
        "--ks-key-alias", KEY_ALIAS,
        "--ks-pass", f"pass:{KEY_PASS}",
        "--key-pass", f"pass:{KEY_PASS}",
        "--out", str(signed_apk),
        str(aligned_apk),
    ]
    subprocess.check_call(cmd_sign, shell=True)

    # Copy signed apk to final Unicode destination using Python
    shutil.copy2(signed_apk, APK_OUTPUT)

    size_mb = APK_OUTPUT.stat().st_size / (1024 * 1024)
    print(f"\n[OK] Successfully built and signed: '{APK_OUTPUT.name}' ({size_mb:.2f} MB)")


if __name__ == "__main__":
    setup_project_structure()
    setup_mobile_assets()
    compile_and_build_apk()
