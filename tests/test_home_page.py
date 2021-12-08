from app import app
import unittest


class HomePageTest(unittest.TestCase):

    def test_page(self):
        self.tester = app.test_client()
        response = self.tester.get('/home')
        self.assertEqual(response.status_code, 200)
