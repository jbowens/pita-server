import unittest, sys, os, random

sys.path.append(os.path.dirname(__file__) + '/..')

def random_word(length):
       return ''.join(random.choice(string.lowercase) for i in range(length))
def random_phone():
       return ''.join(random.choice(string.digits) for i in range(11))

from mylittlepita import app

class EndpointTestCase(unittest.TestCase):
 
    def rand_account(self):
        """
        Creates a random account for testing.
        """
        rv = self.app.post('/accounts/new', data = {
            'name': 'Test Account',
            'email': random_word(8) + '@' + random_word(10) + '.' + random_word(3)
        })
        return json.loads(rv.data)

    def n_rand_accounts(self, n):
        """
        Creates a list of n random accounts.
        """
        return [self.random_account() for x in range(n)]
   
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_true(self):
        assert True

    if __name__ == '__main__':
        unittest.main()
