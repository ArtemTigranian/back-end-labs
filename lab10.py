from flask import Blueprint, url_for, redirect, render_template, request, make_response, session, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab10 = Blueprint('lab10', __name__)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'artem_tigranian_knowledge_base',
            user = 'artem_tigranian_knowledge_base',
            password = 'artem'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)

    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab10.route('/lab10/')
def lab():
    return render_template('lab10/index.html', login=session.get('login'))


@lab10.route('/lab10/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab10/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab10/register.html', error = 'Заполните все поля!')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else: 
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab10/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else: 
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
    
    db_close(conn, cur) 
    return render_template('lab10/success.html', login=login)


@lab10.route('/lab10/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab10/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab10/register.html', error = 'Заполните все поля!')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?", (login, ))
 
    user = cur.fetchone()

    if not user:
        db_close(conn, cur) 
        return render_template('lab10/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn,cur)
        return render_template('lab10/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur) 
    return render_template('lab10/index.html', login=login)


@lab10.route('/lab10/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab10')


@lab10.route('/lab10/katalog')
def katalog():
    conn, cur = db_connect()
    cur.execute("SELECT id, title, description, price FROM products")
    products = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab10/katalog.html', products=products)


@lab10.route('/lab10/cart', methods=['GET'])
def view_cart():
    if 'login' not in session:
        return render_template('lab10/katalog.html', error='Пожалуйста, войдите в систему для добавления товаров в корзину.')

    # Получаем корзину из сессии
    cart = session.get('cart', [])

    total_amount = sum(float(item['price']) * int(item['quantity']) for item in cart)
    
    return render_template('lab10/cart.html', cart_items=cart, total_amount=total_amount)


@lab10.route('/lab10/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'login' not in session:
        return render_template('lab10/katalog.html', error='Для добавления в корзину необходимо войти в систему.')

    product_id = request.form.get('product_id')
    product_title = request.form.get('product_title')
    product_price = request.form.get('product_price')

    # Проверяем, есть ли уже этот товар в корзине
    cart = session.get('cart', [])
    existing_product = next((item for item in cart if item['id'] == product_id), None)

    if existing_product:
        existing_product['quantity'] += 1  # Увеличиваем количество товара
    else:
        cart.append({'id': product_id, 'title': product_title, 'price': product_price, 'quantity': 1})

    session['cart'] = cart  # Сохраняем корзину обратно в сессию

    return redirect('/lab10/katalog')


@lab10.route('/lab10/update_cart', methods=['POST'])
def update_cart():
    if 'login' not in session:
        return render_template('lab10/katalog.html', error='Для изменения количества товара необходимо войти в систему.')

    # Получаем id товара и новое количество
    product_id = request.form.get('product_id')
    new_quantity = int(request.form.get('quantity'))  # Преобразуем quantity в целое число

    # Получаем корзину из сессии
    cart = session.get('cart', [])

    # Ищем товар в корзине и обновляем его количество
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = new_quantity
            break

    # Сохраняем обновленную корзину в сессии
    session['cart'] = cart

    # Перенаправляем обратно на страницу корзины
    return redirect('/lab10/cart')



@lab10.route('/lab10/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'login' not in session:
        return render_template('lab10/katalog.html', error='Для удаления товара из корзины необходимо войти в систему.')

    # Получаем id товара, который нужно удалить
    product_id = request.form.get('product_id')

    # Получаем корзину из сессии
    cart = session.get('cart', [])

    # Фильтруем корзину, чтобы удалить товар с указанным id
    cart = [item for item in cart if item['id'] != product_id]

    # Сохраняем обновленную корзину в сессии
    session['cart'] = cart

    return redirect('/lab10/cart')


@lab10.route('/lab10/checkout', methods=['POST'])
def checkout():
    if 'login' not in session:
        return render_template('lab10/katalog.html', error='Для оформления покупки необходимо войти в систему.')

    # Получаем корзину из сессии
    cart = session.get('cart', [])

    if not cart:
        return render_template('lab10/cart.html', error="Ваша корзина пуста.")

    # Рассчитываем общую сумму
    total_amount = sum(float(item['price']) * item['quantity'] for item in cart)

    # Очищаем корзину после оформления
    session.pop('cart', None)

    # Перенаправляем на страницу с поздравлением
    return render_template('lab10/thank_you.html', total_amount=total_amount)