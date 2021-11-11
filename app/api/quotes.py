from app.api import bp
from flask import jsonify, request
from app.models import Quote, Users
from app import db
from app.api import check, quote_management
from random import randrange, choice
from werkzeug.security import generate_password_hash
from app import generate_token


@bp.route('/quote/<int:quote_id>', methods=['GET'])
def send_quotes_on_quote_id(quote_id):
    """Возвращает цитату по id цитаты"""
    return jsonify(quote_management.return_dict_quote_info(Quote.query.get_or_404(quote_id)))


@bp.route('/quote/<string:author_or_book_title>', methods=['GET'])
def send_quotes_on_author_or_book_title(author_or_book_title):
    """Возвращает цитату по автору или названию книги"""
    if Quote.query.filter_by(author=author_or_book_title).first():
        return jsonify(quote_management.return_dict_quote_info(Quote.query.filter_by(
            author=author_or_book_title).first()))

    if Quote.query.filter_by(book_title=author_or_book_title).first():
        return jsonify(quote_management.return_dict_quote_info(Quote.query.filter_by(
            book_title=author_or_book_title).first()))

    return "Author or book title not found", 404


@bp.route('/quote/<string:author>/<string:book_title>', methods=['GET'])
def send_quotes_author_and_book_title(author, book_title):
    """Фильтрует цитаты по автору и названию книги, и возвращает случайную цитату"""
    quotes = []
    for quote in Quote.query.filter_by(author=author):
        if quote.book_title == book_title:
            quotes.append(quote)

    if quotes:
        return jsonify(quote_management.return_dict_quote_info(choice(quotes)))

    return "Quote not found", 404


@bp.route('/quotes/<int:count>', methods=['GET'])
def send_give_count_quotes(count):
    """Возвращает случайные цитаты в заданном количестве"""
    quotes = []
    quotes_id = []
    i = 0
    while i < count:
        quote_id = randrange(1, Quote.query.count())
        if quote_id not in quotes_id:
            quotes.append(quote_management.return_dict_quote_info(Quote.query.get_or_404(quote_id)))
            quotes_id.append(quote_id)
            i += 1

        if len(quotes_id) == Quote.query.count():
            break
    return jsonify(quotes), 200


@bp.route('/all_quotes', methods=['POST'])
def send_all_quote_id_which_add_user():
    """Возвращает id всех цитат, добавленных пользователем"""
    quote_data = request.get_json() or {}
    quotes_id = []
    if not (check.token_in_json(quote_data) and check.token_in_db(quote_data['token'])):
        return "The form of the submitted json is not correct.", 400

    for quote in Quote.query.filter_by(user_id=Users.query.filter_by(token=quote_data['token']).first().user_id):
        quotes_id.append({'quote_id': quote.quote_id})

    if quotes_id:
        return jsonify(quotes_id)
    return 'You not add quotes', 404


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


@bp.route('/new_quote', methods=['POST', 'PUT'])
def add_new_quote():
    """Добавляет новую цитату или изменяет существующую """
    quote_id = request.args.get('quote_id', type=int) or None
    quote_data = request.get_json() or {}

    if not check.correct_form_sent_json(quote_data):
        return "The form of the submitted json is not correct.", 400
    if not check.token_in_db(quote_data['token']):
        return "Token is incorrect", 401

    quote_text = quote_data['quote']['quote']
    if Quote.query.filter_by(quote=quote_text).first():
        return "This quote already added.", 404

    if quote_id:
        if not check.user_and_quote_user_id(quote_data['token'], quote_id):
            return "You do not have permission to update this quote.", 403
        if Quote.query.filter_by(quote_id=quote_id).first():
            db.session.delete(Quote.query.filter_by(quote_id=quote_id).first())
        quote = quote_management.creates_a_quote_object(quote_data, quote_id=quote_id)
    else:
        quote = quote_management.creates_a_quote_object(quote_data, quote_id=Quote.query.count() + 1)

    db.session.add(quote)
    db.session.commit()
    return jsonify(quote_management.return_dict_quote_info(
        Quote.query.filter_by(quote=quote_text).first())), 200


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


@bp.route('del_quote/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    """Delete-метод, удаляет цитату, если Вы её добавляли."""
    quote_data = request.get_json() or {}

    if not (check.token_in_json(quote_data) and check.token_in_db(quote_data['token'])):
        return "The form or the token of the submitted json is not correct.", 400

    if not check.user_and_quote_user_id(quote_data['token'], quote_id):
        return "You do not have permission to delete this quote.", 403

    quote = Quote.query.filter_by(quote_id=quote_id).first()
    db.session.delete(Quote.query.filter_by(quote_id=quote_id).first())
    db.session.commit()
    return jsonify(quote_management.return_dict_quote_info(quote)), 200
