import random
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
import app.forms as forms
from app.models import Users, Quote
from app import generate_token
from flask_login import logout_user, login_user, current_user, login_required


@app.route('/')
@app.route('/home')
def home():
    """Возвращает страницу home"""
    return render_template('home.html', title='Home')


@app.route('/documentation', methods=['GET', 'POST'])
def docs():
    """Возвращает страницу с документацией к Api"""
    token_form = forms.AuthForm()
    if current_user.is_authenticated:
        # Сразу отображает токен пользователя в поле, если пользователь уже вошёл в систему.
        email = current_user.email
        return render_template('documentation.html', title='Documentation', form=token_form,
                               message=Users.query.filter_by(email=email).first().token)

    if token_form.validate_on_submit():
        user = Users.query.filter_by(email=token_form.email.data).first()
        if not user:
            flash('Вы не зарегистрированы.')
            return redirect(url_for('docs'))

        if not check_password_hash(Users.query.filter_by(email=token_form.email.data).first().password_hash,
                                   token_form.password.data):
            flash('Пароль не верный.')
            return redirect(url_for('docs'))

        message = user.token
        return render_template('documentation.html', title='Documentation', form=token_form, message=message)
    return render_template('documentation.html', title='Documentation', form=token_form)


@app.route('/registration', methods=['GET', 'POST'])
def reg():
    """Возвращает страницу с регистрацией"""
    if current_user.is_authenticated:
        return render_template('after_login.html')
    registration_data = forms.RegistrationForm()
    if registration_data.validate_on_submit():
        if Users.query.filter_by(email=registration_data.email.data).first():
            flash('Пользователь c таким email-адресом уже существует.')
            return redirect(url_for('reg'))

        user = Users(id=Users.query.count() + 1, email=registration_data.email.data,
                     password_hash=generate_password_hash(registration_data.password.data),
                     token=generate_token.generate_token())
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались.')
        login_user(user, remember=registration_data.remember_me.data)
        return render_template('after_login.html')
    return render_template('registration.html', title='registration', form=registration_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница аутентификации"""
    if current_user.is_authenticated:
        return render_template('after_login.html')
    login_data = forms.LoginForm()
    if login_data.validate_on_submit():
        user = Users.query.filter_by(email=login_data.email.data).first()
        if not user:
            flash('Вы не зарегистрированы.')
            return redirect(url_for('login'))

        if not check_password_hash(Users.query.filter_by(email=login_data.email.data).first().password_hash,
                                   login_data.password.data):
            flash('Пароль не верный.')
            return redirect(url_for('login'))

        login_user(user, remember=login_data.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return render_template('after_login.html')
        return redirect(next_page)
    return render_template('login.html', title='login', form=login_data)


@app.route('/quote', methods=['GET', 'POST'])
def get_a_quote():
    """Страница получения цитат"""
    quote_data = forms.GetQuoteForm()
    if quote_data.validate_on_submit():
        if quote_data.quote_id.data:
            quote = Quote.query.filter_by(quote_id=quote_data.quote_id.data).first()
            if quote:
                return render_template('get_quote.html', title='Quote', form=quote_data, quote_info=quote)
            else:
                flash("Цитата не найдена.")
                return redirect(url_for('get_a_quote'))
        else:
            quote_id = random.randrange(1, Quote.query.count())
            quote = Quote.query.filter_by(quote_id=quote_id).first()
            return render_template('get_quote.html', title='Quote', form=quote_data, quote_info=quote)
    return render_template('get_quote.html', title='Quote', form=quote_data)


@app.route('/add_quote', methods=['GET', 'POST'])
@login_required
def add_quote():
    """Страница добавления новых цитат"""
    quote_data = forms.AddQuoteForm()
    if quote_data.validate_on_submit():
        # Проверка на наличие этой цитаты в базу данных
        if Quote.query.filter_by(quote=quote_data.quote.data).first():
            flash('Такая цитата уже добавлена.')
            return redirect(url_for('add_quote'))
        # Добавляет цитату в базу данных
        user_id = Users.query.filter_by(email=current_user.email).first().id
        quote_id = Quote.query.count() + 1
        db.session.add(Quote(user_id=user_id, quote_id=quote_id,  author=quote_data.author.data,
                             book_title=quote_data.book_title.data, quote=quote_data.quote.data))
        db.session.commit()

        flash(f'Цитата добавлена.\nid-цитаты - {quote_id}')
        return redirect(url_for('add_quote'))
    return render_template('add_quote.html', title='Documentation', form=quote_data)


@app.route('/del_quote', methods=['GET', 'POST'])
def del_quote():
    """Страница удаления цитаты"""
    del_quote_data = forms.DelQuoteForm()
    if del_quote_data.validate_on_submit():
        quote_id = del_quote_data.quote_id.data
        quote = Quote.query.filter_by(quote_id=quote_id).first()

        if not quote:
            flash('Цитата не найдена.')
            return redirect(url_for('del_quote'))

        if not quote.user_id == Users.query.filter_by(email=current_user.email).first().id:
            flash('У вас нет доступа удалить данную цитату.')
            return redirect(url_for('del_quote'))

        db.session.delete(quote)
        db.session.commit()
        flash('Цитата удалена.')
        return redirect(url_for('del_quote'))
    return render_template('del_quote.html', title='Удалить цитату', form=del_quote_data)


@app.route('/logout')
def logout():
    """Страница выхода пользователя"""
    logout_user()
    flash('Вы вышли из системы.')
    return redirect(url_for('login'))
