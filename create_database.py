import sqlite3
from pathlib import Path

# กำหนดพาธของไฟล์ฐานข้อมูล
db_path = Path(__file__).parent / "flowers_store.db"

# ลบไฟล์ฐานข้อมูลเก่า (ถ้ามี) เพื่อสร้างใหม่
if db_path.exists():
    db_path.unlink()

# เชื่อมต่อไปยังฐานข้อมูล SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 80)
print("สร้างฐานข้อมูล SQLite สำหรับระบบร้านขายดอกไม้")
print("=" * 80)

# ===== สร้างตาราง Categories (ตารางรอง) =====
print("\n📦 กำลังสร้างตาราง Categories (ตารางรอง)...")
cursor.execute('''
CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE
)
''')
print("✓ ตาราง Categories สร้างสำเร็จ")

# ===== สร้างตาราง Flowers (ตารางหลัก) =====
print("\n🌸 กำลังสร้างตาราง Flowers (ตารางหลัก)...")
cursor.execute('''
CREATE TABLE Flowers (
    flower_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flower_name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    price REAL NOT NULL CHECK(price > 0),
    quantity INTEGER NOT NULL CHECK(quantity >= 0),
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
)
''')
print("✓ ตาราง Flowers สร้างสำเร็จ")

# ===== เพิ่มข้อมูลตัวอย่างในตาราง Categories =====
print("\n📝 กำลังเพิ่มข้อมูลตัวอย่างในตาราง Categories...")
categories_data = [
    ("ดอกไม้สด"),
    ("ดอกไม้ประดิษฐ์"),
    ("ดอกไม้ตากแห้ง"),
]
cursor.executemany("INSERT INTO Categories (category_name) VALUES (?)", 
                   [(cat,) for cat in categories_data])
print(f"✓ เพิ่มข้อมูล Categories {len(categories_data)} รายการ")

# ===== เพิ่มข้อมูลตัวอย่างในตาราง Flowers =====
print("\n🌺 กำลังเพิ่มข้อมูลตัวอย่างในตาราง Flowers...")
flowers_data = [
    ("กุหลาบแดง", 1, 50.00, 25, "ดอกไม้สดสีแดงสวยงาม เหมาะสำหรับวันวาเลนไทน์"),
    ("แสนดอกเหม", 1, 35.00, 15, "ดอกไม้สดสีขาว มีกลิ่นหอม เหมาะสำหรับบอกรักปฏิเสธการแต่งงาน"),
    ("ดอกเดซี่ประดิษฐ์", 2, 20.00, 30, "ดอกไม้ประดิษฐ์คุณภาพสูง ไม่เหี่ยว ทนทานนาน"),
    ("ดอกไม้ตากแห้งรวมมิตร", 3, 15.00, 50, "ชุดดอกไม้ตากแห้งสำหรับตกแต่งบ้าน สวย ติดทน"),
    ("กุหลาบขาว", 1, 45.00, 20, "ดอกไม้สดสีขาว แสดงความบริสุทธิ์ เหมาะสำหรับงานแต่งงาน"),
]
cursor.executemany(
    "INSERT INTO Flowers (flower_name, category_id, price, quantity, description) VALUES (?, ?, ?, ?, ?)",
    flowers_data
)
print(f"✓ เพิ่มข้อมูล Flowers {len(flowers_data)} รายการ")

# บันทึกการเปลี่ยนแปลง
conn.commit()

# ===== แสดงข้อมูลที่เพิ่มเข้ามา =====
print("\n" + "=" * 80)
print("📊 ข้อมูลที่เหก็บไว้ในฐานข้อมูล")
print("=" * 80)

print("\n📦 ข้อมูลในตาราง Categories:")
print("-" * 80)
cursor.execute("SELECT * FROM Categories")
categories = cursor.fetchall()
for cat_id, cat_name in categories:
    print(f"  ID: {cat_id} | ชื่อหมวดหมู่: {cat_name}")

print("\n🌸 ข้อมูลในตาราง Flowers:")
print("-" * 80)
cursor.execute('''
SELECT f.flower_id, f.flower_name, c.category_name, f.price, f.quantity, f.description
FROM Flowers f
INNER JOIN Categories c ON f.category_id = c.category_id
''')
flowers = cursor.fetchall()
for flower in flowers:
    print(f"\n  🌺 ID: {flower[0]}")
    print(f"     ชื่อดอกไม้: {flower[1]}")
    print(f"     หมวดหมู่: {flower[2]}")
    print(f"     ราคา: ฿{flower[3]:.2f}")
    print(f"     จำนวนคงเหลือ: {flower[4]} ชอ")
    print(f"     รายละเอียด: {flower[5]}")

# ===== อธิบายประเภทข้อมูลในแต่ละคอลัมน์ =====
print("\n" + "=" * 80)
print("📋 รายละเอียดประเภทข้อมูล (Data Types) ในแต่ละคอลัมน์")
print("=" * 80)

print("\n📦 ตาราง Categories (ตารางรอง):")
print("-" * 80)
schema_categories = [
    ("category_id", "INTEGER", "รหัสหมวดหมู่ (คีย์หลัก) เพิ่มอัตโนมัติ"),
    ("category_name", "TEXT", "ชื่อหมวดหมู่ (ต้องไม่ซ้ำกัน)"),
]
for col_name, data_type, description in schema_categories:
    print(f"  • {col_name:20} | {data_type:15} | {description}")

print("\n🌸 ตาราง Flowers (ตารางหลัก):")
print("-" * 80)
schema_flowers = [
    ("flower_id", "INTEGER", "รหัสดอกไม้ (คีย์หลัก) เพิ่มอัตโนมัติ"),
    ("flower_name", "TEXT", "ชื่อดอกไม้ (ต้องไม่ว่าง)"),
    ("category_id", "INTEGER", "รหัสหมวดหมู่ (Foreign Key ไปยัง Categories)"),
    ("price", "REAL", "ราคาดอกไม้เป็นบาท (ต้องมากกว่า 0)"),
    ("quantity", "INTEGER", "จำนวนดอกไม้ที่มีในคลัง (ต้องมากกว่าหรือเท่ากับ 0)"),
    ("description", "TEXT", "รายละเอียดการนำเสนอสินค้า"),
]
for col_name, data_type, description in schema_flowers:
    print(f"  • {col_name:20} | {data_type:15} | {description}")

print("\n🔗 ความสัมพันธ์ (Foreign Key Relationship):")
print("-" * 80)
print("  • Flowers.category_id → Categories.category_id")
print("    (ทุกรายการดอกไม้ต้องมีหมวดหมู่ที่มีอยู่ในตาราง Categories)")

# ปิดการเชื่อมต่อ
conn.close()

print("\n" + "=" * 80)
print(f"✅ สร้างฐานข้อมูลสำเร็จ!")
print(f"📁 ไฟล์ฐานข้อมูล: {db_path}")
print("=" * 80)
