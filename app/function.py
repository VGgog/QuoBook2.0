from app.models import Users, Quote
from app import passwords


def check_password(username, password):
    """Проверяет правильность введённого пароля"""
    password_hash = Users.query.filter_by(username=username).first().password_hash
    if passwords.check_password(password_hash, password):
        return True

    return False
