import random
from app import app, db
from flask import render_template, flash, redirect, url_for
import app.forms as forms
from app.models import Users, Quote
from flask_login import current_user, login_required


@app.route('/quote', methods=['GET', 'POST'])
def get_a_quote():
    """Страница получения цитат"""
    quote_data = forms.GetQuoteForm()
    if quote_data.validate_on_submit():
        author = quote_data.author.data
        book_title = quote_data.book_title.data

        if quote_data.quote_id.data:
            quote = Quote.query.filter_by(quote_id=quote_data.quote_id.data).first()
            if quote:
                return render_template('get_quote.html', title='Quote', form=quote_data, quote_info=quote)
        elif author or book_title:
            if author and book_title:
                quote = Quote.query.filter_by(author=author, book_title=book_title).first()
                if quote:
                    return render_template('get_quote.html', title='Quote', form=quote_data, quote_info=quote)
            if author:
                quote = Quote.query.filter_by(author=author).first()
                if quote:
                    return render_template('get_quote.html', title='Quote', form=quote_data, quote_info=quote)
            if book_title:
                quote = Quote.query.filter_by(book_title=book_title).first()
                if quote:
                    return render_template('get_quote.html', title='Quote', form=quote_data, quote_info=quote)
        else:
            quote_id = random.randrange(1, Quote.query.count())
            quote = Quote.query.filter_by(quote_id=quote_id).first()
            return render_template('get_quote.html', title='Quote', form=quote_data, quote_info=quote)

        flash("Цитата не найдена.")
        return redirect(url_for('get_a_quote'))
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
@login_required
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
