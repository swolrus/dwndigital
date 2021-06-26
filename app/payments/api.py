from flask import Blueprint, url_for, request, jsonify, render_template
from app.common.extensions import db, paypal
from app.payments.models import Item, PurchasedItem, Buyer, Transaction
from app.common.util import toJSON


payments_api = Blueprint('payments', __name__, url_prefix='/payments')

from app.payments import errors, tokens

@payments_api.route('/create', methods=['POST'])
def create_transaction():
    data = request.get_json()

    for item in ['firstname', 'lastname', 'email', 'address', 'country', 'city', 'state', 'postcode', 'items']:
        if item not in data:
            return errors.bad_request('request must include: all fields')

    address = data['address'] + ' ' + data['country'] + ' ' + data['city'] + ' ' + data['state'] + ' ' + data['postcode']
    name = data['firstname'] + ' ' + data['lastname']
    buyer = Buyer.objects(email=data['email']).first()
    
    if not buyer:
        buyer = Buyer(email=data['email'], name=name, address=address).save()
    
    transaction = Transaction(status='pending', buyer=buyer)
    
    for i in data['items']:
        if not Item.objects().get(pk=i['id']):
            return errors.bad_request('request contains invalid items')
        item = PurchasedItem(item=i['id'], quantity=i['quantity'])
        transaction.items.append(item)
    
    data = paypal.build_request(data)
    result = paypal.create_order(data)

    transaction.order_id=result.result.id
    transaction.save()

    response = toJSON(result.result)
    
    return response

@payments_api.route('/items', methods=['GET'])
def get_items():
    data = Item.objects()
    return jsonify(data)

@payments_api.route('/reciept', methods=['GET'])
def set_approved():
    order_id=request.args.get('id')
    transaction = Transaction.objects(pk=order_id).get_or_404()
    trans = transaction.to_dict(include_email=True)
    
    return render_template('reciept.html', trans=trans)

@payments_api.route('/setitem', methods=['POST'])
def set_item():
    data = request.get_json()

    for item in ['ref', 'name', 'description', 'price']:
        if item not in data:
            return errors.bad_request('request must include: name, email, address fields')

    item = Item(ref=ref, name=name, description=description, price=price)
    item.save()

    return item.to_dict()

@payments_api.route('/log', methods=['POST'])
def db_transaction():
    data = request.data
    print(data)

    buyer.transactions.append(transaction)
    buyer.save()
    