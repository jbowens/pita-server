import json
from endpoint_testcase import EndpointTestCase

class PitasTestCase(EndpointTestCase):

    def create_account_and_pita(self):
        acc = self.rand_account()
        rv = self.app.post('/pitas/random', dict(), headers = {
            'X-PITA-ACCOUNT-ID': acc['aid'],
            'X-PITA-SECRET': acc['key']
        })
        p = json.loads(rv.data)
        assert 'pid' in p
        return acc, p

    def test_random_pita(self):
        acc = self.rand_account()
        rv = self.app.post('/pitas/random', dict(), headers = {
            'X-PITA-ACCOUNT-ID': acc['aid'],
            'X-PITA-SECRET': acc['key']
        })
        p = json.loads(rv.data)
        assert 'pid' in p
        assert p.get('state') == 'egg'
        assert len(p.get('name', '')) > 3
        assert p.get('body_hue') is not None

    def test_unauth_random_pita(self):
        rv = self.app.post('/pitas/random', dict())
        assert '403' in rv.status

    def test_get_no_pita(self):
        acc = self.rand_account()
        rv = self.app.post('/pitas/get', dict(), headers = {
            'X-PITA-ACCOUNT-ID': acc['aid'],
            'X-PITA-SECRET': acc['key']
        })
        o = json.loads(rv.data)
        assert o['status'] == 'ok'
        assert o['has_pita'] is False

    def test_get_pita(self):
        acc, pita = self.create_account_and_pita()
        rv = self.app.post('/pitas/get', dict(), headers = {
            'X-PITA-ACCOUNT-ID': acc['aid'],
            'X-PITA-SECRET': acc['key']
        })
        o = json.loads(rv.data)
        assert o['has_pita'] is True
        assert o['pid'] == pita['pid']
        assert 'body_hue' in o
        assert o['name'] == pita['name']
        assert o['has_spots'] == pita['has_spots']
        assert o['state'] == pita['state']

    def test_save_no_pita(self):
        acc = self.rand_account()
        rv = self.app.post('/pitas/save', data = {
            'happiness': 80.4,
            'hunger': 34.6,
            'sleepiness': 66.6
        }, headers = {
            'X-PITA-ACCOUNT-ID': acc['aid'],
            'X-PITA-SECRET': acc['key']
        })
        assert '400' in rv.status
        o = json.loads(rv.data)
        assert o['user_error'] is False

    def test_save_pita(self):
        acc, pita = self.create_account_and_pita()
        # Save some arbitrary pita state attrbitutes
        rv = self.app.post('/pitas/save', data = {
            'happiness': 66.6,
            'hunger': 33.3,
            'sleepiness': 50.0
        }, headers = {
            'X-PITA-ACCOUNT-ID': acc['aid'],
            'X-PITA-SECRET': acc['key']
        })
        assert '200' in rv.status
        o = json.loads(rv.data)
        assert o['status'] == 'ok'
        # Get the pita and verify that the state attributes were saved.
        rv = self.app.post('/pitas/get', dict(), headers = {
            'X-PITA-ACCOUNT-ID': acc['aid'],
            'X-PITA-SECRET': acc['key']
        })
        assert '200' in rv.status
        p = json.loads(rv.data)
        assert p['status'] == 'ok'
        approx_equal = lambda a, b: abs(a - b) < 0.01
        assert approx_equal(p['happiness'], 66.6)
        assert approx_equal(p['hunger'], 33.3)
        assert approx_equal(p['sleepiness'], 50.0)
