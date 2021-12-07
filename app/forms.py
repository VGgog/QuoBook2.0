from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Optional


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


class AddQuoteForm(FlaskForm):
    """Форма добавления цитаты"""
    author = StringField(validators=[DataRequired()], render_kw={"placeholder": "Автор"})
    book_title = StringField(validators=[DataRequired()], render_kw={"placeholder": "Название книги"})
    quote = TextAreaField(validators=[DataRequired()], render_kw={"placeholder": "Цитата", "rows": 10, "cols": 39})
    add_quote = SubmitField('Добавить цитату')


class DelQuoteForm(FlaskForm):
    """Форма удаления цитаты"""
    quote_id = IntegerField(validators=[DataRequired()], render_kw={"placeholder": "ID цитаты"})
    del_quote = SubmitField('Удалить цитату')


class GetQuoteForm(FlaskForm):
    """Форма получения цитат"""
    quote_id = IntegerField(validators=[Optional()], render_kw={"placeholder": "ID цитаты"})
    author = StringField(render_kw={"placeholder": "Автор"})
    book_title = StringField(render_kw={"placeholder": "Название книги"})
    get_quote = SubmitField('Получить цитату')
