import random

from werkzeug.security import generate_password_hash, check_password_hash


def make_password_hash(password):
    """Создаёт хэш пароля"""
    return generate_password_hash(password)


def check_password(password_hash, password):
    """Сравнивает хэш-пароля и заданный пароль"""
    return check_password_hash(password_hash, password)


def generate_token():
    """Генерирует токен"""
    SYMBLS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    token = ''
    for i in range(32):
        token += random.choice(SYMBLS)

    return token
