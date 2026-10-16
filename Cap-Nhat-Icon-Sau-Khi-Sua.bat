@echo off
chcp 65001 >nul
title CẬP NHẬT ICON VÀO GAME MOLY VN
cd /d "%~dp0"

echo ======================================================================
echo    ĐANG TỰ ĐỘNG CẬP NHẬT ẢNH ICON ĐÃ SỬA VÀO GAME MOLY VN...
echo ======================================================================
echo.

python tools\cap_nhat_icon_sau_khi_sua.py

echo.
pause
