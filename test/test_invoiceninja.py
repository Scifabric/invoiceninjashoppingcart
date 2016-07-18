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
