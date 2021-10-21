# Модуль для работы с функциями

from app.models import Users, Quote


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


def made_quote_obj(quote_data, quote_id):
    """Возвращает цитату в виде объекта"""
    quote_info = quote_data['quote']
    user_id = Users.query.filter_by(username=quote_data['login']).first().user_id
    return Quote(user_id=user_id, quote_id=quote_id,  author=quote_info['author'],
                 book_title=quote_info['book_title'], quote=quote_info['quote'])


def check_user_id_and_quote_user_id(quote_data, quote_id):
    """Проверяет user_id цитаты и user_id логина который отправили в запросе."""
    quote = Quote.query.get_or_404(quote_id)

    if Users.query.filter_by(username=quote_data['login']).first().user_id == quote.user_id:
        return True

    return False
