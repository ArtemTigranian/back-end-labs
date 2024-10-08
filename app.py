from flask import Flask, url_for, redirect, render_template

# ЛАБОРАТОРНАЯ РАБОТА 1

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
                    <a href="/lab1">Меню</a>
                </main>
                <footer>
                    &copy; Артём Тигранян, ФБИ-21, 3 курс, 2024
                </footer>
            </body>
        </html>""", 200, {
            "X-Server": "sample",
            "Content-Type": "text/html; charset=utf-8"
         } 
        

@app.route("/lab1/author")
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

@app.route("/lab1/reset_counter")
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

resource_created = False

@app.route("/lab1/created")
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

@app.route("/lab1/delete")
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

# Родительская страница, показывающая статус ресурса
@app.route("/lab1/resource")
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


@app.route("/lab1/400")
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

@app.route("/lab1/401")
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

@app.route("/lab1/402")
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

@app.route("/lab1/403")
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

@app.route("/lab1/405")
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

@app.route("/lab1/418")
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

@app.route("/lab1/error")
def trigger_error():
    error = 1 / 0
    return

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


@app.route("/lab1/custom_route")
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


# ЛАБОРАТОРНАЯ РАБОТА 2

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return 'такого цветка нет', 404
    else:
        return f'''
<!doctype html>
<html>
    <body>
        <h1>Цветок: {flower_list[flower_id]}</h1>
        <p>Идентификатор цветка: {flower_id}</p>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a> |
        <a href="/lab2/clear_flowers">Очистить список цветов</a>
    </body>
</html>
'''

@app.route('/lab2/add_flower/')
@app.route('/lab2/add_flower/<name>')
def add_flower(name=None):
    if not name:
        return 'вы не задали имя цветка', 400
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name} </p>
        <p>Всего цветов: {len(flower_list)} </p>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a> |
        <a href="/lab2/flowers/0">Перейти к первому цветку</a>
    </body>
</html>
'''

@app.route('/lab2/all_flowers')
def all_flowers():
    flower_list_html = ''.join([f'<li>{flower}</li>' for flower in flower_list])
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Все цветы</h1>
        <p>Всего цветов: {len(flower_list)}</p>
        <ul>{flower_list_html}</ul>
        <a href="/lab2/clear_flowers">Очистить список цветов</a>
    </body>
</html>
'''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <body>
        <h1>Список цветов очищен</h1>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a>
    </body>
</html>
'''



@app.route('/lab2/example')
def example():
    name = 'Артём Тигранян'
    course = '3 курс'
    lab_number = 2
    group_number = 'ФБИ-21'
    fruits = [
        {'name': 'груши', 'price': 100},
        {'name': 'яблоки', 'price': 120},
        {'name': 'абрикосы', 'price': 92},
        {'name': 'сливы', 'price': 86},
        {'name': 'ананасы', 'price': 240},
        {'name': 'апельсины', 'price': 30},
    ]
    return render_template('example.html', 
                           name=name, course=course, lab_number=lab_number, 
                           group_number=group_number, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', phrase=phrase)