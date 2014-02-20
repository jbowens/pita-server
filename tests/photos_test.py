import json
from endpoint_testcase import EndpointTestCase
from StringIO import StringIO

class PhotosTestCase(EndpointTestCase):

    def test_photo(self):
        acc = self.rand_account()
        rv = self.app.post('/photos/record', data = {
            'context': 'feeding',
            'photo': (StringIO('test file contents'), 'test.jpg')
            }, headers = {
            'X-PITA-ACCOUNT-ID': acc['aid'],
            'X-PITA-SECRET': acc['key']
            })
        o = json.loads(rv.data)
        assert o['status'] == 'ok'
