from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField



class NewClient(Form):
    """New Client Form."""
    name = StringField('name', validators=[DataRequired()])
    address1 = StringField('Address', validators=[DataRequired()])
    address2 = StringField('Address 2')
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    vat = StringField('VAT')


class NewInvoice(Form):
    """New Invoice Form."""
    client_id = StringField('Client ID', validators=[DataRequired()])
    product_key = StringField('Product Key')
    notes = StringField('Notes')
    cost = IntegerField('Cost', validators=[DataRequired()])
    qty = IntegerField('Quantity', validators=[DataRequired()])
    recurring = StringField('Recurring')
