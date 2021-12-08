from tests.test_db_config import TEST_SQLALCHEMY_DATABASE_URI
from werkzeug.security import generate_password_hash
from app import generate_token
from app.models import Users
from app import app, db
import unittest


"""
Тест страницы /login
Тесты проверяют только то, чтобы сайт не выдал статусный код кроме 200, но не какие сообщения выдаёт сайт, 
и логику backend.
"""


class UserLoginTest(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI
        db.session.add(Users(id=1, email='monoliza@google.com', password_hash=generate_password_hash('igrauchu'),
                             token=generate_token.generate_token()))
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_page_login(self):
        """Тест страницы /login"""
        response = self.tester.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_successful(self):
        """Успешная авторизация"""
        response = self.tester.get('/login', data={'email': 'monoliza@google.com', 'password': 'igrauchu'})
        self.assertEqual(response.status_code, 200)

    def test_login1(self):
        """Пользователь ввёл логин, которого нет в бд"""
        response = self.tester.get('/login', data={'email': 'papa@mail.com', 'password': 'igrauchu'})
        self.assertEqual(response.status_code, 200)

    def test_login2(self):
        """Пользователь отправил неверный пароль"""
        response = self.tester.get('/login', data={'email': 'monoliza@google.com', 'password': 'failpassword'})
        self.assertEqual(response.status_code, 200)
