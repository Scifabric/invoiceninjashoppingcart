from invoiceninja import invoiceNinja
import data
from mock import patch, Mock


class TestInvoiceNinja(object):

    """Class for testing the invoice ninja module."""

    @patch('invoiceninja.invoiceNinja.get_static_data', return_value=data.static)
    def test_invoice_ninja_setup(self, mock_data):
        """Test invoice ninja setup works."""
        iv = invoiceNinja(token='token', url='http://myurl.com')

        err_msg = "invoice ninja should have been created with static data."
        assert iv.static == data.static, err_msg
        assert iv.token == 'token', err_msg
        assert iv.url == 'http://myurl.com', err_msg
        assert 'X-Ninja-Token' in iv.headers.keys(), err_msg
        assert iv.headers['X-Ninja-Token'] == 'token', err_msg

    @patch('invoiceninja.requests.get', return_value=data.static_response)
    def test_get_static_data(self, mock_data):
        """Test get_static_data works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')

        err_msg = "invoice ninja should have been created with static data."
        assert iv.static == data.static, err_msg
        assert iv.token == 'token', err_msg
        assert iv.url == 'http://myurl.com', err_msg
        assert 'X-Ninja-Token' in iv.headers.keys(), err_msg
        assert iv.headers['X-Ninja-Token'] == 'token', err_msg

    @patch('invoiceninja.requests.get', return_value=data.client_response_exists)
    def test_exists_client_returns_client(self, mock_data):
        """Test exists_client works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        client = iv.exists_client(data.client)
        err_msg = "It should return a client, as it exists."
        assert client['data'] == data.client, err_msg

    @patch('invoiceninja.requests.get', return_value=data.client_response_exists)
    def test_exists_client_returns_false_is_deleted(self, mock_data):
        """Test exists_client works."""

        data.client['is_deleted'] = True

        iv = invoiceNinja(token='token', url='http://myurl.com')
        client = iv.exists_client(data.client)
        err_msg = "It should return False, as it exists but has been deleted."
        assert client == False, err_msg


    @patch('invoiceninja.requests.get', return_value=data.client_response_no_exists)
    def test_exists_client_returns_false(self, mock_data):
        """Test exists_client works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        client = iv.exists_client(data.client)
        err_msg = "It should return False, as client does not exist."
        assert client == False, err_msg

    @patch('invoiceninja.requests.get', return_value=data.client_response_no_403)
    def test_exists_client_returns_false_403(self, mock_data):
        """Test exists_client works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        client = iv.exists_client(data.client)
        err_msg = "It should return False, as client does not exist."
        assert client == False, err_msg

    @patch('invoiceninja.requests.get', return_value=data.client_response_exists)
    def test_create_client(self, mock_data):
        """Test create_client works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        res = iv.create_client(data.client)
        err_msg = "It should return the client as it already exists."
        assert res['data'] == data.client, err_msg

    @patch('invoiceninja.requests.get', return_value=data.client_response_no_exists)
    @patch('invoiceninja.requests.post', return_value=data.client_from_invoice_ninja)
    def test_create_client_no_exists(self, mock_data, mock_post):
        """Test create_client works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        res = iv.create_client(data.client)
        err_msg = "It should a new client and have an ID."
        assert res['data']['id'] == 1, err_msg
        assert iv.client['data']['id'] == 1, err_msg

    @patch('invoiceninja.requests.get', return_value=data.client_response_no_exists)
    @patch('invoiceninja.requests.post', return_value=data.client_from_invoice_ninja_403)
    def test_create_client_400(self, mock_data, mock_post):
        """Test create_client works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        res = iv.create_client(data.client)
        err_msg = "It should a new client and have an ID."
        assert res['data']['id'] == 1, err_msg
        err_msg = "Client should not be created"
        assert iv.client is None, err_msg

    @patch('invoiceninja.invoiceNinja.get_static_data', return_value=data.static)
    @patch('invoiceninja.requests.post', return_value=data.invoice_response)
    def test_create_invoice(self, mock1, mock2):
        """Test create invoice works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        iv.client = dict()
        iv.client['data'] = dict()
        iv.client['data']['id'] = 1
        res = iv.create_invoice(dict(qty=1))
        err_msg = "There should be an invoice"
        assert res['data']['id'] == 1, err_msg
        assert iv.invoice['data']['id'] == 1, err_msg

    @patch('invoiceninja.invoiceNinja.get_static_data', return_value=data.static)
    @patch('invoiceninja.requests.post', return_value=data.invoice_response_403)
    def test_create_invoice_403(self, mock1, mock2):
        """Test create invoice works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        iv.client = dict()
        iv.client['data'] = dict()
        iv.client['data']['id'] = 1
        res = iv.create_invoice(dict(qty=1))
        err_msg = "Something went wrong, it returns error"
        assert res['err'] == 403, err_msg

    @patch('invoiceninja.invoiceNinja.get_static_data', return_value=data.static)
    @patch('invoiceninja.requests.post', return_value=data.invoice_response)
    def test_create_recurring_invoice_monthly(self, mock1, mock2):
        """Test create recurring invoice works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        iv.client = dict()
        iv.client['data'] = dict()
        iv.client['data']['id'] = 1
        res = iv.create_recurring_invoice(dict(qty=1, recurring='monthly'))
        err_msg = "There should be an invoice"
        assert res['data']['id'] == 1, err_msg
        assert iv.invoice['data']['id'] == 1, err_msg

    @patch('invoiceninja.invoiceNinja.get_static_data', return_value=data.static)
    @patch('invoiceninja.requests.post', return_value=data.invoice_response)
    def test_create_recurring_invoice_annually(self, mock1, mock2):
        """Test create recurring invoice works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        iv.client = dict()
        iv.client['data'] = dict()
        iv.client['data']['id'] = 1
        res = iv.create_recurring_invoice(dict(qty=1, recurring='annually'))
        err_msg = "There should be an invoice"
        assert res['data']['id'] == 1, err_msg
        assert iv.invoice['data']['id'] == 1, err_msg

    @patch('invoiceninja.invoiceNinja.get_static_data', return_value=data.static)
    @patch('invoiceninja.requests.post', return_value=data.invoice_response_403)
    def test_create_recurring_invoice_403(self, mock1, mock2):
        """Test create invoice works."""

        iv = invoiceNinja(token='token', url='http://myurl.com')
        iv.client = dict()
        iv.client['data'] = dict()
        iv.client['data']['id'] = 1
        res = iv.create_recurring_invoice(dict(qty=1, recurring='monthly'))
        err_msg = "Something went wrong, it returns error"
        assert res['err'] == 403, err_msg
