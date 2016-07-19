import json
import data
from app import app, format_client_data, format_invoice_data
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
        """Test post new client works."""

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

    def test_post_errors_new_client(self):
        """Test post new client returns errors."""

        tmp = data.form_client_data.copy()
        tmp['first_name'] = None
        res = self.tc.post('/newclient', data=tmp)
        tmp = json.loads(res.data)
        err_msg = "A list of errors should be returned."
        assert 'csrf_token' in tmp.keys(), err_msg
        assert 'first_name' in tmp.keys(), err_msg


    def test_get_new_invoice(self):
        """Test get new invoice returns CSRF token."""
        res = self.tc.get('/newinvoice')
        err_msg = "There should be a CSRF token"
        tmp = json.loads(res.data)
        assert tmp['csrf_token'], err_msg
        assert tmp['csrf_token'] != '', err_msg

    @patch('app.invoiceninja')
    def test_post_new_invoice(self, mymock):
        """Test post new invoice works."""

        mymock.create_invoice.return_value = dict(id=1)

        res = self.tc.get('/newinvoice')
        tmp = json.loads(res.data)

        data.form_invoice_data['csrf_token'] = tmp['csrf_token']
        res = self.tc.post('/newinvoice', data=data.form_invoice_data)
        tmp = json.loads(res.data)
        err_msg = "An invoice should be created."
        assert tmp['id'] == 1, err_msg

    def test_post_errors_new_invoice(self):
        """Test post new invoice returns errors."""

        tmp = data.form_invoice_data.copy()
        tmp['client_id'] = None
        res = self.tc.post('/newinvoice', data=tmp)
        tmp = json.loads(res.data)
        err_msg = "A list of errors should be returned."
        assert 'csrf_token' in tmp.keys(), err_msg
        assert 'client_id' in tmp.keys(), err_msg

    @patch('app.invoiceninja')
    def test_get_countries(self, mymock):
        """Test get countries returns a list of countries."""
        mymock.static = dict(countries=[{'name': 'Spain'}])
        res = self.tc.get('/countries')
        tmp = json.loads(res.data)

        err_msg = "There should be a list of countries."
        assert len(tmp) == 1, err_msg
        assert tmp[0]['name'] == 'Spain', err_msg

    def test_format_invoice_data(self):
        """Test format invoice data works."""
        dat = data.form_invoice_data.copy()
        res = format_invoice_data(dat)

        err_msg = "Wrong format for invoice"
        assert 'invoice_items' in res.keys(), err_msg
        assert res['invoice_items'] == [dat], err_msg
        assert 'email_invoice' in res.keys(), err_msg
        assert res['email_invoice'], err_msg
