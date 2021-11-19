from tests.test_db_config import TEST_SQLALCHEMY_DATABASE_URI
from werkzeug.security import generate_password_hash
from app.models import Quote, Users
from app import app, db
import unittest
import json

"""Тестирование функции delete_quote()"""


class DelQuoteTestCase(unittest.TestCase):
    """Тестирование функции delete_quote()"""
    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI

        quote3 = Quote(user_id=1, quote_id=3,
                       author='Эрих Мария Ремарк', book_title='Ночь в Лиссабоне',
                       quote='Она еще не сдалась, но уже не боролась.')
        db.session.add(quote3)
        db.session.add(Users(id=1, email='monoliza@google.com', password_hash=generate_password_hash('igrauchu'),
                             token='sfgasgasgasgdasgf'))
        db.session.add(Users(id=2, email='monoliza45@google.com', password_hash=generate_password_hash('igrauchu123'),
                             token='dsgsdfdsfs'))
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_delete_quote(self):
        """Тестирование функции delete_quote()"""
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

    def test_delete_quote_error(self):
        """Тестирование функции delete_quote(), пользователь не отправил данные токена"""
        response = self.tester.delete('/api/del_quote/3')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form or the token of the submitted json is not correct.', response.get_data(as_text=True))

    def test_delete_quote_error2(self):
        """Тестирование функции delete_quote(), пользователь отправил несуществующий токен"""
        response = self.tester.delete('/api/del_quote/3', data=json.dumps({'token': 'csvlv jsjgkgjsld'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form or the token of the submitted json is not correct.', response.get_data(as_text=True))

    def test_delete_quote_error3(self):
        """Тестирование функции delete_quote(), данный пользователь не имеет право удалить цитату"""
        response = self.tester.delete('/api/del_quote/3', data=json.dumps({'token': 'dsgsdfdsfs'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual('You do not have permission to delete this quote.', response.get_data(as_text=True))

    def test_delete_quote_error4(self):
        """Тестирование функции delete_quote(), отправил данные без токена"""
        response = self.tester.delete('/api/del_quote/3', data=json.dumps({'author': 'dsgsdfdsfs'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual('The form or the token of the submitted json is not correct.', response.get_data(as_text=True))

    def test_delete_quote_error5(self):
        """Тестирование функции delete_quote(), цитата не найдена"""
        response = self.tester.delete('/api/del_quote/fg', data=json.dumps({'token': 'dsgsdfdsfs'}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()