import json
from collections import namedtuple

countries = [dict(name='Spain', id=1)]

frequencies = [{u'id': 1, u'name': u'Weekly'}, {u'id': 2, u'name': u'Two weeks'},
               {u'id': 3, u'name': u'Four weeks'}, {u'id': 4, u'name': u'Monthly'},
               {u'id': 5, u'name': u'Three months'},
               {u'id': 6, u'name': u'Six months'}, {u'id': 7, u'name': u'Annually'}]

static = dict(industries=None, currencies=None, sizes=None,
              fonts=None, timezones=None, invoiceStatus=None,
              countries=countries, languages=None, paymentTypes=None,
              paymentTerms=None, gateways=None, frequencies=frequencies,
              banks=None, invoiceDesigns=None, datetimeFormats=None,
              dateFormats=None)

FakeRequest = namedtuple('FakeRequest', ['json', 'status_code', 'headers'])

mimetype = {'content-type': 'application/json'}

def return_static():
    return dict(data=static)

static_response = FakeRequest(return_static, 200, mimetype)

client = dict(contact=dict(email='me@me.com'), is_deleted=False)

def return_client():
    return dict(data=[client])

client_response_exists = FakeRequest(return_client, 200, mimetype)

def return_no_client():
    return dict(data=[])

client_response_no_exists = FakeRequest(return_no_client, 200, mimetype)

client_response_no_403 = FakeRequest(return_no_client, 403, mimetype)


def return_client_from_in():
    return dict(data=dict(id=1))

client_from_invoice_ninja = FakeRequest(return_client_from_in, 200, mimetype)
client_from_invoice_ninja_403 = FakeRequest(return_client_from_in, 403, mimetype)


def return_invoice():
    return dict(data=dict(id=1))

def return_403():
    return dict(err=403)

invoice_response = FakeRequest(return_invoice, 200, mimetype)
invoice_response_403 = FakeRequest(return_403, 403, mimetype)

form_client_data = dict(name='University', first_name='Perico',
                        last_name='Palotes', address1='address1',
                        address2='address2', city='Madrid', state='Madrid',
                        postal_code='28045', country='4',
                        email='perico@palotes.com', vat='IDVAT')

form_invoice_data = dict(client_id='1', product_key='1',
                         notes='Notes', cost=1, qty=1, recurring=None)
