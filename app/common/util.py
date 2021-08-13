import os
from flask import current_app as app
from flask import render_template
import json
from app.common.extensions import mail
from flask_mail import Message

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def toJSON(obj):
        return json.dumps(obj, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def to_pretty_json(value):
    return json.dumps(value, sort_keys=True,
                      indent=4, separators=(',', ': '))

def send_invoice(t):
    transaction = t.to_dict(include_email=True)
    invoice = transaction['invoice_id']
    msg = Message(subject=invoice + ' - POSTMAN x KAIMAN Order Confirmation', sender='david@posted.studio', recipients=[transaction['email']])
    msg.html = render_template('invoice.html', transaction=transaction, shipping=t.get_shipping(), invoice=invoice)
    msg.body = msg.html
    mail.send(msg)