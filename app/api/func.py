# Модуль для работы с функциями

from app.models import Users


def translates_into_the_correct_format(info_for_quote):
    """Переводит цитату в правильный формат"""
    return {
        'user_id': info_for_quote.user_id,
        'quote_id': info_for_quote.quote_id,
        'quote': {
            'author': info_for_quote.author,
            'book_title': info_for_quote.book_title,
            'quote': info_for_quote.quote
        }
    }


def check_user(quote_data):
    """Производит проверку, зарегистрирован ли пользователь, и правильность введённого пароля"""
    if Users.query.filter_by(username=quote_data['login']).first():

        password_hash = Users.query.filter_by(username=quote_data['login']).first().password_hash
        if Users.check_password(password_hash, quote_data['password']):
            return True

    return False


def checking_correctness_json(quote_data):
    """Проверяет правильность отправленного json"""
    if 'login' and 'password' and 'quote' in quote_data:
        info_for_quote = quote_data['quote']
        if 'author' and 'book_title' and 'quote' in info_for_quote:
            return True

    return False

