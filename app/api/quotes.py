from app.api import check, quote_management
from random import randrange, choice
from app.models import Quote, Users
from flask import jsonify, request
from app.api import bp
from app import db


@bp.route('/quote', methods=['GET'])
def send_a_random_quote():
    """Отправляет случайную цитату"""
    return jsonify(quote_management.return_dict_quote_info(Quote.query.get_or_404(randrange(1, Quote.query.count()))))


@bp.route('/quote/<int:quote_id>', methods=['GET'])
def send_quote_on_quote_id(quote_id):
    """Отправляет цитату по id цитаты"""
    return jsonify(quote_management.return_dict_quote_info(Quote.query.get_or_404(quote_id)))


@bp.route('/quote/<string:author_or_book_title>', methods=['GET'])
def send_quote_on_author_or_book_title(author_or_book_title):
    """Отправляет цитату отфильтрованную по автору или названию книги"""
    if Quote.query.filter_by(author=author_or_book_title).first():
        return jsonify(quote_management.return_dict_quote_info(Quote.query.filter_by(
            author=author_or_book_title).first()))

    if Quote.query.filter_by(book_title=author_or_book_title).first():
        return jsonify(quote_management.return_dict_quote_info(Quote.query.filter_by(
            book_title=author_or_book_title).first()))

    return "Author or book title not found", 404


@bp.route('/quote/<string:author>/<string:book_title>', methods=['GET'])
def send_quote_author_and_book_title(author, book_title):
    """Сортирует цитаты по автору и названию книги, и отправляет случайную цитату из отсортированных"""
    quotes = []
    for quote in Quote.query.filter_by(author=author):
        if quote.book_title == book_title:
            quotes.append(quote)

    if quotes:
        return jsonify(quote_management.return_dict_quote_info(choice(quotes)))

    return "Quote not found", 404


@bp.route('/quotes/<int:count>', methods=['GET'])
def send_give_count_quotes(count):
    """Отправляет случайные цитаты в заданном количестве"""
    quotes = []
    quotes_id = []
    i = 0
    while i < count:
        quote_id = randrange(1, Quote.query.count())
        if quote_id not in quotes_id:
            quotes.append(quote_management.return_dict_quote_info(Quote.query.get_or_404(quote_id)))
            quotes_id.append(quote_id)
            i += 1

        # Если пользователь задаст количество цитат большее чем имеется в бд, то цикл станет бесконечным.
        # Во избежание этого добавлен этот if.
        if len(quotes_id) == Quote.query.count():
            break
    return jsonify(quotes), 200


@bp.route('/all_quotes', methods=['POST'])
def send_all_quote_id_which_add_user():
    """Отправляет id всех цитат, добавленных пользователем"""
    token_data = request.get_json() or {}
    quotes_id = []
    if not (check.token_in_json(token_data) and check.token_in_db(token_data['token'])):
        return "The form of the submitted json is not correct.", 400

    for quote in Quote.query.filter_by(user_id=Users.query.filter_by(token=token_data['token']).first().user_id):
        quotes_id.append({'quote_id': quote.quote_id})

    if quotes_id:
        return jsonify(quotes_id)
    return 'You not add quotes', 404


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


@bp.route('del_quote/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    """Удаляет цитату, если Вы её добавляли."""
    token_data = request.get_json() or {}

    if not (check.token_in_json(token_data) and check.token_in_db(token_data['token'])):
        return "The form or the token of the submitted json is not correct.", 400

    if not check.user_and_quote_user_id(token_data['token'], quote_id):
        return "You do not have permission to delete this quote.", 403

    quote = Quote.query.filter_by(quote_id=quote_id).first()
    db.session.delete(Quote.query.filter_by(quote_id=quote_id).first())
    db.session.commit()
    return jsonify(quote_management.return_dict_quote_info(quote)), 200
