import os


class Config:
    SECRET_KEY = os.environ.get('MY_SECRET_KEY') or 'try_to_guess_password'
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://') or
                               "postgresql://postgres:fqlfh2004@localhost:5432/QuoBook2.0")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "smtp.googlemail.com"
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "gluhovkich@gmail.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "kigvspyvpehmsjyz"
    ADMINS = ["gluhovkich@gmail.com"]
