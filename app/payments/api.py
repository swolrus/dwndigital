from flask import Blueprint, url_for, request, jsonify
from app.common.extensions import db
from app.payments.models import Item, PurchasedItem, Buyer, Transaction


payments_api = Blueprint('payments', __name__, url_prefix='/payments')

from app.payments import errors, tokens

@payments_api.route('/', methods=['GET'])
def get_transaction():
    email = requests.args.get('email')
    return jsonify(Buyer.objects(email=email).get_or_404())

@payments_api.route('/items', methods=['GET'])
def get_items():
    data = Item.objects()
    return jsonify(data)

@payments_api.route('/setapproved/<int:oid>', methods=['POST'])
def set_approved(oid):
    transaction = Transaction.objects(id=oid).get_or_404()
    transaction.status = 'approved'
    transaction.save()
    
    response = jsonify(transaction)
    response.status_code = 201
    response.headers['Location'] = url_for('payments.get_transaction', id=transaction.oid)
    return response

@payments_api.route('/setitem', methods=['POST'])
def set_item():
    data = request.get_json()

    for item in ['name', 'price', 'displayname', 'description']:
        if item not in data:
            return errors.bad_request('request must include: name, email, address fields')

    item = Item(name=name, price=price, displayname=displayname, description=description)
    item.save()

    return jsonify(item)

@payments_api.route('/create', methods=['POST'])
def create_transaction():
    data = request.get_json()

    for item in ['name', 'email', 'address', 'items']:
        if item not in data:
            return errors.bad_request('request must include: name, email, address fields')

    buyer = Buyer.objects(email=data['email']).first()
    if not buyer:
        buyer = Buyer(email=data['email'], name=data['name'], address=data['address'])

    transaction = Transaction(status='pending')
    
    for i in data['items']:
        if not Item.objects(pk=item['id']).first():
            return errors.bad_request('request contains invalid items')
        item = PurchasedItem(item=i['id'], quantity=i['quantity'])
        transaction.items.append(item)

    buyer.transactions.append(transaction)
    buyer.save()

    response = jsonify(transaction)
    response.status_code = 201
    response.headers['Location'] = url_for('payments.get_transaction')
    return response

@payments_api.route('/wh', methods=['POST'])
def webhook():
    print("paypal webhook")
    if request.method == 'POST':
        print(request.json)
        return '', 200
    else:
        errors.bad_request('Paypal Request Error')