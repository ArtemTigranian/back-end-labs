from flask import Blueprint, url_for, redirect, render_template, request, make_response, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


films = [
    {
        "title": "Inglourious Basterds",
        "title_ru": "Бесславные ублюдки",
        "year": 2009,
        "description": "Вторая мировая война. В оккупированной немцами Франции группа американских солдат-евреев наводит страх на нацистов, жестоко убивая и скальпируя солдат."
    },
    {
        "title": "Django Unchained",
        "title_ru": "Джанго освобожденный",
        "year": 2012,
        "description": "Шульц — эксцентричный охотник за головами, который выслеживает и отстреливает самых опасных преступников. Он освобождает раба по имени Джанго, поскольку тот может помочь ему в поисках трёх бандитов. Джанго знает этих парней в лицо, ведь у него с ними свои счёты."
    },
    {
        "title": "Kill Bill: Vol. 1",
        "title_ru": "Убить Билла",
        "year": 2003,
        "description": "В беременную наёмную убийцу по кличке Чёрная Мамба во время бракосочетания стреляет человек по имени Билл. Но голова у женщины оказалась крепкой — пролежав четыре года в коме, бывшая невеста приходит в себя. Она горит желанием найти предателей. Теперь только безжалостная месть успокоит сердце Чёрной Мамбы, и она начинает по очереди убивать членов банды Билла, решив оставить главаря напоследок."
    },
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if 0 <= id < len(films):
        return films[id]
    else:
        return "Нет фильма под таким индексом", 404


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def del_films():
    if 0 <= id < len(films):
        del films[id]
        return '', 204
    else:
        return "Нет фильма под таким индексом", 404