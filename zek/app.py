# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, create_user, get_user_by_username, get_user_balance
from models import get_purchased_games


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'supersecretkey'

db.init_app(app)

# Код для создания таблицы пользователей
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('osn.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if create_user(username, password):
            return redirect(url_for('main_page'))
        else:
            flash('Этот никнейм уже занят')
    return render_template('registr.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user is None:
            flash('Такого пользователя не существует')
        elif user.password != password:
            flash('Не верный пароль')
        else:
            session['username'] = username
            return redirect(url_for('main_page'))
    return render_template('login.html')

@app.route('/main')
def main_page():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user_balance = get_user_balance(username)
    return render_template('main.html', username=username, user_balance=user_balance)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/games')
def games():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user_balance = get_user_balance(username)
    return render_template('Games.html', username=username, user_balance=user_balance)

@app.route('/game1_details')
def game1_details():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user_balance = get_user_balance(username)
    return render_template('game1_details.html', username=username, user_balance=user_balance)


@app.route('/game2_details')
def game2_details():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user_balance = get_user_balance(username)
    return render_template('game2_details.html', username=username, user_balance=user_balance)


@app.route('/game3_details')
def game3_details():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user_balance = get_user_balance(username)
    return render_template('game3_details.html', username=username, user_balance=user_balance)


@app.route('/game4_details')
def game4_details():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user_balance = get_user_balance(username)
    return render_template('game4_details.html', username=username, user_balance=user_balance)


@app.route('/game5_details')
def game5_details():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user_balance = get_user_balance(username)
    return render_template('game5_details.html', username=username, user_balance=user_balance)


@app.route('/game6_details')
def game6_details():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user_balance = get_user_balance(username)
    return render_template('game6_details.html', username=username, user_balance=user_balance)


@app.route('/buy_game', methods=['POST'])
def buy_game():
    if 'username' not in session:
        return 'Unauthorized', 401

    game_id = request.json.get('game_id')
    username = session['username']
    user = get_user_by_username(username)
    if not user:
        return 'User not found', 404

    game_prices = {
        1: 2199,
        2: 3000,
        3: 1499,
        4: 2300,
        5: 3300,
        6: 7800
    }

    game_price = game_prices.get(game_id)
    if game_price is None:
        return 'Invalid game ID', 400

    if user.balance < game_price:
        return 'Insufficient funds', 400

    # Проверяем, куплена ли уже игра
    if getattr(user, f'game{game_id}'):
        return 'Game already purchased', 400

    # Вычитаем цену игры из баланса пользователя
    user.balance -= game_price

    # Устанавливаем флаг покупки игры
    setattr(user, f'game{game_id}', True)

    db.session.commit()

    return 'Game purchased', 200

# app.py

@app.route('/purchased_games')
def purchased_games():
    username = session.get('username')
    user_balance = get_user_balance(username)
    if not username:
        return redirect(url_for('login'))
    purchased_games = get_purchased_games(username)  # Передаем имя пользователя
    return render_template('purchased_games.html', purchased_games=purchased_games, username=username, user_balance=user_balance)



@app.route('/balance')
def balance():
    # Здесь может быть ваша логика для отображения страницы с пополнением баланса
    return render_template('balance.html')  # Замените 'balance.html' на ваш шаблон



@app.route('/Kotya/admin7')
def secret_page():
    return render_template('secret_page.html')

# Добавление баланса
@app.route('/add_balance', methods=['POST'])
def add_balance():
    username = request.form['username']
    amount = int(request.form['amount'])
    user = get_user_by_username(username)
    if user:
        user.balance += amount
        db.session.commit()
        flash(f'Баланс пользователя {username} увеличен на {amount} котомонет.')
    else:
        flash('Пользователь не найден.')
    return redirect(url_for('secret_page'))

# Отнятие баланса
@app.route('/subtract_balance', methods=['POST'])
def subtract_balance():
    username = request.form['username']
    amount = int(request.form['amount'])
    user = get_user_by_username(username)
    if user:
        user.balance -= amount
        db.session.commit()
        flash(f'Баланс пользователя {username} уменьшен на {amount} котомонет.')
    else:
        flash('Пользователь не найден.')
    return redirect(url_for('secret_page'))

# Удаление аккаунта
@app.route('/delete_account', methods=['POST'])
def delete_account():
    username = request.form['username']
    user = get_user_by_username(username)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'Аккаунт пользователя {username} удален.')
    else:
        flash('Пользователь не найден.')
    return redirect(url_for('secret_page'))

if __name__ == '__main__':
    app.run(debug=True)
