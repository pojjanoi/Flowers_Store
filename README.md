# 🌸 ระบบจัดการร้านดอกไม้ (Flowers Store Management System)

ระบบจัดการร้านดอกไม้ที่สร้างด้วย **Flask** และ **SQLite** พร้อมด้วย UI สวยงามที่ใช้ **Tailwind CSS**

## 📋 ความสามารถของระบบ

### CRUD Operations (เพิ่ม, ดู, แก้ไข, ลบ)
- ✅ **เพิ่มดอกไม้ใหม่** (Create) - เพิ่มรายการดอกไม้พร้อมข้อมูลทั้งหมด
- ✅ **ดูรายการทั้งหมด** (Read) - แสดงรายการดอกไม้ทั้งหมดด้วยไดโชว์สวยงาม
- ✅ **ดูรายละเอียด** (Read Single) - แสดงรายละเอียดแต่ละรายการอย่างละเอียด
- ✅ **แก้ไขข้อมูล** (Update) - อัพเดทข้อมูลดอกไม้
- ✅ **ลบรายการ** (Delete) - ลบรายการดอกไม้ที่ไม่ต้องการ

## 📦 โครงสร้างไฟล์

```
Flowers_Store/
├── app.py                          # Flask Application หลัก
├── create_database.py              # Script สร้างฐานข้อมูล
├── flowers_store.db                # ไฟล์ฐานข้อมูล SQLite
├── requirements.txt                # Dependencies
├── README.md                       # ไฟล์นี้
└── templates/
    ├── index.html                  # หน้าแรก (แสดงรายการทั้งหมด)
    ├── add_flower.html             # หน้าเพิ่มดอกไม้
    ├── edit_flower.html            # หน้าแก้ไขดอกไม้
    └── view_flower.html            # หน้าดูรายละเอียด
```

## 🗄️ โครงสร้างฐานข้อมูล

### ตาราง Categories (ตารางรอง)
| คอลัมน์ | ประเภทข้อมูล | รายละเอียด |
|--------|-----------|----------|
| `category_id` | INTEGER | รหัสหมวดหมู่ (Primary Key - Auto Increment) |
| `category_name` | TEXT | ชื่อหมวดหมู่ (UNIQUE) |

### ตาราง Flowers (ตารางหลัก)
| คอลัมน์ | ประเภทข้อมูล | ข้อจำกัด | รายละเอียด |
|--------|-----------|--------|----------|
| `flower_id` | INTEGER | PRIMARY KEY | รหัสดอกไม้ (Auto Increment) |
| `flower_name` | TEXT | NOT NULL | ชื่อดอกไม้ |
| `category_id` | INTEGER | FOREIGN KEY | เชื่อมโยงไปยัง Categories |
| `price` | REAL | CHECK(> 0), NOT NULL | ราคาดอกไม้เป็นบาท |
| `quantity` | INTEGER | CHECK(>= 0), NOT NULL | จำนวนดอกไม้ในคลัง |
| `description` | TEXT | - | รายละเอียดการนำเสนอสินค้า |

### ความสัมพันธ์ (Foreign Key Relationship)
```
Flowers.category_id → Categories.category_id
```
ทุกรายการดอกไม้จะต้องมีหมวดหมู่ที่มีอยู่ในตาราง Categories

## 🚀 วิธีการใช้งาน

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2. สร้างฐานข้อมูล (รันครั้งแรกเท่านั้น)
```bash
python create_database.py
```

### 3. รัน Flask Application
```bash
python app.py
```

### 4. เปิดเบราว์เซอร์ไปที่
```
http://localhost:5000
```

## 🔗 Routes (เส้นทาง API)

