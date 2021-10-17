

def translates_into_the_correct_format(info_for_quote):
    """Переводит цитату в правильный формат"""
    return {
        'user_id': info_for_quote['user_id'],
        'quote_id': info_for_quote['quote_id'],
        'quote': {
            'author': info_for_quote['author'],
            'book_title': info_for_quote['book_title'],
            'quote': info_for_quote['quote']
        }
    }
