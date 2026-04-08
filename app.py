from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
from pathlib import Path
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-for-sessions'

# กำหนดพาธของฐานข้อมูล
DATABASE = Path(__file__).parent / "flowers_store.db"

def get_db_connection():
    """เชื่อมต่อกับฐานข้อมูล"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_categories():
    """ดึงรายการหมวดหมู่ทั้งหมด"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Categories ORDER BY category_id")
    categories = cursor.fetchall()
    conn.close()
    return categories

def get_flowers():
    """ดึงรายการดอกไม้ทั้งหมดพร้อมชื่อหมวดหมู่"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT f.flower_id, f.flower_name, c.category_name, f.price, 
               f.quantity, f.description, f.category_id
        FROM Flowers f
        INNER JOIN Categories c ON f.category_id = c.category_id
        ORDER BY f.flower_id
    ''')
    flowers = cursor.fetchall()
    conn.close()
    return flowers

def get_flower_by_id(flower_id):
    """ดึงข้อมูลดอกไม้ตามรหัส"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT f.flower_id, f.flower_name, c.category_name, f.price, 
               f.quantity, f.description, f.category_id
        FROM Flowers f
        INNER JOIN Categories c ON f.category_id = c.category_id
        WHERE f.flower_id = ?
    ''', (flower_id,))
    flower = cursor.fetchone()
    conn.close()
    return flower

# ===== ROUTES =====

@app.route('/')
def index():
    """หน้าแรกแสดงรายการดอกไม้ทั้งหมด"""
    flowers = get_flowers()
    return render_template('index.html', flowers=flowers)

@app.route('/api/flowers', methods=['GET'])
def api_get_flowers():
    """API ดึงรายการดอกไม้ (JSON)"""
    flowers = get_flowers()
    flowers_list = [
        {
            'flower_id': f['flower_id'],
            'flower_name': f['flower_name'],
            'category_name': f['category_name'],
            'price': f['price'],
            'quantity': f['quantity'],
            'description': f['description']
        }
        for f in flowers
    ]
    return jsonify(flowers_list)

@app.route('/add-flower', methods=['GET', 'POST'])
def add_flower():
    """เพิ่มดอกไม้ใหม่"""
    if request.method == 'POST':
        flower_name = request.form.get('flower_name')
        category_id = request.form.get('category_id')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        description = request.form.get('description')

        # ตรวจสอบข้อมูล
        if not flower_name or not category_id or not price or quantity is None:
            flash('❌ กรุณากรอกข้อมูลให้ครบถ้วน', 'error')
            return redirect(url_for('add_flower'))

        try:
            price = float(price)
            quantity = int(quantity)
            category_id = int(category_id)

            if price <= 0:
                flash('❌ ราคาต้องมากกว่า 0', 'error')
                return redirect(url_for('add_flower'))

            if quantity < 0:
                flash('❌ จำนวนต้องมากกว่าหรือเท่ากับ 0', 'error')
                return redirect(url_for('add_flower'))

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Flowers (flower_name, category_id, price, quantity, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (flower_name, category_id, price, quantity, description))
            conn.commit()
            conn.close()

            flash('✅ เพิ่มดอกไม้สำเร็จ!', 'success')
            return redirect(url_for('index'))

        except ValueError:
            flash('❌ ข้อมูลไม่ถูกต้อง (ราคาและจำนวนต้องเป็นตัวเลข)', 'error')
            return redirect(url_for('add_flower'))

    categories = get_categories()
    return render_template('add_flower.html', categories=categories)

@app.route('/edit-flower/<int:flower_id>', methods=['GET', 'POST'])
def edit_flower(flower_id):
    """แก้ไขข้อมูลดอกไม้"""
    flower = get_flower_by_id(flower_id)
    
    if not flower:
        flash('❌ ไม่พบดอกไม้นี้', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        flower_name = request.form.get('flower_name')
        category_id = request.form.get('category_id')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        description = request.form.get('description')

        if not flower_name or not category_id or not price or quantity is None:
            flash('❌ กรุณากรอกข้อมูลให้ครบถ้วน', 'error')
            return redirect(url_for('edit_flower', flower_id=flower_id))

        try:
            price = float(price)
            quantity = int(quantity)
            category_id = int(category_id)

            if price <= 0:
                flash('❌ ราคาต้องมากกว่า 0', 'error')
                return redirect(url_for('edit_flower', flower_id=flower_id))

            if quantity < 0:
                flash('❌ จำนวนต้องมากกว่าหรือเท่ากับ 0', 'error')
                return redirect(url_for('edit_flower', flower_id=flower_id))

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Flowers
                SET flower_name = ?, category_id = ?, price = ?, quantity = ?, description = ?
                WHERE flower_id = ?
            ''', (flower_name, category_id, price, quantity, description, flower_id))
            conn.commit()
            conn.close()

            flash('✅ แก้ไขดอกไม้สำเร็จ!', 'success')
            return redirect(url_for('index'))

        except ValueError:
            flash('❌ ข้อมูลไม่ถูกต้อง (ราคาและจำนวนต้องเป็นตัวเลข)', 'error')
            return redirect(url_for('edit_flower', flower_id=flower_id))

    categories = get_categories()
    return render_template('edit_flower.html', flower=flower, categories=categories)

