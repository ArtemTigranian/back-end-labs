from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)

# Страница 1: Ввод имени
@lab9.route('/lab9/', methods=['GET', 'POST'])
def lab():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('lab9.age', name=name))
    return render_template('lab9/lab9.html')

# Страница 2: Ввод возраста
@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = int(request.form['age'])
        return redirect(url_for('lab9.gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)

# Страница 3: Ввод пола
@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form['gender']
        return redirect(url_for('lab9.preference', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)

# Страница 4: Выбор предпочтений
@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def preference():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    if request.method == 'POST':
        preference = request.form['preference']
        return redirect(url_for('lab9.style', name=name, age=age, gender=gender, preference=preference))
    return render_template('lab9/preference.html', name=name, age=age, gender=gender)

# Страница 5: Красивое или функциональное
@lab9.route('/lab9/style', methods=['GET', 'POST'])
def style():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    if request.method == 'POST':
        style = request.form['style']
        return redirect(url_for('lab9.congratulations', name=name, age=age, gender=gender, preference=preference, style=style))
    return render_template('lab9/style.html', name=name, age=age, gender=gender, preference=preference)

@lab9.route('/lab9/congratulations', methods=['GET'])
def congratulations():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    style = request.args.get('style')

    # Логика выбора подарка
    if age <= 12:
        if preference == 'дорогое' and style == 'красивое':
            gift = 'Футбольная форма Роналдо' if gender == 'мужчина' else 'Платье'
            image = 'football_jersey.png' if gender == 'мужчина' else 'dress.png'
        elif preference == 'дорогое' and style == 'функциональное':
            gift = 'Машинка на пульте управления' if gender == 'мужчина' else 'Айфон'
            image = 'remote_car.jpg' if gender == 'мужчина' else 'iphone.jpg'
        elif preference == 'милое' and style == 'красивое':
            gift = 'Новогодний свитер'
            image = 'sweater.jpg'
        elif preference == 'милое' and style == 'функциональное':
            gift = 'Санки'
            image = 'sled.jpg'
    else:
        if preference == 'дорогое' and style == 'красивое':
            gift = 'Часы Ролекс' if gender == 'мужчина' else 'Браслет Картье'
            image = 'rolex.jpg' if gender == 'мужчина' else 'bracelet.jpg'
        elif preference == 'дорогое' and style == 'функциональное':
            gift = 'Плейстейшн 5' if gender == 'мужчина' else 'Фен Дайсон'
            image = 'ps5.jpg' if gender == 'мужчина' else 'dyson_dryer.jpg'
        elif preference == 'милое' and style == 'красивое':
            gift = 'Новогодний свитер'
            image = 'sweater.jpg'
        elif preference == 'милое' and style == 'функциональное':
            gift = 'Новогодняя книга'
            image = 'new_year_book.jpg'

    # Поздравления для каждой категории
    if age <= 12:
        if gender == 'мужчина':
            message = f"Поздравляю тебя, {name}! Пусть твои мечты сбудутся, а впереди будет много побед, интересных приключений и новых достижений! Желаю, чтобы ты всегда был таким же веселым и активным! Вот тебе подарок — {gift}."
        else:
            message = f"Поздравляю тебя, {name}! Пусть в твоей жизни будет много радости, улыбок и волшебных моментов! Желаю расти умной, красивой и уверенной в себе девочкой! Вот тебе подарок — {gift}."
    else:
        if gender == 'мужчина':
            message = f"Поздравляю тебя, {name}! Пусть этот год принесет тебе много удачи и успешных начинаний! Желаю всегда быть сильным, уверенным и достигать больших целей! Твой подарок — {gift}!"
        else:
            message = f"Поздравляю тебя, {name}! Пусть твоя жизнь будет наполнена счастьем, гармонией и красивыми моментами. Желаю здоровья, любви и успехов во всем! Твой подарок — {gift}!"

    return render_template('lab9/congratulations.html', name=name, gift=gift, image=image, message=message)

