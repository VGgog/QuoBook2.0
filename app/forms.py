from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    """Форма аутентификации пользователя"""
    email = StringField(validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    """Форма регистрации нового пользователя"""
    email = StringField(validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Password"})
    password2 = PasswordField(validators=[DataRequired(), EqualTo('password')],
                              render_kw={"placeholder": "Repeat password"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')


class AuthForm(FlaskForm):
    """Форма для получения токена"""
    email = StringField(validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Получить токен')

