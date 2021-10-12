from app import app
from flask import render_template
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
    return render_template('registration.html', title='Registration', form=login)
