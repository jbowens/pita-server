import unittest, sys, os

sys.path.append(os.path.dirname(__file__) + '/..')

from mylittlepita import app

class EndpointTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_true(self):
        assert True

    if __name__ == '__main__':
        unittest.main()
