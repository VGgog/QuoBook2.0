from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String, index=True, unique=True)

    def make_password_hash(password):
        """Создаёт хэш пароля"""
        return generate_password_hash(password)

    def check_password(password_hash, password):
        """"""
        return check_password_hash(password_hash, password)

    def __repr__(self):
        return "User {}".format(self.username)


class Quote(db.Model):
    __tablename__ = 'quotes'

    user_id = db.Column(db.Integer, index=True)
    quote_id = db.Column(db.Integer, primary_key=True, unique=True)
    author = db.Column(db.String, index=True)
    book_title = db.Column(db.String, index=True)
    quote = db.Column(db.String, index=True)

