from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.models import Users


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/documentation')
def docs():
    return render_template('documentation.html', title='Documentation')


@app.route('/registration', methods=['GET', 'POST'])
def reg():
    login = LoginForm()
    if login.validate_on_submit():
        if Users.query.filter_by(username=login.username.data).first():
            flash('Пользователь под таким логином уже существует.')
            return redirect(url_for('reg'))
        
        user = Users(user_id=Users.query.count() + 1, username=login.username.data,
                     password_hash=Users.make_password_hash(login.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались.')
        return redirect(url_for('reg'))
    return render_template('registration.html', title='Registration', form=login)
