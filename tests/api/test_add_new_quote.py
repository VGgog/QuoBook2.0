from tests.config import TEST_SQLALCHEMY_DATABASE_URI
from werkzeug.security import generate_password_hash
from app.models import Quote, Users
from app import app, db
import unittest
import json

"""Тестирование функции add_new_quote()"""


class AddNewQuoteTest(unittest.TestCase):
    """Тестирование функции add_new_quote()"""
    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI

        quote3 = Quote(user_id=1, quote_id=3,
                       author='Эрих Мария Ремарк', book_title='Ночь в Лиссабоне',
                       quote='Она еще не сдалась, но уже не боролась.')
        db.session.add(quote3)
        db.session.add(Users(user_id=1, username='monoliza', password_hash=generate_password_hash('igrauchu'),
                             token='sfgasgasgasgdasgf'))
        db.session.add(Users(user_id=2, username='monoliza45', password_hash=generate_password_hash('igrauchu123'),
                             token='dsgsdfdsfs'))
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_new_quote(self):
        """Тестирование функции add_new_quote()"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'sfgasgasgasgdasgf',
                                    'quote': {'author': 'Франц Кафка',
                                              'book_title': 'Письма к Фелиции',
                                              'quote': 'Если не удается сойтись поближе, люди расходятся подальше.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('user_id', json_response)
        self.assertIn('quote_id', json_response)
        self.assertIn('quote', json_response)
        self.assertIn('author', json_response['quote'])
        self.assertIn('book_title', json_response['quote'])
        self.assertIn('quote', json_response['quote'])

    def test_add_new_quote_error(self):
        """Тестирование функции add_or_change_quote(), пользователь не отправил данные цитаты"""
        response = self.tester.post('/api/new_quote')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_add_new_quote_error2(self):
        """Тестирование функции add_new_quote(), токена нет в базе данных"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'дымыфлмтфыл',
                                    'quote': {'author': 'Франц Кафка',
                                              'book_title': 'Письма к Фелиции',
                                              'quote': 'Если не удается сойтись поближе, люди расходятся подальше.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual('Token is incorrect', response.get_data(as_text=True))

    def test_add_new_quote_error3(self):
        """Тестирование функции add_new_quote(), когда цитата уже добавлена"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'sfgasgasgasgdasgf',
                                    'quote': {'author': 'Эрих Мария Ремарк',
                                              'book_title': 'Ночь в Лиссабоне',
                                              'quote': 'Она еще не сдалась, но уже не боролась.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual('This quote already added.', response.get_data(as_text=True))

    def test_add_new_quote_error4(self):
        """Тестирование функции add_new_quote(), когда токена нет в отправленных данных"""
        response = self.tester.post('/api/new_quote', data=json.dumps({
                                    'quote': {'author': 'Франц Кафка',
                                              'book_title': 'Письма к Фелиции',
                                              'quote': 'Если не удается сойтись поближе, люди расходятся подальше.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_add_new_quote_error5(self):
        """Тестирование функции add_new_quote(), когда quote нет в отправленных данных"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'dsgsdfdsfs'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_add_new_quote_error6(self):
        """Тестирование функции add_new_quote(), когда quote['author'] нет в отправленных данных"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'dsgsdfdsfs',
                                    'quote': {'book_title': 'Письма к Фелиции',
                                              'quote': 'Если не удается сойтись поближе, люди расходятся подальше.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_add_new_quote_error7(self):
        """Тестирование функции add_new_quote(), когда quote['book_title'] нет в отправленных данных"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'dsgsdfdsfs',
                                    'quote': {'author': 'Франц Кафка',
                                              'quote': 'Если не удается сойтись поближе, люди расходятся подальше.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_add_new_quote_error8(self):
        """Тестирование функции add_new_quote(), когда quote['quote'] нет в отправленных данных"""
        response = self.tester.post('/api/new_quote?quote_id=3', data=json.dumps({'token': 'dsgsdfdsfs',
                                    'quote': {'author': 'Франц Кафка',
                                              'book_title': 'Письма к Фелиции'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
