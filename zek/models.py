# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer, default=0)
    game1 = db.Column(db.Boolean, default=False)  # Для игры 1
    game2 = db.Column(db.Boolean, default=False)  # Для игры 2
    game3 = db.Column(db.Boolean, default=False)  # Для игры 3
    game4 = db.Column(db.Boolean, default=False)  # Для игры 4
    game5 = db.Column(db.Boolean, default=False)  # Для игры 5
    game6 = db.Column(db.Boolean, default=False)  # Для игры 6


class regis(db.Model):
    code = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


def create_user(username, password):
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return True

def create_user(username, password):
    # Проверяем существование пользователя с таким именем
    existing_user = get_user_by_username(username)
    if existing_user:
        # Пользователь с таким именем уже существует, возвращаем False
        return False
    
    # Создаем нового пользователя
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return True


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_balance(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.balance
    else:
        return None  # Вернуть None, если пользователь не найден

def get_purchased_games(username):
    user = get_user_by_username(username)
    if user:
        purchased_games = []
        if user.game1:
            purchased_games.append({"name": "Game 1", "image": "game1.jpg", "purchased": True})
        if user.game2:
            purchased_games.append({"name": "Game 2", "image": "game2.jpg", "purchased": True})
        if user.game3:
            purchased_games.append({"name": "Game 3", "image": "game3.jpg", "purchased": True})
        if user.game4:
            purchased_games.append({"name": "Game 4", "image": "game4.jpg", "purchased": True})
        if user.game5:
            purchased_games.append({"name": "Game 5", "image": "game5.jpg", "purchased": True})
        if user.game6:
            purchased_games.append({"name": "Game 6", "image": "game6.jpg", "purchased": True})
        return purchased_games
    return []