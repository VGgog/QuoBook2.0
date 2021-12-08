from tests.test_db_config import TEST_SQLALCHEMY_DATABASE_URI
from werkzeug.security import generate_password_hash
from app import generate_token
from app.models import Users
from app import app, db
import unittest


"""
Тест страницы /documentation
Тесты проверяют только то, чтобы сайт не выдал статусный код кроме 200, но не какие сообщения выдаёт сайт, 
и логику backend.
"""


class DocumentationPageTest(unittest.TestCase):

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

    def test_page_documentation(self):
        """Тест страницы /documentation"""
        response = self.tester.get('/documentation')
        self.assertEqual(response.status_code, 200)

    def test_documentation_successful(self):
        """Успешная авторизация"""
        response = self.tester.get('/documentation', data={'email': 'monoliza@google.com', 'password': 'igrauchu'})
        self.assertEqual(response.status_code, 200)

    def test_documentation1(self):
        """Пользователь ввёл логин, которого нет в бд"""
        response = self.tester.get('/documentation', data={'email': 'papa@mail.com', 'password': 'igrauchu'})
        self.assertEqual(response.status_code, 200)

    def test_documentation2(self):
        """Пользователь отправил неверный пароль"""
        response = self.tester.get('/documentation', data={'email': 'monoliza@google.com', 'password': 'failpassword'})
        self.assertEqual(response.status_code, 200)
