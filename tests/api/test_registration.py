from werkzeug.security import generate_password_hash
from app.models import Users
from app import app, db
import unittest
import json

'''
Тестирование функции регистрации пользователя по api
Тестируется функция registration_new_user() в модуле quotes 
'''


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:fqlfh2004@localhost:5432/QuoBookTest"
        
        # Добавляет пользователя в бд, для проведения теста в методе test_login_in_exists()
        db.session.add(Users(user_id=1, username='monoliza', password_hash=generate_password_hash('igrauchu')))
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful(self):
        """Успешная регистрация"""
        response = self.tester.post('/api/registration', data=json.dumps({
            'login': 'papatola', 'password': 'pororo'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('You have successful registered', response.get_data(as_text=True))

    def test_json_without_login(self):
        """Регистрация, когда отправленный json без логина"""
        response = self.tester.post('/api/registration', data=json.dumps({
            'password': 'pororo'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_json_without_password(self):
        """Отправленный json без пароля"""
        response = self.tester.post('/api/registration', data=json.dumps({
            'login': 'papatola'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('The form of the submitted json is not correct.', response.get_data(as_text=True))

    def test_login_in_exists(self):
        """Проверяет поведение программы, если login уже есть в бд"""
        response = self.tester.post('/api/registration', data=json.dumps({
            'login': 'monoliza', 'password': 'igrauchu'}), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('A user with this username already exists', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()