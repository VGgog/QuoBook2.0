import random


def generate_token():
    """Генерирует токен"""
    SYMBLS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    token = ''
    for i in range(32):
        token += random.choice(SYMBLS)

    return token
