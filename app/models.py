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

    def __repr__(self):
        return "User {}".format(self.username)


