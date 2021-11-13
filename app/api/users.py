from werkzeug.security import generate_password_hash
from app import generate_token
from app.models import Users
from app.api import check
from flask import request
from app.api import bp
from app import db


@bp.route('/registration', methods=['POST'])
def registration_new_user():
    """Регистрация нового пользователя"""
    quote_data = request.get_json() or {}
    if not check.login_and_password_in_sent_json(quote_data):
        return "The form of the submitted json is not correct.", 400

    if Users.query.filter_by(username=quote_data['login']).first():
        return "A user with this username already exists", 401

    user = Users(user_id=Users.query.count() + 1, username=quote_data['login'],
                 password_hash=generate_password_hash(quote_data['password']), token=generate_token.generate_token())
    db.session.add(user)
    db.session.commit()
    return user.token, 200


@bp.route('/changed_password', methods=['PUT'])
def changed_pass():
    """Позволяет поменять пароль"""
    quote_data = request.get_json()
    if not check.login_and_password_in_sent_json(quote_data) and ('new_password' in quote_data):
        return "The form of the submitted json is not correct.", 400

    if not check.user_login_and_password(quote_data):
        return "Login or password is incorrect", 401

    if not Users.query.filter_by(username=quote_data['login']).first():
        return "This login not found", 404

    user = Users.query.filter_by(username=quote_data['login']).first()
    user.password_hash = generate_password_hash(quote_data['new_password'])
    db.session.commit()
    return "You have successful changed password", 200


@bp.route('/del_user', methods=['DELETE'])
def delete_user():
    """Удаляет пользователя"""
    quote_data = request.get_json()
    if not check.login_and_password_in_sent_json(quote_data):
        return "The form of the submitted json is not correct.", 400

    if not Users.query.filter_by(username=quote_data['login']).first():
        return "This login not found", 404

    if not check.user_login_and_password(quote_data):
        return "Login or password is incorrect", 401

    db.session.delete(Users.query.filter_by(username=quote_data['login']).first())
    db.session.commit()
    return "This user successful delete", 200
