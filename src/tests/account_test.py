from endpoint_testcase import EndpointTestCase

class AccountsTestCase(EndpointTestCase):

    def test_new_account(self):
        rv = self.app.post('/accounts/new', data={
                'name': 'Jackson',
                'phone': 14402892895,
                'email': 'jackson_owens@brown.edu'
            }, follow_redirects=True)
        assert 'aid' in rv.data
        assert 'key' in rv.data
