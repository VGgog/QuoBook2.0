from app.api import bp
from flask import jsonify, request
from app.models import Quote, Users
from app import db
from app.api import func
from random import randrange


@bp.route('/quote/<int:quote_id>', methods=['GET'])
def send_quotes_on_quote_id(quote_id):
    """Возвращает цитату по id цитаты"""
    return jsonify(func.translates_into_the_correct_format(Quote.query.get_or_404(quote_id)))


@bp.route('/quote/<string:author_or_book_title>', methods=['GET'])
def send_quotes_on_author_or_book_title(author_or_book_title):
    """Возвращает цитату по автору или названию книги"""
    if Quote.query.filter_by(author=author_or_book_title).first():
        return jsonify(func.translates_into_the_correct_format(Quote.query.filter_by(
            author=author_or_book_title).first()))

    if Quote.query.filter_by(book_title=author_or_book_title).first():
        return jsonify(func.translates_into_the_correct_format(Quote.query.filter_by(
            book_title=author_or_book_title).first()))

    return "Author or book title not found", 404


@bp.route('/quotes/<int:count>', methods=['GET'])
def send_give_count_quotes(count):
    """Возвращает случайные цитаты в заданном количестве"""
    quotes = []
    quotes_id = []
    i = 0
    while i < count:
        quote_id = randrange(1, Quote.query.count())
        if quote_id not in quotes_id:
            quotes.append(func.translates_into_the_correct_format(Quote.query.get_or_404(quote_id)))
            quotes_id.append(quote_id)
            i += 1

        if len(quotes_id) == Quote.query.count():
            break
    return jsonify(quotes), 200


@bp.route('/new_quote', methods=['POST', 'PUT'])
def add_new_quote():
    """Добавляет новую цитату"""
    quote_id = None
    if request.args.get('quote_id'):
        try:
            quote_id = int(request.args['quote_id'])
        except ValueError:
            return "Not true request", 400

    quote_data = request.get_json()
    if func.checking_correctness_json(quote_data):
        if func.check_user(quote_data):
            info_for_quote = quote_data['quote']

            if quote_id:
                if func.check_user_id_and_quote_user_id(quote_data, quote_id):
                    if Quote.query.filter_by(quote_id=quote_id).first():
                        db.session.delete(Quote.query.filter_by(quote_id=quote_id).first())
                    quote = func.made_quote_obj(quote_data, quote_id=quote_id)
                else:
                    return "You do not have permission to update this quote.", 403
            else:
                if Quote.query.filter_by(quote=info_for_quote['quote']).first():
                    return "This quote already added.", 404

                quote = func.made_quote_obj(quote_data, quote_id=Quote.query.count() + 1)
            db.session.add(quote)
            db.session.commit()
            return jsonify(func.translates_into_the_correct_format(
                Quote.query.filter_by(quote=info_for_quote['quote']).first())), 200
        return "Login or password is incorrect", 401
    return "The form of the submitted json is not correct.", 400


@bp.route('del_quote/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    """Delete-метод, удаляет цитату, если её добавляли Вы."""
    quote_data = request.get_json()
    if "login" and "password" in quote_data:

        if func.check_user(quote_data):
            if func.check_user_id_and_quote_user_id(quote_data, quote_id):
                quote = Quote.query.filter_by(quote_id=quote_id).first()
                db.session.delete(Quote.query.filter_by(quote_id=quote_id).first())
                db.session.commit()
                return jsonify(func.translates_into_the_correct_format(quote)), 200

            return "You do not have permission to delete this quote.", 403
        return "Login or password is incorrect", 401
    return "The form of the submitted json is not correct.", 400
