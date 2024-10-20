from flask import Flask, url_for
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

@app.route("/")
def start():
    css_path = url_for("static", filename="lab1.css")
    return """<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href='""" + css_path + """'>
            </head>
            <body>
                <header>
                    НГТУ, ФБ, Лабораторная 1
                </header>
                <main>
                    <h1>web-сервер на flask</h1>
                    <a href="/lab1">Меню Лабораторной 1</a>
                    <a href="/lab2">Меню Лабораторной 2</a>
                    <a href="/lab3">Меню Лабораторной 3</a>
                </main>
                <footer>
                    &copy; Артём Тигранян, ФБИ-21, 3 курс, 2024
                </footer>
            </body>
        </html>""" 


@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="trollface.jpg")
    return """
<!doctype html>
<html>
    <head>
        <title>Ошибка 404 - Страница не найдена</title>
        <link rel="stylesheet" type="text/css" href='""" + css_path + """'>
        <style>
            h1{
                text-align: center;
            }
            p{
                text-align: center;
            }
        </style>
    </head>
    <body>
        <main>
            <h1>ОШИБКА 404</h1>
            <p>НЕТ ТАКОЙ СТРАНИЦЫ</p>
            <img src='""" + img_path + """'>
            <p>Попробуйте вернуться <a href="/">на главную страницу</a>.</p>
        </main>    
    </body>
</html>""", 404


@app.errorhandler(500)
def internal_server_error(e):
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Ошибка 500: Внутренняя ошибка сервера</h1>
        <a href="/lab1">Вернуться на страницу лабораторной 1</a>
    </body>
</html>
    ''', 500