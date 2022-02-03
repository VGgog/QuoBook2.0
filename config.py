import os


class Config:
    SECRET_KEY = os.environ.get('MY_SECRET_KEY') or "my-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
