from app.api import bp
from flask import jsonify, request
from app.models import Quote, Users
from app import db
from app.api import func


@bp.route('/quote/<int:quote_id>', methods=['GET'])
def send_quotes_on_quote_id(quote_id):
    """Возвращает цитату по id цитаты"""
    return jsonify(func.translates_into_the_correct_format(Quote.query.get_or_404(quote_id)))


@bp.route('/quote/<string:author_or_book_title>', methods=['GET'])
def send_quotes_on_author(author_or_book_title):
    """Возвращает цитату по автору или названию книги"""
    if Quote.query.filter_by(author=author_or_book_title).first():
        return jsonify(func.translates_into_the_correct_format(Quote.query.filter_by(
            author=author_or_book_title).first()))

    if Quote.query.filter_by(book_title=author_or_book_title).first():
        return jsonify(func.translates_into_the_correct_format(Quote.query.filter_by(
            book_title=author_or_book_title).first()))

    return "Author or book title not found", 404


@bp.route('/new_quote', methods=['POST'])
def add_new_quote():
    quote_data = request.get_json()
    if 'login' and 'password' and 'quote' in quote_data:

        if Users.query.filter_by(username=quote_data['login']).first():

            password_hash = Users.query.filter_by(username=quote_data['login']).first().password_hash
            if Users.check_password(password_hash, quote_data['password']):

                info_for_quote = quote_data['quote']
                if 'author' and 'book_title' and 'quote' in info_for_quote:

                    # Проверяет наличие цитаты в бд.
                    if not Quote.query.filter_by(quote=info_for_quote['quote']).first():

                        user_id = Users.query.filter_by(username=quote_data['login']).first().user_id
                        quote = Quote(user_id=user_id, quote_id=Quote.query.count() + 1,  author=info_for_quote['author'],
                                      book_title=info_for_quote['book_title'], quote=info_for_quote['quote'])
                        db.session.add(quote)
                        db.session.commit()

                        return jsonify(func.translates_into_the_correct_format(
                            Quote.query.filter_by(quote=info_for_quote['quote']).first()))

                    return "This quote already added"

                return "The form of the submitted json is not correct.", 400
            return "Password is incorrect", 401
        return "Login is incorrect", 401
    return "The form of the submitted json is not correct.", 400
