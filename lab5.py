from flask import Blueprint, url_for, redirect, render_template, request, make_response, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


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


@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error = 'Заполните все поля!')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else: 
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else: 
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
    
    db_close(conn, cur) 
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error = 'Заполните все поля!')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?", (login, ))
 
    user = cur.fetchone()

    if not user:
        db_close(conn, cur) 
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn,cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    # if user['password'] != password:
    #     db_close(conn, cur) 
    #     return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur) 
    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'  # Чекбокс: True, если выбран
    is_public = request.form.get('is_public') == 'on'      # Чекбокс: True, если выбран

    if not title or not article_text:
        return render_template('lab5/create_article.html', error="Заголовок и текст статьи не могут быть пустыми!")

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) 
            VALUES (%s, %s, %s, %s, %s);
        """, (user_id, title, article_text, is_favorite, is_public))
    else:
        cur.execute("""
            INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) 
            VALUES (?, ?, ?, ?, ?);
        """, (user_id, title, article_text, is_favorite, is_public))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    user_id = cur.fetchone()['id']

    # Извлекаем статьи, сортируя любимые статьи первыми
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT * FROM articles 
            WHERE user_id=%s 
            ORDER BY is_favorite DESC, id DESC;
        """, (user_id,))
    else:
        cur.execute("""
            SELECT * FROM articles 
            WHERE user_id=? 
            ORDER BY is_favorite DESC, id DESC;
        """, (user_id,))
    
    articles = cur.fetchall()

    db_close(conn, cur)

    if not articles:
        return render_template('lab5/articles.html', error="У вас пока нет ни одной статьи.")
    
    return render_template('lab5/articles.html', articles=articles)




@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    # Получаем статью для редактирования
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    
    article = cur.fetchone()

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = request.form.get('is_favorite') == 'on'  # Чекбокс: True, если выбран
        is_public = request.form.get('is_public') == 'on'      # Чекбокс: True, если выбран

        # Валидация: заголовок и текст не могут быть пустыми
        if not title.strip() or not article_text.strip():
            return render_template('lab5/edit_article.html', article=article, error="Заголовок и текст статьи не могут быть пустыми!")

        # Обновляем статью в базе данных
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE articles 
                SET title=%s, article_text=%s, is_favorite=%s, is_public=%s 
                WHERE id=%s;
            """, (title, article_text, is_favorite, is_public, article_id))
        else:
            cur.execute("""
                UPDATE articles 
                SET title=?, article_text=?, is_favorite=?, is_public=? 
                WHERE id=?;
            """, (title, article_text, is_favorite, is_public, article_id))
        
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    db_close(conn, cur)
    return render_template('lab5/edit_article.html', article=article)


@lab5.route('/lab5/delete/<int:article_id>', methods=['GET'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    # Проверяем, существует ли статья
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))

    # Удаляем статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/users')
def users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    # Получаем список всех пользователей (только логины)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users;")
    else:
        cur.execute("SELECT login FROM users;")
    
    users = cur.fetchall()

    db_close(conn, cur)

    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/public_articles')
def public_articles():
    conn, cur = db_connect()

    # Извлекаем все публичные статьи
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE is_public=True ORDER BY id DESC;")
    else:
        cur.execute("SELECT * FROM articles WHERE is_public=1 ORDER BY id DESC;")
    
    articles = cur.fetchall()

    db_close(conn, cur)

    if not articles:
        return render_template('/lab5/public_articles.html', error="Публичных статей пока нет.")
    
    return render_template('/lab5/public_articles.html', articles=articles)
