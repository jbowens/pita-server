import json
from endpoint_testcase import EndpointTestCase

class ErrorsTestCase(EndpointTestCase):

    def test_client_error(self):
        rv = self.app.post('/error', data = {
            'message': 'client done fucked up'
        })
        output = json.loads(rv.data)
        assert output['status'] == 'ok'
