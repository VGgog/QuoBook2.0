from app.models import Users, Quote
from werkzeug.security import check_password_hash


def user_and_quote_user_id(token, quote_id):
    """Проверяет user_id цитаты и user_id логина который отправили в запросе."""
    return Users.query.filter_by(token=token).first().id == Quote.query.get_or_404(quote_id).user_id


def token_in_db(token):
    """Проверяет наличие токена в базе данных"""
    return Users.query.filter_by(token=token).first()


def token_in_json(quote_data):
    """Проверяет наличие токена в json"""
    return 'token' in quote_data


def user_login_and_password(quote_data):
    """Производит проверку, зарегистрирован ли пользователь, и правильность введённого пароля"""
    if Users.query.filter_by(email=quote_data['email']).first():
        return check_password_hash(Users.query.filter_by(email=quote_data['email']).first().password_hash,
                                   quote_data['password'])
    return False


def correct_form_sent_json(quote_data):
    """Проверяет правильность отправленного json"""
    return ('token' in quote_data) and ('quote' in quote_data) and (('author' in quote_data['quote'])
                                                                    and ('book_title' in quote_data['quote'])
                                                                    and ('quote' in quote_data['quote']))


def email_and_password_in_sent_json(quote_data):
    """Проверяет наличие нужных полей в отправленном json-файле"""
    return 'email' in quote_data and 'password' in quote_data