| Route | Method | ความหมาย |
|-------|--------|---------|
| `/` | GET | หน้าแรก - แสดงรายการดอกไม้ทั้งหมด |
| `/add-flower` | GET, POST | หน้าเพิ่มดอกไม้ใหม่ |
| `/edit-flower/<id>` | GET, POST | หน้าแก้ไขข้อมูลดอกไม้ |
| `/delete-flower/<id>` | POST | ลบรายการดอกไม้ |
| `/flower/<id>` | GET | ดูรายละเอียดดอกไม้ |
| `/api/flowers` | GET | API ดึงข้อมูลทั้งหมด (JSON) |

## 🎨 ฟีเจอร์ UI/UX

### Responsive Design
- ✅ รองรับทั้ง Desktop และ Mobile
- ✅ Tailwind CSS สำหรับการออกแบบสวยงาม
- ✅ Font Awesome Icons สำหรับสัญลักษณ์

### Interactive Elements
- ✅ Gradient Headers สำหรับห้องลักษณ์
- ✅ Hover Effects บนการ์ด
- ✅ Status Badges (มีสต็อก, ใกล้หมด, หมดแล้ว)
- ✅ Flash Messages สำหรับข้อความแจ้งเตือน
- ✅ Form Validation ด้านหน้า (Frontend)

### Validation
- ✅ ชื่อดอกไม้ต้องไม่ว่าง
- ✅ ราคาต้องมากกว่า 0
- ✅ จำนวนต้องมากกว่าหรือเท่ากับ 0
- ✅ Confirmation Dialog เมื่อลบรายการ

## 💾 ข้อมูลตัวอย่าง

ระบบมีข้อมูลตัวอย่าง 5 รายการ:

1. **กุหลาบแดง** - ฿50.00 - 25 ชอ - ดอกไม้สด
2. **แสนดอกเหม** - ฿35.00 - 15 ชอ - ดอกไม้สด
3. **ดอกเดซี่ประดิษฐ์** - ฿20.00 - 30 ชอ - ดอกไม้ประดิษฐ์
4. **ดอกไม้ตากแห้งรวมมิตร** - ฿15.00 - 50 ชอ - ดอกไม้ตากแห้ง
5. **กุหลาบขาว** - ฿45.00 - 20 ชอ - ดอกไม้สด

## 🛠️ เทคโนโลยีที่ใช้

- **Backend**: Flask (Python Web Framework)
- **Database**: SQLite
- **Frontend**: HTML 5, Tailwind CSS, JavaScript
- **Icons**: Font Awesome
- **Font**: Kanit (Google Fonts)

## 📝 หมายเหตุสำคัญ

1. **Secret Key**: ควรเปลี่ยน `app.secret_key` เป็นค่าที่ซับซ้อนและปลอดภัยในการใช้งานจริง
2. **Debug Mode**: ปิด Debug Mode เมื่อ Deploy ไปโปรดักชั่น
3. **Database**: ฐานข้อมูล SQLite เหมาะสำหรับแอปพลิเคชันเล็ก ถ้าต้องใช้ขนาดใหญ่ ให้ใช้ PostgreSQL หรือ MySQL
4. **Foreign Key**: จำเป็นต้องอยู่ในตาราง Categories ก่อน จึงจะสามารถเพิ่มลงตาราง Flowers ได้

## 🎓 วัตถุประสงค์การเรียนรู้

ระบบนี้ถูกออกแบบมาเพื่อสอนแนวคิด:
- ✅ CRUD Operations ด้วย Flask
- ✅ Database Design ด้วย SQLite
- ✅ Foreign Key Relationships
- ✅ Form Validation
- ✅ RESTful API Concepts
- ✅ Responsive Web Design ด้วย Tailwind CSS
- ✅ Template Rendering ด้วย Jinja2

## 📞 ติดต่อสำหรับการสนับสนุน

หากมีข้อสงสัยหรือพบปัญหา กรุณาติดต่อผู้พัฒนา

---

**สez**: ระบบจัดการร้านดอกไม้ 🌸 | **ปีการศึกษา**: 2026 | **ภาษา**: ไทย
