@echo off
title Moly - The Gioi Chuot Chui VN
cd /d "%~dp0"

:: 1. Kiem tra va khoi dong proxy tai nguyen (Port 18080) chay ngam hoan toan qua pythonw
netstat -ano | findstr :18080 >nul 2>&1
if errorlevel 1 (
    start "" pythonw tools\capture_proxy.py --archive archive\clients\captured-live --host 127.0.0.1 --port 18080 --local-server 127.0.0.1 --overrides archive\clients\local-overrides --mirror archive\clients\offline-mirror
    timeout /t 1 /nobreak >nul
)

:: 2. Kiem tra va khoi dong game server (Port 1863) chay ngam hoan toan qua pythonw
netstat -ano | findstr :1863 >nul 2>&1
if errorlevel 1 (
    start "" pythonw tools\moly_probe_server.py --log data\server\probe-events.jsonl
    timeout /t 1 /nobreak >nul
)

:: 3. Mo truc tiep cua so game Ruffle va tu dong dong bang lenh nay
start "" "%~dp0tools\ruffle-0.7.1\ruffle.exe" http://127.0.0.1:18080/Client.swf --tcp-connections allow --scale show-all --force-scale --width 1024 --height 768
exit
