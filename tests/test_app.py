from app import app
import unittest


class BasicTestCase(unittest.TestCase):

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_docs(self):
        tester = app.test_client(self)
        response = tester.get('/documentation')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()