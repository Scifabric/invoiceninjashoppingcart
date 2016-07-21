# -*- coding: utf8 -*-
#
# Copyright (C) 2016 Scifabric LTD.
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField


class NewClient(Form):

    """New Client Form."""

    name = StringField('name')
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    address1 = StringField('Address', validators=[DataRequired()])
    address2 = StringField('Address 2')
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
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


invoiceSchema = {
        "type": "object",
        "properties": {
            "client_id": {"type": "string"},
            "product_key": {"type": "string"},
            "notes": {"type": "string"},
            "cost": {"type": "number"},
            "qty": {"type": "number"},
            "recurring": {"type": "string"},
            },
        "required": ["client_id", "cost", "qty"]
        }
