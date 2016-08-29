import unittest

from app import get_app


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = get_app(dict(
            MONGO_DBNAME='coffee_advisor_test'
        ))
        self.app.config['TESTING'] = True
        self.app = self.app.test_client()

    def tearDown(self):
        pass

    def test_empty_db(self):
        rv = self.app.get('/api/places')
        print rv.data
        assert '[]' == rv.data


if __name__ == '__main__':
    unittest.main()
