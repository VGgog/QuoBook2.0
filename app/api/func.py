# Модуль для работы с функциями

from app.models import Users, Quote
from werkzeug.security import check_password_hash


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
        return check_password_hash(Users.query.filter_by(username=quote_data['login']).first().password_hash,
                                   quote_data['password'])
    return False


def checking_correctness_json(quote_data):
    """Проверяет правильность отправленного json"""
    return ('token' and 'quote' in quote_data) and ('author' and 'book_title' and 'quote' in quote_data['quote'])


def made_quote_obj(quote_data, quote_id):
    """Возвращает цитату в виде объекта"""
    quote_info = quote_data['quote']
    user_id = Users.query.filter_by(token=quote_data['token']).first().user_id
    return Quote(user_id=user_id, quote_id=quote_id,  author=quote_info['author'],
                 book_title=quote_info['book_title'], quote=quote_info['quote'])


def check_user_id_and_quote_user_id(token, quote_id):
    """Проверяет user_id цитаты и user_id логина который отправили в запросе."""
    return Users.query.filter_by(token=token).first().user_id == Quote.query.get_or_404(quote_id).user_id


def checking_correct_json2(quote_data):
    """Проверяет наличие нужных полей в отправленном json-файле"""
    return 'login' and 'password' in quote_data


def check_token(token):
    """Проверяет наличие токена в базе данных"""
    return Users.query.filter_by(token=token).first()


def check_correctness_json_with_token(quote_data):
    """Проверяет наличие токена в json и наличие токена в бд"""
    return ('token' in quote_data) and (Users.query.filter_by(token=quote_data.get('token')).first())
