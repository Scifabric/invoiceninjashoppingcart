from flask import Flask, jsonify, request
from forms import NewClient, NewInvoice
from flask_cors import CORS, cross_origin
from flask_wtf.csrf import generate_csrf
from invoiceninja import invoiceNinja


app = Flask(__name__)
app.config.from_object('settings')
cors = CORS(app, resources={r"/*": {"origins": app.config.get('CORS'), "supports_credentials": True}})
invoiceninja = invoiceNinja(app.config.get('TOKEN'))


@app.route("/newclient", methods=['GET', 'POST'])
def newclient():
    """Endpoint for creating a new client."""
    form = NewClient()
    if request.method == 'GET':
        resp = form.data
        resp['csrf_token'] = generate_csrf()
        return jsonify(resp)
    else:
        if form.validate_on_submit():
            client = format_client_data(form.data)
            res = invoiceninja.create_client(client)
            return jsonify(res)
        else:
            return jsonify(form.errors)


@app.route("/newinvoice", methods=['GET', 'POST'])
def newinvoice():
    """Endpoint for creating a new invoice."""
    form = NewInvoice()
    if request.method == 'GET':
        resp = form.data
        resp['csrf_token'] = generate_csrf()
        return jsonify(resp)
    else:
        if form.validate_on_submit():
            invoice = format_invoice_data(form.data)
            if invoice['recurring'] != '':
                del invoice['email_invoice']
                res = invoiceninja.create_recurring_invoice(invoice)
            else:
                res = invoiceninja.create_invoice(invoice)
            return jsonify(res)
        else:
            return jsonify(form.errors)


@app.route("/countries")
def get_countries():
    """Return a list of countries and its IDs."""
    return jsonify(invoiceninja.static['countries'])


def format_invoice_data(data):
    invoice = dict()
    invoice['client_id'] = data['client_id']
    invoice['recurring'] = data['recurring']
    del data['client_id']
    del data['recurring']
    invoice['invoice_items'] = [data.copy()]
    invoice['email_invoice'] = True
    return invoice


def format_client_data(data):
    client = dict()
    client['contact'] = dict()
    client['contact'] = {'email': data['email'], 'first_name': data['first_name'],
                         'last_name': data['last_name']}
    if not data['name']:
        data['name'] = "%s %s" % (data['first_name'], data['last_name'])
    del data['email']
    del data['first_name']
    del data['last_name']
    client.update(data)
    return client

if __name__ == "__main__":
    app.run()
