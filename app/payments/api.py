from flask import Blueprint
from flask import jsonify
from flask import request, url_for
from app.common.extensions import db
from app.payments.models import Buyer, Item, Transaction, Transaction


payments_api = Blueprint('payments', __name__, url_prefix='/payments')

from app.payments import errors, tokens

@payments_api.route('/', methods=['GET'])
def test():
    response = jsonify({ 'test': 'worked' })
    response.status_code = 200
    return response

@payments_api.route('/<int:id>', methods=['GET'])
def get_transaction(id):
    return jsonify(Transaction.query.get_or_404(id).to_dict())

@payments_api.route('/items', methods=['GET'])
def get_items():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Item.to_collection_dict(Item.query, page, per_page, 'Payments.get_items')
    return jsonify(data)

@payments_api.route('/listener', methods=['POST'])
def set_approved(id):

    transaction = Transaction.query.get_or_404(id)
    transaction.status = 'approved'
    transaction.commit()
    
    response = jsonify(transaction.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('payments.get_transaction', id=transaction.id)
    return response

@payments_api.route('/create', methods=['PUT'])
def create_transaction():
    data = request.get_json() or {}
    for item in ['name', 'email', 'address', 'item_id', 'quantity']:
        if item not in data:
            return errors.bad_request('Must include: name, email, address, item_id, quantity fields')
    if Buyer.query.filter_by(email=data['email']).first():
        return errors.bad_request('Please use a different email address')

    buyer_id = Buyer(email=data['email'], name=data['name'], address=data['address']).commit().id
    transaction = Transaction(buyer_id=buyer_id, item_id=data['item_id'], quantity=data['quantity']).commit()

    response = jsonify(transaction.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('payments.get_transaction', id=transaction.id)
    return response

@payments_api.route('/wh', methods=['POST'])
def webhook():
    print("paypal webhook")
    if request.method == 'POST':
        print(request.json)
        return '', 200
    else:
        errors.bad_request('Paypal Request Error')