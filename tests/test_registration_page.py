from .test_db_config import TEST_SQLALCHEMY_DATABASE_URI
from werkzeug.security import generate_password_hash
from app.models import Users
from app import app, db
import unittest


"""
Тесты страницы /registration.
Тесты проверяют только то, чтобы сайт не выдал статусный код кроме 200, но не какие сообщения выдаёт сайт, 
и логику backend. 
"""


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI

        # Добавляет пользователя в бд, для проведения теста в методе test_login_in_exists()
        db.session.add(Users(id=1, email='monoliza@google.com', password_hash=generate_password_hash('igrauchu')))
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful_registration(self):
        """Тест страницы /registration"""
        response = self.tester.get('/registration')
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        """Успешная регистрация"""
        response = self.tester.get('/registration', data={'email': 'papa@gmail.com', 'password': 'papa14',
                                                          'password2': 'papa14'})
        self.assertEqual(response.status_code, 200)

    def test_registration2(self):
        """Вывод ошибки когда пользователь под таким email уже существует."""
        response = self.tester.get('/registration', data={'email': 'monoliza@google.com', 'password': 'papa14',
                                                          'password2': 'papa14'})
        self.assertEqual(response.status_code, 200)

    def test_registration3(self):
        """Вывод ошибки когда пользователь ввёл не одинаковые пароли."""
        response = self.tester.get('/registration', data={'email': 'papa@gmail.com', 'password': 'papa14',
                                                          'password2': 'mamavmayami'})
        self.assertEqual(response.status_code, 200)
