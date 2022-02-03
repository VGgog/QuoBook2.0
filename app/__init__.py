from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = "Чтобы получить доступ к этой странице, Вам надо авторизоваться."
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['JSON_AS_ASCII'] = False


from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')


from app import models
from app.routes import user, quote
