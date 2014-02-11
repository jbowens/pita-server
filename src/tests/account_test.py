import json
from endpoint_testcase import EndpointTestCase

class AccountsTestCase(EndpointTestCase):

    def create_account(self, name, phone, email):
        return self.app.post('/accounts/new', data = {
            'name': name,
            'phone': phone,
            'email': email}, follow_redirects=True)

    def test_new_account(self):
        rv = self.create_account('Jackson', '14405554444', 'john@doe.org')
        assert 'aid' in rv.data
        assert 'key' in rv.data
        obj = json.loads(rv.data)
        assert obj['aid'] > 0
        assert len(obj['key']) == 128

    def test_no_name(self):
        rv = self.create_account(None, '15555555555', None)
        assert 'name' in rv.data
        assert '400' in rv.status
        assert 'BAD REQUEST' in rv.status
        assert 'error' in rv.data

    def test_no_email_or_phone(self):
        rv = self.create_account('Jackson', None, None)
        assert 'phone' in rv.data
        assert '400' in rv.status
        assert 'BAD REQUEST' in rv.status
        assert 'error' in rv.data

    def test_update_location(self):
        rv = self.create_account('Jackson', '12345678901', None)
        account = json.loads(rv.data)
        rv = self.app.post('/accounts/location', data = {
            'latitude': 41.8236,
            'longitude': -71.4222
        }, headers={
            'X-PITA-ACCOUNT-ID': account['aid'],
            'X-PITA-SECRET': account['key']
        });
        result = json.loads(rv.data)
        assert result['status'] == 'ok'


