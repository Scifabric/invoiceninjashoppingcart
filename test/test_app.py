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
        res = self.tc.post('/newclient', data=data.form_client_data,
                           headers={'X-CSRFToken': tmp['csrf_token']})
        tmp = json.loads(res.data)
        err_msg = "A client should be created."
        assert tmp['id'] == 1, err_msg

    def test_post_errors_new_client(self):
        """Test post new client returns errors."""

        res = self.tc.get('/newclient')
        err_msg = "There should be a CSRF token"
        tmp_csrf = json.loads(res.data)

        tmp = data.form_client_data.copy()
        tmp['first_name'] = None
        res = self.tc.post('/newclient', data=tmp,
                           headers={'X-CSRFToken': tmp_csrf['csrf_token']})
        tmp = json.loads(res.data)
        err_msg = "A list of errors should be returned."
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
        mydata = data.invoice_json.copy()
        res = self.tc.post('/newinvoice', data=json.dumps(mydata),
                           content_type='application/json',
                           headers={'X-CSRFToken': tmp['csrf_token']})
        tmp = json.loads(res.data)
        err_msg = "An invoice should be created."
        assert tmp['id'] == 1, err_msg

    @patch('app.invoiceninja')
    def test_post_new_recurring_invoice(self, mymock):
        """Test post new recurring invoice works."""

        mymock.create_recurring_invoice.return_value = dict(id=1)

        res = self.tc.get('/newinvoice')
        tmp = json.loads(res.data)

        data.form_invoice_data['csrf_token'] = tmp['csrf_token']
        data.form_invoice_data['recurring'] = 'monthly'
        invoice_rec = data.invoice_json.copy()
        invoice_rec['recurring'] = 'monthly'
        res = self.tc.post('/newinvoice', data=json.dumps(invoice_rec),
                           content_type='application/json',
                           headers={'X-CSRFToken': tmp['csrf_token']})
        tmp = json.loads(res.data)
        err_msg = "An invoice should be created."
        assert tmp['id'] == 1, err_msg

    def test_post_errors_new_invoice(self):
        """Test post new invoice returns errors."""
        res = self.tc.get('/newinvoice')
        tmp_csrf = json.loads(res.data)

        tmp = data.invoice_json.copy()
        tmp['client_id'] = "1"
        res = self.tc.post('/newinvoice', data=json.dumps(tmp),
                           content_type='application/json',
                           headers={'X-CSRFToken': tmp_csrf['csrf_token']})
        tmp = json.loads(res.data)
        err_msg = "A list of errors should be returned."
        assert 'message' in tmp.keys(), err_msg

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
        res = format_invoice_data(data.invoice_json)

        err_msg = "Data should be valid"
        assert res == data.invoice_json, err_msg

        wrong_data = data.invoice_json.copy()
        wrong_data['client_id'] = "string"
        wrong_data['invoice_items'] = [data.invoice_items_json.copy()]
        res = format_invoice_data(wrong_data)

        err_msg = "It should return a format error"
        msg = "'string' is not of type 'number'"
        assert res['message'] == msg, res

        wrong_data['client_id'] = 1
        wrong_data['invoice_items'][0]['qty'] = '1'

        res = format_invoice_data(wrong_data)
        msg = "'1' is not of type 'number'"
        assert res['message'] == msg, res

    def test_format_client_data(self):
        """Test format client data works."""
        dat = data.form_client_data.copy()
        dat2 = data.form_client_data.copy()
        res = format_client_data(dat)

        err_msg = "Wrong format for client"
        assert 'contact' in res.keys(), err_msg
        assert res['contact']['email'] == dat2['email'], err_msg
        assert res['contact']['first_name'] == dat2['first_name'], err_msg
        assert res['contact']['last_name'] == dat2['last_name'], err_msg
        assert res['name'] == dat2['name'], err_msg

        name = "%s %s" % (dat2['first_name'], dat2['last_name'])
        dat2['name'] = None
        res = format_client_data(dat2)
        assert res['name'] == name, err_msg
