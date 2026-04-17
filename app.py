from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secretkey'
DB_NAME = 'product.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        image = request.form['image']

        if not name or not price or not quantity:
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('add_product'))

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, price, quantity, image) VALUES (?, ?, ?, ?)',
                       (name, price, quantity, image))
        conn.commit()
        conn.close()

        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        image = request.form['image']

        cursor.execute('''
            UPDATE products
            SET name=?, price=?, quantity=?, image=?
            WHERE id=?
        ''', (name, price, quantity, image, id))

        conn.commit()
        conn.close()

        flash('Product updated successfully!', 'success')
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM products WHERE id=?', (id,))
    product = cursor.fetchone()
    conn.close()

    return render_template('edit.html', product=product)

@app.route('/delete/<int:id>')
def delete_product(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id=?', (id,))
    conn.commit()
    conn.close()

    flash('Product deleted!', 'warning')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