@app.route('/delete-flower/<int:flower_id>', methods=['POST'])
def delete_flower(flower_id):
    """ลบดอกไม้"""
    flower = get_flower_by_id(flower_id)
    
    if not flower:
        flash('❌ ไม่พบดอกไม้นี้', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Flowers WHERE flower_id = ?', (flower_id,))
    conn.commit()
    conn.close()

    flash('✅ ลบดอกไม้สำเร็จ!', 'success')
    return redirect(url_for('index'))

@app.route('/flower/<int:flower_id>')
def view_flower(flower_id):
    """ดูรายละเอียดดอกไม้"""
    flower = get_flower_by_id(flower_id)
    
    if not flower:
        flash('❌ ไม่พบดอกไม้นี้', 'error')
        return redirect(url_for('index'))

    return render_template('view_flower.html', flower=flower)

# ===== CATEGORY ROUTES =====

@app.route('/categories')
def categories():
    """แสดงรายการหมวดหมู่ทั้งหมด"""
    categories = get_categories()
    return render_template('categories.html', categories=categories)

@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    """เพิ่มหมวดหมู่ใหม่"""
    if request.method == 'POST':
        category_name = request.form.get('category_name')

        if not category_name or category_name.strip() == '':
            flash('❌ กรุณากรอกชื่อหมวดหมู่', 'error')
            return redirect(url_for('add_category'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # ตรวจสอบว่ามีหมวดหมู่นี้อยู่แล้วหรือไม่
            cursor.execute("SELECT * FROM Categories WHERE category_name = ?", (category_name,))
            if cursor.fetchone():
                flash('❌ หมวดหมู่นี้มีอยู่แล้ว', 'error')
                conn.close()
                return redirect(url_for('add_category'))
            
            cursor.execute('INSERT INTO Categories (category_name) VALUES (?)', (category_name,))
            conn.commit()
            conn.close()

            flash(f'✅ เพิ่มหมวดหมู่ "{category_name}" สำเร็จ!', 'success')
            return redirect(url_for('categories'))

        except Exception as e:
            flash(f'❌ เกิดข้อผิดพลาด: {str(e)}', 'error')
            return redirect(url_for('add_category'))

    return render_template('add_category.html')

@app.route('/edit-category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    """แก้ไขหมวดหมู่"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Categories WHERE category_id = ?', (category_id,))
    category = cursor.fetchone()
    conn.close()

    if not category:
        flash('❌ ไม่พบหมวดหมู่นี้', 'error')
        return redirect(url_for('categories'))

    if request.method == 'POST':
        category_name = request.form.get('category_name')

        if not category_name or category_name.strip() == '':
            flash('❌ กรุณากรอกชื่อหมวดหมู่', 'error')
            return redirect(url_for('edit_category', category_id=category_id))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # ตรวจสอบว่ามีหมวดหมู่นี้อยู่แล้วหรือไม่ (ยกเว้นตัวมันเอง)
            cursor.execute("SELECT * FROM Categories WHERE category_name = ? AND category_id != ?", 
                         (category_name, category_id))
            if cursor.fetchone():
                flash('❌ หมวดหมู่นี้มีอยู่แล้ว', 'error')
                conn.close()
                return redirect(url_for('edit_category', category_id=category_id))
            
            cursor.execute('UPDATE Categories SET category_name = ? WHERE category_id = ?', 
                         (category_name, category_id))
            conn.commit()
            conn.close()

            flash(f'✅ แก้ไขหมวดหมู่สำเร็จ!', 'success')
            return redirect(url_for('categories'))

        except Exception as e:
            flash(f'❌ เกิดข้อผิดพลาด: {str(e)}', 'error')
            return redirect(url_for('edit_category', category_id=category_id))

    return render_template('edit_category.html', category=category)

@app.route('/delete-category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    """ลบหมวดหมู่"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # ตรวจสอบว่ามีดอกไม้ในหมวดหมู่นี้หรือไม่
    cursor.execute('SELECT COUNT(*) FROM Flowers WHERE category_id = ?', (category_id,))
    flower_count = cursor.fetchone()[0]
    
    if flower_count > 0:
        flash(f'❌ ไม่สามารถลบได้ มีดอกไม้ {flower_count} รายการในหมวดหมู่นี้', 'error')
        conn.close()
        return redirect(url_for('categories'))

    try:
        cursor.execute('DELETE FROM Categories WHERE category_id = ?', (category_id,))
        conn.commit()
        conn.close()
        flash('✅ ลบหมวดหมู่สำเร็จ!', 'success')
    except Exception as e:
        flash(f'❌ เกิดข้อผิดพลาด: {str(e)}', 'error')

    return redirect(url_for('categories'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
