from werkzeug.security import generate_password_hash
from validate_email import validate_email
from flask import request, jsonify
from app import generate_token
from app.models import Users
from app.api import check
from app.api import bp
from app import db


@bp.route('/registration', methods=['POST'])
def registration_new_user():
    """Регистрация нового пользователя, возвращает словарь {"token": <Токен>}"""
    user_data = request.get_json() or {}
    if not check.email_and_password_in_sent_json(user_data):
        return "The form of the submitted json is not correct.", 400

    if Users.query.filter_by(email=user_data['email']).first():
        return "A user with this username already exists", 401

    if not validate_email(user_data['email']):
        return "Please write right email", 401

    user = Users(user_id=Users.query.count() + 1, email=user_data['email'],
                 password_hash=generate_password_hash(user_data['password']), token=generate_token.generate_token())
    db.session.add(user)
    db.session.commit()
    return jsonify({"token": user.token}), 200


@bp.route('/authentication', methods=['POST'])
def user_authentication():
    """Авторизация пользователя, возвращает словарь {"token": <Токен>}"""
    user_data = request.get_json() or {}
    if not check.email_and_password_in_sent_json(user_data):
        return "The form of the submitted json is not correct.", 400

    if not Users.query.filter_by(email=user_data['email']).first():
        return "This email not found", 404

    if not validate_email(user_data['email']) or not check.user_login_and_password(user_data):
        return "Email or password is incorrect", 401

    return jsonify({'token': Users.query.filter_by(email=user_data['email']).first().token}), 200
