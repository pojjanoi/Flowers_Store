#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script ตรวจสอบสถานะฐานข้อมูล Flowers Store
"""

import sqlite3
from pathlib import Path

def check_database():
    """ตรวจสอบสถานะของฐานข้อมูล"""
    db_path = Path(__file__).parent / "flowers_store.db"
    
    print("=" * 80)
    print("📊 สถานะฐานข้อมูล Flowers Store")
    print("=" * 80)
    
    if not db_path.exists():
        print(f"❌ ไม่พบไฟล์ฐานข้อมูล: {db_path}")
        return
    
    print(f"✅ ไฟล์ฐานข้อมูล: {db_path}")
    print(f"📦 ขนาด: {db_path.stat().st_size:,} bytes")
    print()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # ตรวจสอบตาราง
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📋 ตารางที่มีในฐานข้อมูล:")
        print("-" * 80)
        for table in tables:
            print(f"  • {table[0]}")
        print()
        
        # ตรวจสอบจำนวนข้อมูล
        print("📊 จำนวนข้อมูลในแต่ละตาราง:")
        print("-" * 80)
        
        cursor.execute("SELECT COUNT(*) FROM Categories")
        cat_count = cursor.fetchone()[0]
        print(f"  Categories: {cat_count} รายการ")
        
        cursor.execute("SELECT COUNT(*) FROM Flowers")
        flower_count = cursor.fetchone()[0]
        print(f"  Flowers: {flower_count} รายการ")
        print()
        
        # แสดงข้อมูล Categories
        print("📦 ข้อมูล Categories:")
        print("-" * 80)
        cursor.execute("SELECT * FROM Categories")
        categories = cursor.fetchall()
        for cat in categories:
            print(f"  ID: {cat[0]} | {cat[1]}")
        print()
        
        # แสดงข้อมูล Flowers
        print("🌸 ข้อมูล Flowers:")
        print("-" * 80)
        cursor.execute("""
            SELECT f.flower_id, f.flower_name, c.category_name, f.price, f.quantity
            FROM Flowers f
            JOIN Categories c ON f.category_id = c.category_id
            ORDER BY f.flower_id
        """)
        flowers = cursor.fetchall()
        for flower in flowers:
            print(f"  {flower[0]}. {flower[1]:30} | {flower[2]:20} | ฿{flower[3]:8.2f} | {flower[4]:3} ชอ")
        print()
        
        print("=" * 80)
        print("✅ ฐานข้อมูลทำงานได้ปกติ")
        print("=" * 80)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ ข้อผิดพลาด: {e}")

if __name__ == "__main__":
    check_database()
