from app.api import bp
from flask import jsonify, request
from app.models import Quote, Users
from app import db
from app.api import func


@bp.route('/quotes/quote/<int:quote_id>', methods=['GET'])
def send_quotes(quote_id):
    """Возвращает цитату по id цитаты"""
    return jsonify(func.translates_into_the_correct_format(Quote.query.get_or_404(quote_id).__dict__))


@bp.route('/quote/new_quote', methods=['POST'])
def add_new_quote():
    quote_data = request.get_json()
    if 'login' and 'password' and 'quote' in quote_data:

        if Users.query.filter_by(username=quote_data['login']).first():

            password_hash = Users.query.filter_by(username=quote_data['login']).first().__dict__['password_hash']
            user_id = Users.query.filter_by(username=quote_data['login']).first().__dict__['user_id']
            if Users.check_password(password_hash, quote_data['password']):

                info_for_quote = quote_data['quote']
                if 'author' and 'book_title' and 'quote' in info_for_quote:
                    count = Quote.query.count()
                    quote = Quote(user_id=user_id, quote_id=count + 1,  author=info_for_quote['author'],
                                  book_title=info_for_quote['book_title'], quote=info_for_quote['quote'])
                    db.session.add(quote)
                    db.session.commit()

                    #info_for_add_quote = Quote.query.filter_by(quote=info_for_quote['quote']).first().__dict__
                    user_id = Quote.query.filter_by(quote=info_for_quote['quote']).first().__dict__['user_id']
                    quote_id = Quote.query.filter_by(quote=info_for_quote['quote']).first().__dict__['quote_id']
                    author = Quote.query.filter_by(quote=info_for_quote['quote']).first().__dict__['author']
                    book_title = Quote.query.filter_by(quote=info_for_quote['quote']).first().__dict__['book_title']
                    quote = Quote.query.filter_by(quote=info_for_quote['quote']).first().__dict__['quote']
                    new_quote = {
                        "user_id": user_id,
                        "quote_id": quote_id,
                        "quote": {
                            "author": author,
                            "book_title": book_title,
                            "quote": quote
                        }
                    }
                    return jsonify(new_quote)

                return "The form of the submitted json is not correct.", 404
            return "The specified password is incorrect", 404
        return "There is no user with this login.", 404
    return "The form of the submitted json is not correct.", 404
