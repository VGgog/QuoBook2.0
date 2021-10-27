from app.models import Users
from app import passwords
from flask import flash, redirect, url_for


def check_password(username, password):
    """Проверяет правильность введённого пароля"""
    password_hash = Users.query.filter_by(username=username).first().password_hash
    if passwords.check_password(password_hash, password):
        return True

    return False


def check_user(username, password, page):
    """Проверяет существования логина и правильность введённого пароля."""
    if not Users.query.filter_by(username=username).first():
        flash('Такой логин не зарегистрирован.')
        return redirect(url_for(page))

    if not check_password(username, password):
        flash('Пароль не верный.')
        return redirect(url_for(page))

    return True
