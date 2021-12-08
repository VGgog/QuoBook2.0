from .test_db_config import TEST_SQLALCHEMY_DATABASE_URI
from app.models import Quote
from app import app, db
import unittest


"""
Тесты страницы /quote
Тесты проверяют только то, чтобы сайт не выдал статусный код кроме 200, но не какие сообщения выдаёт сайт, 
и логику backend. 
"""


class GetQuotePageTest(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI

        quote = Quote(user_id=1, quote_id=1,
                      author='Рэй Брэдбери', book_title='Вино из одуванчиков',
                      quote='Что хочешь помнить, то всегда помнишь.')
        db.session.add(quote)
        quote2 = Quote(user_id=1, quote_id=2,
                       author='Л.Н.Толстой', book_title='Война и мир', quote='Навсегда ничего не бывает.')
        db.session.add(quote2)
        quote3 = Quote(user_id=1, quote_id=3,
                       author='Эрих Мария Ремарк', book_title='Ночь в Лиссабоне',
                       quote='Она еще не сдалась, но уже не боролась.')
        db.session.add(quote3)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_send_quote_page(self):
        """Тест страницы получения цитаты"""
        response = self.tester.get('/quote')
        self.assertEqual(response.status_code, 200)

    def test_send_random_quote(self):
        """Если пользователь не заполнил ни одной формы, отправляется случайная цитата"""
        response = self.tester.post('/quote', data={'quote_id': None, 'author': None, 'book_title': None})
        self.assertEqual(response.status_code, 200)

    def test_send_quote_by_quote_id(self):
        """Пользователь заполнил поле id"""
        response = self.tester.post('/quote', data={'quote_id': 2, 'author': None, 'book_title': None})
        self.assertEqual(response.status_code, 200)

    def test_send_quote_by_quote_id2(self):
        """Пользователь заполнил поле id. id цитаты не найден"""
        response = self.tester.post('/quote', data={'quote_id': 10000, 'author': None, 'book_title': None})
        self.assertEqual(response.status_code, 200)

    def test_send_quote_by_author(self):
        """Пользователь заполнил поле автор"""
        response = self.tester.post('/quote', data={'quote_id': None, 'author': 'Рэй Брэдбери', 'book_title': None})
        self.assertEqual(response.status_code, 200)

    def test_send_quote_by_author2(self):
        """Пользователь заполнил поле автор. Цитата не найдена"""
        response = self.tester.post('/quote', data={'quote_id': None, 'author': 'Мавроди', 'book_title': None})
        self.assertEqual(response.status_code, 200)

    def test_send_quote_by_book_title(self):
        """Пользователь заполнил поле названия книги"""
        response = self.tester.post('/quote', data={'quote_id': None, 'author': None, 'book_title': 'Война и мир'})
        self.assertEqual(response.status_code, 200)

    def test_send_quote_by_book_title2(self):
        """Пользователь заполнил поле названия книги. Цитата не найдена"""
        response = self.tester.post('/quote', data={'quote_id': None, 'author': None, 'book_title': 'Мир и война'})
        self.assertEqual(response.status_code, 200)

    def test_send_quote_by_author_and_book_title(self):
        """Пользователь заполнил поле автор и название книги"""
        response = self.tester.post('/quote', data={'quote_id': None, 'author': 'Эрих Мария Ремарк',
                                                    'book_title': 'Ночь в Лиссабоне'})
        self.assertEqual(response.status_code, 200)

    def test_send_quote_by_author_and_book_title2(self):
        """Пользователь заполнил поле автор и название книги. Цитата не найдена."""
        response = self.tester.post('/quote', data={'quote_id': None, 'author': 'Мавроди',

                                                    'book_title': 'Мир и война'})
        self.assertEqual(response.status_code, 200)
