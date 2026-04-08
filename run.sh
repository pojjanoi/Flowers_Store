#!/bin/bash

# Script สำหรับรัน Flask Application บน Linux/Mac

echo ""
echo "===================================================="
echo "    ระบบจัดการร้านดอกไม้ - Flowers Store System"
echo "===================================================="
echo ""

# ตรวจสอบว่า Python ติดตั้งแล้วหรือไม่
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ไม่ได้ติดตั้ง กรุณาติดตั้ง Python 3 ก่อน"
    exit 1
fi

echo "✓ Python ติดตั้งแล้ว"
echo ""

# ตรวจสอบว่า requirements.txt มีอยู่
if [ ! -f "requirements.txt" ]; then
    echo "❌ ไม่พบไฟล์ requirements.txt"
    exit 1
fi

echo "✓ ไฟล์ requirements.txt พบแล้ว"
echo ""

# ติดตั้ง dependencies
echo "📦 กำลังติดตั้ง/อัพเดต dependencies..."
pip3 install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ ติดตั้ง dependencies ไม่สำเร็จ"
    exit 1
fi

echo "✓ ติดตั้ง dependencies สำเร็จ"
echo ""

# ตรวจสอบว่า app.py มีอยู่
if [ ! -f "app.py" ]; then
    echo "❌ ไม่พบไฟล์ app.py"
    exit 1
fi

echo "✓ ไฟล์ app.py พบแล้ว"
echo ""

# ตรวจสอบว่า flowers_store.db มีอยู่
if [ ! -f "flowers_store.db" ]; then
    echo "⚠ ไม่พบไฟล์ฐานข้อมูล flowers_store.db"
    echo "🔨 กำลังสร้างฐานข้อมูล..."
    python3 create_database.py
fi

echo ""
echo "===================================================="
echo "    🚀 กำลังรัน Flask Application..."
echo "===================================================="
echo ""
echo "📍 URL: http://localhost:5000"
echo "🛑 กด Ctrl+C เพื่อหยุดการทำงาน"
echo ""

# รัน Flask Application
python3 app.py
