from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/")
@app.route("/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/author">author</a><br>
                <a href="/lab1/oak">oak</a><br>
                <a href="/lab1/counter">counter</a><br>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type':'text/plain; charset=utf-8'
        }

@app.route("/author")
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
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename = "oak.jpg")
    return """
<!doctype html>
<html>
    <body>
        <h1>Дуб</h1>
        <img src='""" + path + """'>
        <a href="/web">web</a>
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
        <a href="/web">web</a>
    </body>
</html>
'''

@app.route("/info")
def info():
    return redirect("/author")

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
    return "нет такой страницы", 404