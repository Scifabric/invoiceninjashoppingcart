import json
import data
from app import app
from mock import patch, Mock, MagicMock


class TestApp(object):

    def setUp(self):
        """Setup method for configuring the tests."""
        self.app = app
        self.app.config['TESTING'] = True
        self.tc = self.app.test_client()


    def test_get_new_client(self):
        """Test get new client returns CSRF token."""
        res = self.tc.get('/newclient')
        err_msg = "There should be a CSRF token"
        tmp = json.loads(res.data)
        assert tmp['csrf_token'], err_msg
        assert tmp['csrf_token'] != '', err_msg

    @patch('app.invoiceninja')
    def test_post_new_client(self, mymock):
        """Test post new client returns CSRF token."""

        mymock.create_client.return_value = dict(id=1)

        res = self.tc.get('/newclient')
        err_msg = "There should be a CSRF token"
        tmp = json.loads(res.data)

        data.form_client_data['csrf_token'] = tmp['csrf_token']
        res = self.tc.post('/newclient', data=data.form_client_data)
        tmp = json.loads(res.data)
        print tmp
        err_msg = "A client should be created."
        assert tmp['id'] == 1, err_msg
