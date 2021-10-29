from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Users
import random


def make_password_hash(password):
    """Создаёт хэш пароля"""
    return generate_password_hash(password)


def check_hash_password(password_hash, password):
    """Сравнивает хэш-пароля и заданный пароль"""
    return check_password_hash(password_hash, password)


def check_password(username, password):
    """Проверяет правильность введённого пароля"""
    password_hash = Users.query.filter_by(username=username).first().password_hash
    if check_hash_password(password_hash, password):
        return True

    return False


def generate_token():
    """Генерирует токен"""
    SYMBLS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    token = ''
    for i in range(32):
        token += random.choice(SYMBLS)

    return token
