import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_indicadores_valid_request(self):
        # Test a valid request to the /indicadores route
        response = self.app.get('/indicadores/USD/BRL/5')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('moeda1', data)
        self.assertIn('moeda2', data)
        self.assertIn('ask', data)

    def test_indicadores_invalid_currency(self):
        # Test an invalid currency request
        response = self.app.get('/indicadores/INVALID/BRL/5')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('erro', data)

    def test_indicadores_invalid_days(self):
        # Test an invalid number of days
        response = self.app.get('/indicadores/USD/BRL/0')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('erro', data)

if __name__ == '__main__':
    unittest.main()

