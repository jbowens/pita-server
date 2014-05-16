import json, random, string
from endpoint_testcase import EndpointTestCase

class AccountsTestCase(EndpointTestCase):

    def create_account(self, name, phone, email):
        uuid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        return self.app.post('/accounts/new', data = {
            'name': name,
            'phone': phone,
            'email': email,
            'uuid': uuid}, follow_redirects=True)

    def test_new_account(self):
        rv = self.create_account('Jackson', '14405554444', 'john@doe.org')
        assert 'aid' in rv.data
        assert 'key' in rv.data
        obj = json.loads(rv.data)
        assert obj['aid'] > 0
        assert len(obj['key']) == 128

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

    def test_access_denied(self):
        rv = self.app.post('/accounts/location', data = {
            'latitude': 41.8236,
            'longitude': -71.4222
        }, headers={
            'X-PITA-ACCOUNT-ID': 2,
            'X-PITA-SECRET': 'let me in plz'
        });
        assert '403' in rv.status

