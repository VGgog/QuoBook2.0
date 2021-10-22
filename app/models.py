from app import db


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        return "User {}".format(self.username)


class Quote(db.Model):
    __tablename__ = 'quotes'

    user_id = db.Column(db.Integer, index=True)
    quote_id = db.Column(db.Integer, primary_key=True, unique=True)
    author = db.Column(db.String, index=True)
    book_title = db.Column(db.String, index=True)
    quote = db.Column(db.String, index=True)

    def __repr__(self):
        return "Quote_id: {}".format(self.quote_id)

