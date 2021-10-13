from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm


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
        flash('Вы успешно зарегистрировались.')
        return redirect('/registration')
    return render_template('registration.html', title='Registration', form=login)
