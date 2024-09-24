from flask import Flask, url_for, redirect, make_response
app = Flask(__name__)

@app.route("/")
@app.route("/lab1/web")
def web():
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
                    <a href="/lab1/author">author</a><br>
                    <a href="/lab1/oak">oak</a><br>
                    <a href="/lab1/counter">counter</a><br>
                </main>
                <footer>
                    &copy; Артём Тигранян, ФБИ-21, 3 курс, 2024
                </footer>
            </body>
        </html>""", 200

@app.route("/lab1/author")
def author():
    name = "Тигранян Артём Паруйрович"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/oak")
def oak():
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename = "oak.jpg")
    return """
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href='""" + css_path + """'>
    </head>
    <body>
        <h1>Дуб</h1>
        <img src='""" + img_path + """'>
        <a href="/lab1/web">web</a>
    </body>
</html>
"""


count = 0

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + ''' <br>
        <a href="/lab1/reset_counter">Очистить счётчик</a><br>
        <a href="/lab1/web">web</a>
    </body>
</html>
'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        Счётчик обнулён!<br>
        <a href="/lab1/counter">Вернуться к счётчику</a><br>
        <a href="/lab1/web">web</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

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

@app.route("/lab1")
def lab1():
    css_path = url_for("static", filename="lab1.css")
    return """
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href='""" + css_path + """'>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <header>
        </header>
        <main>
            <p>
                Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
                Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
            </p>
            <a href="/">На главную</a>
            <h2>Список роутов</h2>
            <div class="menu">
                <ol>
                    <li><a href="/lab1/web">WEB</a></li>
                    <li><a href="/lab1/author">AUTHOR</a></li>
                    <li><a href="/lab1/oak">OAK</a></li>
                    <li><a href="/lab1/counter">COUNTER</a></li>
                    <li><a href="/lab1/reset_counter">RESET_COUNTER</a></li>
                    <li><a href="/lab1/info">INFO</a></li>
                    <li><a href="/lab1/created">CREATED</a></li>
                    <li><a href="/lab1/400">400</a></li>
                    <li><a href="/lab1/401">401</a></li>
                    <li><a href="/lab1/402">402</a></li>
                    <li><a href="/lab1/403">403</a></li>
                    <li><a href="/lab1/405">405</a></li>
                    <li><a href="/lab1/418">418</a></li>
                    <li><a href="/lab1/error">error</a></li>
                    <li><a href="/lab1/custom_route">custom_route</a></li>
                </ol>
            </div>
        <main>    
        <footer>
        </footer>
    </body>
</html>
    """


@app.route("/lab1/400")
def error_400():
    return '''
<!doctype html>
<html>
    <body>
        <h1>400: Bad Request</h1>
        <p>Ошибка 400: Сервер не может обработать запрос из-за ошибки клиента.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 400

@app.route("/lab1/401")
def error_401():
    return '''
<!doctype html>
<html>
    <body>
        <h1>401: Unauthorized</h1>
        <p>Ошибка 401: Необходима аутентификация для доступа к ресурсу.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 401

@app.route("/lab1/402")
def error_402():
    return '''
<!doctype html>
<html>
    <body>
        <h1>402: Payment Required</h1>
        <p>Ошибка 402: Требуется оплата для доступа к ресурсу.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 402

@app.route("/lab1/403")
def error_403():
    return '''
<!doctype html>
<html>
    <body>
        <h1>403: Forbidden</h1>
        <p>Ошибка 403: Доступ к ресурсу запрещен.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 403

@app.route("/lab1/405")
def error_405():
    return '''
<!doctype html>
<html>
    <body>
        <h1>405: Method Not Allowed</h1>
        <p>Ошибка 405: Метод запроса не поддерживается данным ресурсом.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 405

@app.route("/lab1/418")
def error_418():
    return '''
<!doctype html>
<html>
    <body>
        <h1>418: I'm a teapot</h1>
        <p>Ошибка 418: Я чайник. Запрос не может быть обработан, так как сервер — это чайник.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 418

@app.route("/lab1/error")
def trigger_error():
    error = 1 / 0
    return

@app.errorhandler(500)
def internal_server_error(e):
    return '''
<!doctype html>
<html>
    <body>
        <h1>Ошибка 500: Внутренняя ошибка сервера</h1>
        <a href="/lab1">Вернуться на страницу лабораторной 1</a>
    </body>
</html>
    ''', 500


@app.route("/lab1/custom_route")
def custom_route():
    # Подготовка HTML содержимого
    img_path = url_for("static", filename="oak.jpg")
    content = """
<!doctype html>
<html>
    <head>
        <title>Текст с картинкой</title>
    </head>
    <body>
        <h1>Добро пожаловать на страницу с текстом и изображением</h1>
        <p>Это первый абзац текста. Здесь может быть ваше описание или история. Flask — это мощный фреймворк для создания веб-приложений.</p>
        <p>Во втором абзаце рассказывается о возможностях Flask, таких как маршрутизация, обработка шаблонов и управление данными с помощью различных библиотек.</p>
        <p>Третий абзац посвящен тому, как легко интегрировать CSS и JavaScript в страницы Flask для улучшения пользовательского интерфейса.</p>
        <p>Здесь можно размещать изображения и другие мультимедиа:</p>
        <img src='""" + img_path + """' alt="Пример изображения" style="width:400px;height:auto;">
    </body>
</html>
    """
    
    # Создание ответа с содержимым
    response = make_response(content)

    # Добавление заголовка Content-Language
    response.headers["Content-Language"] = "ru"  # Указываем, что страница на русском языке

    # Добавление двух нестандартных заголовков
    response.headers["X-Custom-Header"] = "StudentProject"
    response.headers["X-Page-Info"] = "CustomRouteWithImage"

    return response
