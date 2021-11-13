from werkzeug.security import generate_password_hash
from app.models import Quote, Users
from app import app, db
import unittest
import json

"""Тестирование функций send_all_quote_id_which_add_user(), add_or_change_quote()"""


class SendQuoteTestCase(unittest.TestCase):
    """Тестирование функции send_all_quote_id_which_add_user()"""
    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:fqlfh2004@localhost:5432/QuoBookTest"

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
        db.session.add(Users(user_id=1, username='monoliza', password_hash=generate_password_hash('igrauchu'),
                             token='sfgasgasgasgdasgf'))
        db.session.add(Users(user_id=2, username='monoliza45', password_hash=generate_password_hash('igrauchu123'),
                             token='dsgsdfdsfs'))
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_send_all_quote_id_which_add_user(self):
        """Тестирование функции send_all_quote_id_which_add_user()"""
        token = Users.query.filter_by(username='monoliza').first().token
        response = self.tester.post('/api/all_quotes', data=json.dumps({
            'token': token}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(3, len(json_response))

    def test_send_all_quote_id_which_add_user_error(self):
        """Тестирование функции send_all_quote_id_which_add_user()"""
        token = Users.query.filter_by(username='monoliza45').first().token
        response = self.tester.post('/api/all_quotes', data=json.dumps({
            'token': token}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual('You not add quotes', response.get_data(as_text=True))

    def test_send_all_quote_id_which_add_user_error2(self):
        """Тестирование функции send_all_quote_id_which_add_user()"""
        response = self.tester.post('/api/all_quotes')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_send_all_quote_id_which_add_user_error3(self):
        """Тестирование функции send_all_quote_id_which_add_user()"""
        response = self.tester.post('/api/all_quotes', data=json.dumps({
            'token': 'skdjvkpasdvvkpasd'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))


class AddOrChangeQuoteTest(unittest.TestCase):
    """Тестирование функции add_or_change_quote()"""
    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:fqlfh2004@localhost:5432/QuoBookTest"

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

    def test_add_or_change_quote(self):
        """Тестирование функции add_or_change_quote()"""
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

    def test_add_or_change_quote_error(self):
        """Тестирование функции add_or_change_quote(), когда json не отправлен"""
        response = self.tester.post('/api/new_quote')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_add_or_change_quote_error2(self):
        """Тестирование функции add_or_change_quote(), когда токена нет в базе данных"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'дымыфлмтфыл',
                                    'quote': {'author': 'Франц Кафка',
                                              'book_title': 'Письма к Фелиции',
                                              'quote': 'Если не удается сойтись поближе, люди расходятся подальше.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual('Token is incorrect', response.get_data(as_text=True))

    def test_add_or_change_quote_error3(self):
        """Тестирование функции add_or_change_quote(), когда цитата уже добавлена"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'sfgasgasgasgdasgf',
                                    'quote': {'author': 'Эрих Мария Ремарк',
                                              'book_title': 'Ночь в Лиссабоне',
                                              'quote': 'Она еще не сдалась, но уже не боролась.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual('This quote already added.', response.get_data(as_text=True))

    def test_add_or_change_quote2(self):
        """Тестирование функции add_or_change_quote()"""
        response = self.tester.post('/api/new_quote?quote_id=3', data=json.dumps({'token': 'sfgasgasgasgdasgf',
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

    def test_add_or_change_quote_error4(self):
        """Тестирование функции add_or_change_quote(), пользователь не имеет прав изменять эту цитату"""
        response = self.tester.post('/api/new_quote?quote_id=3', data=json.dumps({'token': 'dsgsdfdsfs',
                                    'quote': {'author': 'Франц Кафка',
                                              'book_title': 'Письма к Фелиции',
                                              'quote': 'Если не удается сойтись поближе, люди расходятся подальше.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual('You do not have permission to update this quote.', response.get_data(as_text=True))

    def test_add_or_change_quote_error5(self):
        """Тестирование функции add_or_change_quote(), когда токена нет в базе данных"""
        response = self.tester.post('/api/new_quote', data=json.dumps({
                                    'quote': {'author': 'Франц Кафка',
                                              'book_title': 'Письма к Фелиции',
                                              'quote': 'Если не удается сойтись поближе, люди расходятся подальше.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_add_or_change_quote_error6(self):
        """Тестирование функции add_or_change_quote(), когда quote нет в базе данных"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'dsgsdfdsfs'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_add_or_change_quote_error7(self):
        """Тестирование функции add_or_change_quote(), когда quote['author'] нет в базе данных"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'dsgsdfdsfs',
                                    'quote': {'book_title': 'Письма к Фелиции',
                                              'quote': 'Если не удается сойтись поближе, люди расходятся подальше.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_add_or_change_quote_error8(self):
        """Тестирование функции add_or_change_quote(), когда quote['book_title'] нет в базе данных"""
        response = self.tester.post('/api/new_quote', data=json.dumps({'token': 'dsgsdfdsfs',
                                    'quote': {'author': 'Франц Кафка',
                                              'quote': 'Если не удается сойтись поближе, люди расходятся подальше.'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_add_or_change_quote_error9(self):
        """Тестирование функции add_or_change_quote(), когда quote['quote'] нет в базе данных"""
        response = self.tester.post('/api/new_quote?quote_id=3', data=json.dumps({'token': 'dsgsdfdsfs',
                                    'quote': {'author': 'Франц Кафка',
                                              'book_title': 'Письма к Фелиции'}}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form of the submitted json is not correct.', response.get_data(as_text=True))


class DelQuoteTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:fqlfh2004@localhost:5432/QuoBookTest"

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

    def test_successful_del_quote(self):
        response = self.tester.delete('/api/del_quote/3', data=json.dumps({'token': 'sfgasgasgasgdasgf'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('user_id', json_response)
        self.assertIn('quote_id', json_response)
        self.assertIn('quote', json_response)
        self.assertIn('author', json_response['quote'])
        self.assertIn('book_title', json_response['quote'])
        self.assertIn('quote', json_response['quote'])

    def test_del_quote_error(self):
        response = self.tester.delete('/api/del_quote/3')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form or the token of the submitted json is not correct.', response.get_data(as_text=True))

    def test_del_quote_error2(self):
        response = self.tester.delete('/api/del_quote/3', data=json.dumps({'token': 'csvlv jsjgkgjsld'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form or the token of the submitted json is not correct.', response.get_data(as_text=True))

    def test_del_quote_error3(self):
        response = self.tester.delete('/api/del_quote/3', data=json.dumps({'token': 'dsgsdfdsfs'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual('You do not have permission to delete this quote.', response.get_data(as_text=True))

    def test_del_quote_error4(self):
        response = self.tester.delete('/api/del_quote/3', data=json.dumps({'author': 'dsgsdfdsfs'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form or the token of the submitted json is not correct.', response.get_data(as_text=True))

    def test_del_quote_error5(self):
        response = self.tester.delete('/api/del_quote/fg', data=json.dumps({'token': 'dsgsdfdsfs'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 404)
