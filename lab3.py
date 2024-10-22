from flask import Blueprint, url_for, redirect, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    age = request.cookies.get('age')
    name_color = request.cookies.get('name_color')
    if name is None:
        name = 'Анонимус'
    if age is None:
        age = 'неизвестно'
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3'))
    resp.set_cookie('name', 'Artem', max_age=5)
    resp.set_cookie('age', '19')
    resp.set_cookie('name_color', 'limegreen')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    resp.delete_cookie('bcolor')
    resp.delete_cookie('color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_family')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    if sex == '':
        errors['sex'] = 'Заполните поле!'
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')

    if drink == 'coffee':
        price = 250
    elif drink == 'black-tea':
        price = 220
    else:
        price = 200

    if request.args.get('milk') == 'on':
        price += 20
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    bcolor = request.args.get('bcolor')
    color = request.args.get('color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')

    resp = make_response(redirect('/lab3/settings'))

    if bcolor:
        resp.set_cookie('bcolor', bcolor)
    if color:
        resp.set_cookie('color', color)
    if font_size:
        resp.set_cookie('font_size', font_size)
    if font_family:
        resp.set_cookie('font_family', font_family)

    if bcolor or font_size or font_family or color:
        return resp

    return render_template('lab3/settings.html', bcolor=request.cookies.get('bcolor'), color=request.cookies.get('color'), font_size=request.cookies.get('font_size'), font_family=request.cookies.get('font_family'))


@lab3.route('/lab3/ticket_order')
def ticket_order():
    return render_template('lab3/ticket_order.html')


@lab3.route('/lab3/ticket_success', methods=['POST'])
def ticket_success():
    errors = {}
    
    full_name = request.form.get('full_name')
    if not full_name:
            errors['full_name'] = 'Заполните ФИО'

    seat_type = request.form.get('seat_type')
    if not seat_type:
        errors['seat_type'] = 'Выберите тип полки'

    age = request.form.get('age')
    age = int(age)
    if not age:
        errors['age'] = 'Укажите корректный возраст (от 1 до 120 лет)'
    elif age is None:
        age=0

    departure = request.form.get('departure')
    if not departure:
        errors['departure'] = 'Укажите пункт выезда'

    destination = request.form.get('destination')
    if not destination:
        errors['destination'] = 'Укажите пункт назначения'
    
    travel_date = request.form.get('travel_date')
    if not travel_date:
            errors['travel_date'] = 'Укажите дату поездки'

    insurance = request.form.get('insurance') == 'on'
    bed = request.form.get('bed') == 'on'
    luggage = request.form.get('luggage') == 'on'

    ticket_type = "Детский билет" if age < 18 else "Взрослый билет"
    

    price = 1000 if age >= 18 else 700
    if seat_type == 'нижняя полка' or seat_type == 'нижняя боковая полка':
        price += 100
    if bed:
        price += 75
    if luggage:
        price += 250
    if insurance:
        price += 150
    
    return render_template('lab3/ticket_success.html', full_name=full_name, seat_type=seat_type, bed=bed, luggage=luggage, 
                           departure=departure, destination=destination, travel_date=travel_date, 
                           insurance=insurance, price=price, age=age, ticket_type=ticket_type)


products = [
    {"name": "Lexus", "price": 800, "type": "RX270", "color": "Черный"},
    {"name": "Lexus", "price": 700, "type": "RX300", "color": "Серебристый"},
    {"name": "Lexus", "price": 600, "type": "RX330", "color": "Белый"},
    {"name": "Lexus", "price": 500, "type": "RX350", "color": "Красный"},
    {"name": "Lexus", "price": 1500, "type": "RX400h", "color": "Черный"},
    {"name": "Lexus", "price": 1200, "type": "RX450h", "color": "Серебристый"},
    {"name": "Lexus", "price": 1300, "type": "GX460", "color": "Серебристый"},
    {"name": "Lexus", "price": 250, "type": "GX470", "color": "Черный"},
    {"name": "Lexus", "price": 400, "type": "GX500", "color": "Красный"},
    {"name": "Infiniti", "price": 200, "type": "FX30d", "color": "Белый"},
    {"name": "Infiniti", "price": 500, "type": "FX35", "color": "Белый"},
    {"name": "Infiniti", "price": 550, "type": "FX37", "color": "Черный"},
    {"name": "Infiniti", "price": 300, "type": "FX45", "color": "Черный"},
    {"name": "Infiniti", "price": 2000, "type": "FX50", "color": "Черный"},
    {"name": "BMW", "price": 1800, "type": "M2", "color": "Черный"},
    {"name": "BMW", "price": 200, "type": "M3", "color": "Белый"},
    {"name": "BMW", "price": 150, "type": "M4", "color": "Черный"},
    {"name": "BMW", "price": 1000, "type": "M5", "color": "Синий"},
    {"name": "BMW", "price": 1100, "type": "M6", "color": "Черный"},
    {"name": "BMW", "price": 900, "type": "M8", "color": "Серебристый"}
]

@lab3.route('/lab3/filter')
def index():
    return render_template('lab3/filter.html')

@lab3.route('/lab3/search', methods=['POST'])
def search():
    min_price = int(request.form.get('min_price'))
    max_price = int(request.form.get('max_price'))
    if not min_price or not max_price:
        return 'Заполните поля'

    filtered_products = [product for product in products if min_price <= product['price'] <= max_price]
    
    return render_template('lab3/search.html', products=filtered_products)