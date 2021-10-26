from app import app, db
from flask import render_template, flash, redirect, url_for
import app.forms as forms
from app.models import Users
from app import passwords


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
        if Users.query.filter_by(username=login.username.data).first():
            flash('Пользователь под таким логином уже существует.')
            return redirect(url_for('reg'))

        if not login.password.data == login.password2.data:
            flash('Пароли не совпадают.')
            return redirect(url_for('reg'))

        user = Users(user_id=Users.query.count() + 1, username=login.username.data,
                     password_hash=passwords.make_password_hash(login.password.data), token=passwords.generate_token())
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
        pass
    return render_template('token.html', title='token', form=login)


@app.route('/delete_profile', methods=['GET', 'POST'])
def delete_profile():
    """Страница удаления профиля"""
    login = forms.DeleteForm()
    if login.validate_on_submit():
        pass
    return render_template('delete.html', title='delete profile', form=login)
