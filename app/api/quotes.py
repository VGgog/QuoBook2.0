from app.api import bp
from flask import jsonify
from app.models import Quote


@bp.route('/quotes/quote/<int:quote_id>', methods=['GET'])
def send_quotes(quote_id):
    info_for_quote = Quote.query.get_or_404(quote_id).__dict__
    quote = {
        'user_id': info_for_quote['user_id'],
        'quote_id': info_for_quote['quote_id'],
        'author': info_for_quote['author'],
        'book_title': info_for_quote['book_title'],
        'quote': info_for_quote['quote']
    }
    return jsonify(quote)
