from flask import Blueprint, url_for, redirect, render_template, request, make_response, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Логин не должен быть пустым')

    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)

    return redirect('/lab8/')


@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = 'remember_me' in request.form  #запомнить меня

    if not login_form:
        return render_template('lab8/login.html', error='Логин не должен быть пустым')

    if not password_form:
        return render_template('lab8/login.html', error='Пароль не должен быть пустым')

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            # запомнить меня
            login_user(user, remember=remember_me)
            return redirect('/lab8/')
    
    return render_template('lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/logout/')
@login_required
def logout():
    session.pop('login', None)
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = 'is_favorite' in request.form  # если галочка "Избранное" установлена
        is_public = 'is_public' in request.form  # если галочка "Публичная" установлена

        # Проверка на пустые поля
        if not title:
            return render_template('lab8/create_article.html', error='Заголовок не должен быть пустым')

        if not article_text:
            return render_template('lab8/create_article.html', error='Текст статьи не должен быть пустым')

        # Создание нового объекта статьи
        new_article = articles(
            title=title,
            article_text=article_text,
            is_favorite=is_favorite,
            is_public=is_public,
            likes=0,  # Начальное количество лайков
            login_id=current_user.id  # связываем статью с текущим пользователем
        )
        # Сохранение в базу данных
        db.session.add(new_article)
        db.session.commit()

        # Перенаправление на страницу со списком статей
        return redirect('/lab8/articles/')

    # Если запрос GET, просто показываем форму
    return render_template('lab8/create_article.html')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    articly = articles.query.filter_by(login_id=current_user.id).all()  # Показываем статьи только текущего пользователя
    return render_template('lab8/article_list.html', articly=articly)


@lab8.route('/lab8/articles/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    # Проверка, что текущий пользователь является владельцем статьи
    if article.login_id != current_user.id:
        return redirect('/lab8/articles/')

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = 'is_favorite' in request.form
        is_public = 'is_public' in request.form

        # Проверка на пустые поля
        if not title:
            return render_template('lab8/edit_article.html', article=article, error='Заголовок не должен быть пустым')

        if not article_text:
            return render_template('lab8/edit_article.html', article=article, error='Текст статьи не должен быть пустым')

        # Обновление статьи
        article.title = title
        article.article_text = article_text
        article.is_favorite = is_favorite
        article.is_public = is_public

        db.session.commit()

        # Перенаправление на страницу со списком статей
        return redirect('/lab8/articles/')

    return render_template('lab8/edit_article.html', article=article)

@lab8.route('/lab8/articles/delete/<int:article_id>/', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    # Проверка, что текущий пользователь является владельцем статьи
    if article.login_id != current_user.id:
        return redirect('/lab8/articles/')

    # Удаление статьи
    db.session.delete(article)
    db.session.commit()

    # Перенаправление на страницу со списком статей
    return redirect('/lab8/articles/')


