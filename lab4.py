from flask import Blueprint, url_for, redirect, render_template, request, make_response, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2

    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = int(request.form.get('x1') or 0)
    x2 = int(request.form.get('x2') or 0)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = int(request.form.get('x1') or 1)
    x2 = int(request.form.get('x2') or 1)
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/exp-form')
def exp_form():
    return render_template('lab4/exp-form.html')


@lab4.route('/lab4/exp', methods=['POST'])
def exp():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/exp.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/exp.html', error='Оба значения не могут быть равны нулю.')
    result = x1 ** x2
    return render_template('lab4/exp.html', x1=x1, x2=x2, result=result)

tree_count = 0
max_trees = 10 

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < max_trees:
        tree_count += 1

    return redirect('/lab4/tree')


users_dict = {
    'alex': {'password': '123', 'name': 'Alexander Ivanov', 'gender': 'male'},
    'artem': {'password': '777', 'name': 'Artem Smirnov', 'gender': 'male'},
    'thomas': {'password': '365', 'name': 'Thomas Johnson', 'gender': 'male'},
    'theodor': {'password': '321', 'name': 'Theodor White', 'gender': 'male'},
    'bob': {'password': '555', 'name': 'Robert Brown', 'gender': 'male'}
}

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if not login or not password or not name:
            error = 'Все поля обязательны для заполнения'
            return render_template('lab4/register.html', error=error)

        if login in users_dict:
            error = 'Пользователь с таким логином уже существует'
            return render_template('lab4/register.html', error=error)

        users_dict[login] = {'password': password, 'name': name}
        return redirect('/lab4/login')

    return render_template('lab4/register.html')

@lab4.route('/lab4/users')
def users():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user = session['login']
    return render_template('lab4/users.html', users=users_dict, current_user=current_user)


@lab4.route('/lab4/delete_user', methods=['POST'])
def delete_user():
    login = session.pop('login', None)
    if login and login in users_dict:
        del users_dict[login]
    return redirect('/lab4/login')

@lab4.route('/lab4/edit_user', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    login = session['login']
    user = users_dict.get(login)

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_password = request.form.get('password')

        if new_name:
            user['name'] = new_name
        if new_password:
            user['password'] = new_password

        return redirect('/lab4/users')

    return render_template('lab4/edit_user.html', user=user)


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            user = users_dict.get(login)
            name = user['name'] if user else ''
        else:
            authorized = False
            name = ''
        return render_template('lab4/login.html', authorized=authorized, name=name)

    login = request.form.get('login')
    password = request.form.get('password')
    
    # Проверка на пустое значение логина и пароля
    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    # Проверка логина и пароля
    user = users_dict.get(login)
    if user and user['password'] == password:
        session['login'] = login
        return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    snowflakes = 0
    if request.method == 'GET':
        return render_template('lab4/fridge.html', message='', temperature='')

    temperature = request.form.get('temperature')
    
    if temperature is None or temperature.strip() == '':
        message = 'Ошибка: не задана температура'
        return render_template('lab4/fridge.html', message=message, temperature=temperature)

    try:
        temperature = int(temperature)
    except ValueError:
        message = 'Ошибка: температура должна быть числом'
        return render_template('lab4/fridge.html', message=message, temperature=temperature)
    
    if temperature < -12:
        message = 'Не удалось установить температуру — слишком низкое значение'
    elif temperature > -1:
        message = 'Не удалось установить температуру — слишком высокое значение'
    elif -12 <= temperature <= -9:
        message = f'Установлена температура: {temperature}°С'
        snowflakes = 3
    elif -8 <= temperature <= -5:
        message = f'Установлена температура: {temperature}°С'
        snowflakes = 2
    elif -4 <= temperature <= -1:
        message = f'Установлена температура: {temperature}°С'
        snowflakes = 1
    else:
        message = 'Ошибка: недопустимая температура'
        snowflakes = 0

    return render_template('lab4/fridge.html', message=message, temperature=temperature, snowflakes=snowflakes)


@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():
    grain_prices = {
        'ячмень': 12345,
        'овёс': 8522,
        'пшеница': 8722,
        'рожь': 14111
    }
    
    if request.method == 'GET':
        return render_template('lab4/grain_order.html', message='', grain_type='', weight='')

    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    if not weight:
        message = 'Ошибка: не указан вес'
        return render_template('lab4/grain_order.html', message=message, grain_type=grain_type, weight=weight)

    try:
        weight = float(weight)
    except ValueError:
        message = 'Ошибка: вес должен быть числом'
        return render_template('lab4/grain_order.html', message=message, grain_type=grain_type, weight=weight)
    
    if weight <= 0:
        message = 'Ошибка: вес должен быть больше 0'
        return render_template('lab4/grain_order.html', message=message, grain_type=grain_type, weight=weight)

    if weight > 500:
        message = 'Ошибка: такого объёма сейчас нет в наличии'
        return render_template('lab4/grain_order.html', message=message, grain_type=grain_type, weight=weight)

    price_per_ton = grain_prices.get(grain_type)
    if not price_per_ton:
        message = 'Ошибка: неверный тип зерна'
        return render_template('lab4/grain_order.html', message=message, grain_type=grain_type, weight=weight)

    total_cost = weight * price_per_ton
    discount_message = ''
    
    if weight > 50:
        discount = total_cost * 0.10
        total_cost -= discount
        discount_message = f'Скидка за большой объём: 10%, размер скидки: {discount:.2f} руб'

    message = f'Заказ успешно сформирован. Вы заказали {grain_type}. Вес: {weight} т. Сумма к оплате: {total_cost:.2f} руб.'

    return render_template('lab4/grain_order.html', message=message, grain_type=grain_type, weight=weight, discount_message=discount_message)
