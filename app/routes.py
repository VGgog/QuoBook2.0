from app import app
from flask import render_template


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/documentation')
def docs():
    return render_template('documentation.html', title='Documentation')


@app.route('/registration')
def reg():
    return render_template('registration.html', title='Registration')
