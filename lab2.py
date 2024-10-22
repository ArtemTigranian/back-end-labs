from flask import Blueprint, url_for, redirect, request, render_template
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/')    
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = [
    {"name": "роза", "price": 300},
    {"name": "тюльпан", "price": 310},
    {"name": "незабудка", "price": 320},
    {"name": "ромашка", "price": 330},
    {"name": "георгин", "price": 300},
    {"name": "гладиолус", "price": 310}
]


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return 'такого цветка нет', 404
    else:
        flower = flower_list[flower_id]
        return render_template('lab2/flower.html', flower_list=flower_list, flower=flower, flower_id=flower_id)


@lab2.route('/lab2/all_flowers')
def all_flowers():
    return render_template('lab2/all_flowers.html', flowers=flower_list, flower_count=len(flower_list))


@lab2.route('/lab2/add_flower', methods=['post'])
def add_flower():
    name = request.form['name']
    price = request.form['price']
    if not name or not price:
        return "Вы не ввели имя или цену"
    new_flower = {"name": name, "price": price}
    flower_list.lab2end(new_flower)
    return redirect('/lab2/all_flowers')


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return render_template('lab2/clear_flowers.html')


@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        return 'Такого цветка нет', 404
    else:
        del flower_list[flower_id]
        return redirect('/lab2/all_flowers')


@lab2.route('/lab2/example')
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
    return render_template('lab2/example.html', 
                           name=name, course=course, lab_number=lab_number, 
                           group_number=group_number, fruits=fruits)


@lab2.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    slozh = a + b
    vych = a - b
    umnozh = a * b
    delen = a / b if b != 0 else 'ДЕЛИТЬ НА 0 НЕЛЬЗЯ'  
    stepen = a ** b
    return  render_template('lab2/calc.html', slozh=slozh, vych=vych, umnozh=umnozh, delen=delen, stepen=stepen, a=a, b=b)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def calc_with_one(a):
    return redirect(url_for('calc', a=a, b=1))


books = [
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Роман в стихах", "pages": 224},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Роман", "pages": 512},
    {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 315},
    {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Поэма", "pages": 352},
    {"author": "Антон Чехов", "title": "Чайка", "genre": "Пьеса", "pages": 96},
    {"author": "Максим Горький", "title": "На дне", "genre": "Пьеса", "pages": 123},
    {"author": "Владимир Набоков", "title": "Лолита", "genre": "Роман", "pages": 336},
    {"author": "Илья Ильф и Евгений Петров", "title": "Двенадцать стульев", "genre": "Комедия", "pages": 416},
]


@lab2.route('/lab2/books')
def books_list():
    return render_template('lab2/books.html', books=books)


kings = [
    {
        "name": "Арташес I - Արտաշես",
        "description": "Один из величайших древних армянских царей. Правил еще в 189-160 годах до нашей эры. Известен как знаменитый реформатор, собиратель армянских земель в Мец Хайк - Великую Армению.",
        "image": "/static/lab2/artashes.png"
    },
    {
        "name": "Тигран II Великий - Տիգրան",
        "description": "Величайший правитель в армянской истории. Царь Великой Армении из династии Арташесидов, чьи владения в I веке до нашей эры простирались от Каспия до Иерусалима.",
        "image": "/static/lab2/tigran.png"
    },
    {
        "name": "Трдат III - Տրդատ Գ Մեծ",
        "description": "Армянский царь из династии Аршакидов, правивший в IV веке нашей эры. Именно в эпоху Трдата произошло величайшее событие мировой важности - армяне первыми в истории приняли христианскую веру. А сам он вошел в историю как государь-креститель нации.",
        "image": "/static/lab2/trdat.png"
    },
    {
        "name": "Царь Пап - Պապ",
        "description": "Правивший в конце IV века нашей эры армянский царь из династии Аршакидов. Вошел в историю как умный и отважный царь, реформатор церкви, победитель персов в битве у Багавана. Увы, пал жертвой подлости римлян...",
        "image": "/static/lab2/pap.png"
    },
    {
        "name": "Ашот II Еркат (Железный) - Աշոտ Բ Երկաթ",
        "description": "Этот великий царь из династии Багратуни правил в IX веке нашей эры. Именно Ашот Еркат в битве на Севане разбил арабов, избавив Армению от владычества Халифата.",
        "image": "/static/lab2/ashot.png"
    },
    {
        "name": "Левон I Киликийский - Լեւոն Բ Մեծագործ",
        "description": "Этот армянский царь из династии Рубенидов правил в конце XII века в Киликийской Армении. И сделал свою державу одним из величайших на Средиземном море, центром армянской государственности после падения Ани и Багратидской Армении.",
        "image": "/static/lab2/levon.png"
    }
]


@lab2.route('/lab2/kings')
def cars_list():
    return render_template('lab2/kings.html', kings=kings)