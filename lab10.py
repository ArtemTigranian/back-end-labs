from flask import Blueprint, url_for, redirect, render_template, request, make_response, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
lab10 = Blueprint('lab10', __name__)

# Функции для работы с базой данных
def db_connect():
    """Подключение к базе данных (PostgreSQL или SQLite)"""
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='artem_tigranian_knowledge_base',
            user='artem_tigranian_knowledge_base',
            password='artem'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    """Закрытие соединения с базой данных"""
    conn.commit()
    cur.close()
    conn.close()

# Статичные данные для каталога товаров (вместо базы данных для простоты)
products = [
    {"id": 1, "title": "Стул", "description": "Удобный стул для офиса", "price": 1000},
    {"id": 2, "title": "Стол", "description": "Стол для рабочего места", "price": 2000},
    {"id": 3, "title": "Диван", "description": "Мягкий диван для дома", "price": 5000},
    {"id": 4, "title": "Шкаф", "description": "Шкаф для одежды", "price": 3000}
]

cart = []  # Корзина покупок (будет храниться в сессии)

# Роуты для работы с продуктами и корзиной

@lab10.route('/lab10/')
def lab():
    return render_template('lab10/index.html', login=session.get('login'))


@lab10.route('/lab10/json-rpc-api/', methods=['POST'])
def api():
    """API JSON-RPC для работы с товарами и корзиной"""
    data = request.json
    id = data['id']

    # Получение каталога товаров
    if data['method'] == 'get_catalog':
        return {
            'jsonrpc': '2.0',
            'result': products,
            'id': id
        }

    # Проверка авторизации пользователя
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    # Добавление товара в корзину
    if data['method'] == 'add_to_cart':
        product_id = data['params']
        for product in products:
            if product['id'] == product_id:
                # Добавляем товар в корзину
                cart.append(product)
                return {
                    'jsonrpc': '2.0',
                    'result': f'Товар {product_id} добавлен в корзину.',
                    'id': id
                }
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 2,
                'message': 'Product not found'
            },
            'id': id
        }

    # Удаление товара из корзины
    if data['method'] == 'remove_from_cart':
        product_id = data['params']
        global cart
        cart = [item for item in cart if item['id'] != product_id]  # Удаляем товар с данным ID из корзины
        return {
            'jsonrpc': '2.0',
            'result': f'Товар {product_id} удален из корзины.',
            'id': id
        }

    # Получение товаров из корзины
    if data['method'] == 'get_cart':
        return {
            'jsonrpc': '2.0',
            'result': cart,
            'id': id
        }

    # Оформление покупки
    if data['method'] == 'checkout':
        total_price = sum(item['price'] for item in cart)
        cart.clear()  # Очищаем корзину после оформления
        return {
            'jsonrpc': '2.0',
            'result': f'Checkout successful. Total: {total_price} руб.',
            'id': id
        }

    # Если метод не найден
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }


@lab10.route('/lab10/register', methods=['GET', 'POST'])
def register():
    """Регистрация нового пользователя"""
    if request.method == 'GET':
        return render_template('lab10/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab10/register.html', error='Заполните все поля!')
    
    conn, cur = db_connect()
    cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab10/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    db_close(conn, cur) 
    return render_template('lab10/success.html', login=login)


@lab10.route('/lab10/login', methods=['GET', 'POST'])
def login():
    """Авторизация пользователя"""
    if request.method == 'GET':
        return render_template('lab10/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab10/login.html', error='Заполните все поля!')

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users WHERE login=%s", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur) 
        return render_template('lab10/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab10/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur) 
    return redirect('/lab10')


@lab10.route('/lab10/logout')
def logout():
    """Выход из системы"""
    session.pop('login', None)
    return redirect('/lab10')


@lab10.route('/lab10/katalog')
def katalog():
    # Получаем товары из базы данных
    conn, cur = db_connect()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab10/lab10.html', products=products, login=session.get('login'))


@lab10.route('/lab10/cart')
def cart():
    # Логика для отображения корзины
    # Например, получаем товары из корзины из сессии:
    cart_items = session.get('cart', [])
    return render_template('lab10/cart.html', cart_items=cart_items)
