@echo off
REM Script สำหรับรัน Flask Application บน Windows
REM ความสามารถ: อ่านไฟล์ .env และตั้งค่า environment variables

cd /d "%~dp0"

echo.
echo ====================================================
echo    ระบบจัดการร้านดอกไม้ - Flowers Store System
echo ====================================================
echo.

REM ตรวจสอบว่า Python ติดตั้งแล้วหรือไม่
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python ไม่ได้ติดตั้ง กรุณาติดตั้ง Python ก่อน
    pause
    exit /b 1
)

echo ✓ Python ติดตั้งแล้ว
echo.

REM ตรวจสอบว่า requirements.txt มีอยู่
if not exist "requirements.txt" (
    echo ❌ ไม่พบไฟล์ requirements.txt
    pause
    exit /b 1
)

echo ✓ ไฟล์ requirements.txt พบแล้ว
echo.

REM ติดตั้ง dependencies
echo 📦 กำลังติดตั้ง/อัพเดต dependencies...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ ติดตั้ง dependencies ไม่สำเร็จ
    pause
    exit /b 1
)

echo ✓ ติดตั้ง dependencies สำเร็จ
echo.

REM ตรวจสอบว่า app.py มีอยู่
if not exist "app.py" (
    echo ❌ ไม่พบไฟล์ app.py
    pause
    exit /b 1
)

echo ✓ ไฟล์ app.py พบแล้ว
echo.

REM ตรวจสอบว่า flowers_store.db มีอยู่
if not exist "flowers_store.db" (
    echo ⚠ ไม่พบไฟล์ฐานข้อมูล flowers_store.db
    echo 🔨 กำลังสร้างฐานข้อมูล...
    python create_database.py
)

echo.
echo ====================================================
echo    🚀 กำลังรัน Flask Application...
echo ====================================================
echo.
echo 📍 URL: http://localhost:5000
echo 🛑 กด Ctrl+C เพื่อหยุดการทำงาน
echo.

REM รัน Flask Application
python app.py

pause
