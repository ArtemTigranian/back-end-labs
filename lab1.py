from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
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
                    <a href="/lab1">Меню Лабораторной 1</a>
                    <a href="/lab2">Меню Лабораторной 2</a>
                </main>
                <footer>
                    &copy; Артём Тигранян, ФБИ-21, 3 курс, 2024
                </footer>
            </body>
        </html>""", 200, {
            "X-Server": "sample",
            "Content-Type": "text/html; charset=utf-8"
         } 
        

@lab1.route("/lab1/author")
def author():
    css_path = url_for("static", filename="lab1.css")
    name = "Тигранян Артём Паруйрович"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href='""" + css_path + """'>
            </head>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""


@lab1.route("/lab1/oak")
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

@lab1.route("/lab1/counter")
def counter():
    css_path = url_for("static", filename="lab1.css")
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + ''' <br>
        <a href="/lab1/reset_counter">Очистить счётчик</a><br>
        <a href="/lab1/web">web</a>
    </body>
</html>
'''


@lab1.route("/lab1/reset_counter")
def reset_counter():
    css_path = url_for("static", filename="lab1.css")
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        Счётчик обнулён!<br>
        <a href="/lab1/counter">Вернуться к счётчику</a><br>
        <a href="/lab1/web">web</a>
    </body>
</html>
'''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


resource_created = False


@lab1.route("/lab1/created")
def create_resource():
    css_path = url_for("static", filename="lab1.css")
    global resource_created
    if not resource_created:
        resource_created = True
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Успешно: ресурс создан</h1>
        <p>Ваш ресурс был успешно создан.</p>
        <a href="/lab1/resource">Вернуться к статусу ресурса</a>
    </body>
</html>
''', 201
    else:
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Отказано: ресурс уже создан</h1>
        <p>Вы не можете создать ресурс, так как он уже существует.</p>
        <a href="/lab1/resource">Вернуться к статусу ресурса</a>
    </body>
</html>
''', 400


@lab1.route("/lab1/delete")
def delete_resource():
    css_path = url_for("static", filename="lab1.css")
    global resource_created
    if resource_created:
        resource_created = False
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Успешно: ресурс удалён</h1>
        <p>Ваш ресурс был успешно удалён.</p>
        <a href="/lab1/resource">Вернуться к статусу ресурса</a>
    </body>
</html>
''', 200
    else:
        return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Отказано: ресурс отсутствует</h1>
        <p>Вы не можете удалить ресурс, так как он ещё не был создан или уже был удалён.</p>
        <a href="/lab1/resource">Вернуться к статусу ресурса</a>
    </body>
</html>
''', 400


@lab1.route("/lab1/resource")
def resource_status():
    css_path = url_for("static", filename="lab1.css")
    global resource_created
    status = "Ресурс создан" if resource_created else "Ресурс ещё не создан"
    create_link = url_for('create_resource')
    delete_link = url_for('delete_resource')
    
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href={css_path}>
    </head>
    <body>
        <h1>Статус ресурса</h1>
        <p>{status}</p>
        <a href="{create_link}">Создать ресурс</a><br>
        <a href="{delete_link}">Удалить ресурс</a>
    </body>
</html>
    '''


@lab1.route("/lab1")
def lab():
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
                    <li><a href="/lab1/resource">RESOURCE</a></li>
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


@lab1.route("/lab1/400")
def error_400():
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>400: Bad Request</h1>
        <p>Ошибка 400: Сервер не может обработать запрос из-за ошибки клиента.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 400


@lab1.route("/lab1/401")
def error_401():
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>401: Unauthorized</h1>
        <p>Ошибка 401: Необходима аутентификация для доступа к ресурсу.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 401


@lab1.route("/lab1/402")
def error_402():
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>402: Payment Required</h1>
        <p>Ошибка 402: Требуется оплата для доступа к ресурсу.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 402


@lab1.route("/lab1/403")
def error_403():
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>403: Forbidden</h1>
        <p>Ошибка 403: Доступ к ресурсу запрещен.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 403


@lab1.route("/lab1/405")
def error_405():
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>405: Method Not Allowed</h1>
        <p>Ошибка 405: Метод запроса не поддерживается данным ресурсом.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 405


@lab1.route("/lab1/418")
def error_418():
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>418: I'm a teapot</h1>
        <p>Ошибка 418: Я чайник. Запрос не может быть обработан, так как сервер — это чайник.</p>
        <a href="/lab1">На страницу лабораторной 1</a>
    </body>
</html>
    ''', 418


@lab1.route("/lab1/error")
def trigger_error():
    error = 1 / 0
    return


@lab1.route("/lab1/custom_route")
def custom_route():
    css_path = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="oak.jpg")
    return """
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href='""" + css_path + """'>
        <title>Текст с картинкой</title>
    </head>
    <body>
        <h1>Добро пожаловать на страницу с текстом и изображением</h1>
        <p>Равным образом постоянный количественный рост и сфера нашей активности играет важную роль в формировании новых предложений. 
        Не следует, однако забывать, что дальнейшее развитие различных форм деятельности позволяет оценить значение новых предложений. 
        С другой стороны начало повседневной работы по формированию позиции требуют от нас анализа системы обучения кадров, соответствует 
        насущным потребностям. Равным образом постоянный количественный рост и сфера нашей активности играет важную роль в формировании 
        направлений прогрессивного развития.</p>
        <p>Задача организации, в особенности же сложившаяся структура организации требуют от нас анализа систем массового участия. 
        Идейные соображения высшего порядка, а также постоянное информационно-пропагандистское обеспечение нашей деятельности обеспечивает 
        широкому кругу (специалистов) участие в формировании дальнейших направлений развития.</p>
        <p>Идейные соображения высшего порядка, а также рамки и место обучения кадров влечет за собой процесс внедрения и модернизации 
        соответствующий условий активизации. Значимость этих проблем настолько очевидна, что новая модель организационной деятельности 
        требуют определения и уточнения модели развития. Повседневная практика показывает, что консультация с широким активом представляет 
        собой интересный эксперимент проверки форм развития.</p>
        <img src='""" + img_path + """' style="width:400px;height:auto;">
    </body>
</html>
""",{
        "Content-Language": "ru",
        "Content-Type": "text/html; charset=utf-8",
        "X-Server": "sample"
    }