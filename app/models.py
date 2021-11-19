from app import db
from flask_login import UserMixin
from app import login


class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String, index=True, unique=True)
    token = db.Column(db.Text)

    def __repr__(self):
        return "User {}".format(self.email)


class Quote(db.Model):
    __tablename__ = 'quotes'

    user_id = db.Column(db.Integer, index=True)
    quote_id = db.Column(db.Integer, primary_key=True, unique=True)
    author = db.Column(db.String, index=True)
    book_title = db.Column(db.String, index=True)
    quote = db.Column(db.String, index=True)

    def __repr__(self):
        return "Quote_id: {}".format(self.quote_id)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
