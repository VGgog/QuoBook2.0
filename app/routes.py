from app import app, db
from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import app.forms as forms
from app.models import Users, Quote
from app import generate_token
from wtforms.validators import ValidationError


@app.route('/')
@app.route('/home')
def home():
    """Возвращает страницу home"""
    return render_template('home.html', title='Home')


@app.route('/documentation')
def docs():
    """Возвращает страницу с документацией"""
    return render_template('documentation.html', title='Documentation')


@app.route('/registration', methods=['GET', 'POST'])
def reg():
    """Возвращает страницу с регистрацией"""
    login = forms.RegistrationForm()
    if login.validate_on_submit():
        if Users.query.filter_by(email=login.email.data).first():
            flash('Пользователь c таким email-адресом уже существует.')
            return redirect(url_for('reg'))

        user = Users(user_id=Users.query.count() + 1, email=login.email.data,
                     password_hash=generate_password_hash(login.password.data),
                     token=generate_token.generate_token())
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались.')
        return redirect(url_for('get_token'))
    return render_template('registration.html', title='registration', form=login)


@app.route('/token', methods=['GET', 'POST'])
def get_token():
    """Страница получения токена"""
    login = forms.LoginForm()
    if login.validate_on_submit():
        if not Users.query.filter_by(email=login.username.data).first():
            flash('Такой логин не зарегистрирован.')
            return redirect(url_for('get_token'))

        if not check_password_hash(Users.query.filter_by(email=login.username.data).first().password_hash,
                                   login.password.data):
            flash('Пароль не верный.')
            return redirect(url_for('get_token'))

        flash(f'Ваш токен: {Users.query.filter_by(email=login.username.data).first().token}')
        return redirect(url_for('get_token'))
    return render_template('token.html', title='token', form=login)


@app.route('/delete_profile', methods=['GET', 'POST'])
def delete_profile():
    """Страница удаления профиля"""
    login = forms.DeleteForm()
    if login.validate_on_submit():
        if not Users.query.filter_by(email=login.username.data).first():
            flash('Такой логин не зарегистрирован.')
            return redirect(url_for('delete_profile'))

        if not check_password_hash(Users.query.filter_by(email=login.username.data).first().password_hash,
                                   login.password.data):
            flash('Пароль не верный.')
            return redirect(url_for('delete_profile'))

        user = Users.query.filter_by(email=login.username.data).first()

        # Все user_id цитат который добавил этот пользователь, меняются на 1(user_id админа)
        for user_id in Quote.query.filter_by(user_id=user.user_id):
            user_id.user_id = 1
            db.session.commit()

        db.session.delete(user)
        db.session.commit()
        flash('Профиль удалён.')
        return redirect(url_for('delete_profile'))
    return render_template('delete.html', title='delete profile', form=login)
