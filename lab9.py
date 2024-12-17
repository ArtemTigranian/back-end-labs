from flask import Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def lab():
    if 'name' in session:
        return redirect(url_for('lab9.congratulations'))
    
    if request.method == 'POST':
        session['name'] = request.form['name']
        return redirect(url_for('lab9.age'))
    
    return render_template('lab9/lab9.html')

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    if 'name' not in session:
        return redirect(url_for('lab9.lab'))
    
    if request.method == 'POST':
        session['age'] = int(request.form['age'])
        return redirect(url_for('lab9.gender'))
    
    return render_template('lab9/age.html')

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    if 'name' not in session or 'age' not in session:
        return redirect(url_for('lab9.lab'))
    
    if request.method == 'POST':
        session['gender'] = request.form['gender']
        return redirect(url_for('lab9.preference'))
    
    return render_template('lab9/gender.html')

@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def preference():
    if 'name' not in session or 'age' not in session or 'gender' not in session:
        return redirect(url_for('lab9.lab'))
    
    if request.method == 'POST':
        session['preference'] = request.form['preference']
        return redirect(url_for('lab9.style'))
    
    return render_template('lab9/preference.html')

@lab9.route('/lab9/style', methods=['GET', 'POST'])
def style():
    if 'name' not in session or 'age' not in session or 'gender' not in session or 'preference' not in session:
        return redirect(url_for('lab9.lab'))
    
    if request.method == 'POST':
        session['style'] = request.form['style']
        return redirect(url_for('lab9.congratulations'))
    
    return render_template('lab9/style.html')

@lab9.route('/lab9/congratulations', methods=['GET'])
def congratulations():
    if 'name' not in session or 'age' not in session or 'gender' not in session or 'preference' not in session or 'style' not in session:
        return redirect(url_for('lab9.lab'))
    
    name = session['name']
    age = session['age']
    gender = session['gender']
    preference = session['preference']
    style = session['style']
    
    if age <= 12:
        if preference == 'дорогое' and style == 'красивое':
            gift = 'Футбольная форма Роналдо' if gender == 'мужчина' else 'Платье'
            image = 'football_jersey.jpg' if gender == 'мужчина' else 'dress.jpg'
        elif preference == 'дорогое' and style == 'функциональное':
            gift = 'Машинка на пульте управления' if gender == 'мужчина' else 'Айфон'
            image = 'remote_car.jpg' if gender == 'мужчина' else 'iphone.jpg'
        elif preference == 'милое' and style == 'красивое':
            gift = 'Новогодний свитер' if gender == 'мужчина' else 'Новогодний'
            image = 'sweater.jpg'
        elif preference == 'милое' and style == 'функциональное':
            gift = 'Санки' if gender == 'мужчина' else 'Санки'
            image = 'sled.jpg'
    else:
        if preference == 'дорогое' and style == 'красивое':
            gift = 'Часы Ролекс' if gender == 'мужчина' else 'Браслет Картье'
            image = 'rolex.jpg' if gender == 'мужчина' else 'bracelet.jpg'
        elif preference == 'дорогое' and style == 'функциональное':
            gift = 'Плейстейшн 5' if gender == 'мужчина' else 'Фен Дайсон'
            image = 'ps5.jpg' if gender == 'мужчина' else 'dyson_dryer.jpg'
        elif preference == 'милое' and style == 'красивое':
            gift = 'Новогодний свитер' if gender == 'мужчина' else 'Новогодний свитер'
            image = 'mens_sweater.jpg' if gender == 'мужчина' else 'womens_sweater.jpg'
        elif preference == 'милое' and style == 'функциональное':
            gift = 'Новогодняя книга'
            image = 'new_year_book.jpg'

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

@lab9.route('/lab9/reset')
def reset():
    session.clear()
    return redirect(url_for('lab9.lab'))