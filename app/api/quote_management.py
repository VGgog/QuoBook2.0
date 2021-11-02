from app.models import Users, Quote


def return_dict_quote_info(info_for_quote):
    """Возвращает цитату в правильном формате"""
    return {
        'user_id': info_for_quote.user_id,
        'quote_id': info_for_quote.quote_id,
        'quote': {
            'author': info_for_quote.author,
            'book_title': info_for_quote.book_title,
            'quote': info_for_quote.quote
        }
    }


def creates_a_quote_object(quote_data, quote_id):
    """Возвращает цитату в виде объекта"""
    quote_info = quote_data['quote']
    user_id = Users.query.filter_by(token=quote_data['token']).first().user_id
    return Quote(user_id=user_id, quote_id=quote_id,  author=quote_info['author'],
                 book_title=quote_info['book_title'], quote=quote_info['quote'])
