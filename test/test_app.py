import json
import data
from app import app
from mock import patch, Mock


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
