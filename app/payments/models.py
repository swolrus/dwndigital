from app.common.extensions import db
from app.common.models import BaseMixin
from werkzeug.security import check_password_hash, generate_password_hash

class Buyer(BaseMixin, db.Model):
    email = db.Column(db.String(64), unique=True)
    fullname = db.Column(db.String(64))
    address = db.Column(db.String(256))

    def __init__(self, *args, **kwargs):
        # Set given email address to lowercase.
        kwargs.update({'email': kwargs.get('email').lower()})
        super().__init__(*args, **kwargs)

    def from_dict(self, data):
        for field in ['fullname', 'email', 'address']:
            if field in data:
                setattr(self, field, data[field])

class Item(BaseMixin, db.Model):
    name = db.Column(db.String(64))
    price = db.Column(db.Integer)

    def __init__(self, item, price):
        self.item = item
        self.price = price

class Transaction(BaseMixin, db.Model):
    buyer_id = db.Column(db.Integer, db.ForeignKey(Buyer.id))
    item_id = db.Column(db.Integer, db.ForeignKey(Item.id))
    quantity = db.Column(db.Integer, nullable=False)

    item = db.relationship("Item", lazy='dynamic', backref="transactions")
    buyer = db.relationship("Buyer", lazy='dynamic', backref="transactions")

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'buyer_id': self.buyer.id,
            'buyer': self.buyer.name,
            'adress': self.buyer.adress,
            'item_id': self.item.id,
            'item': self.item.name,
            'quantity': self.quantity,
        }
        if TransactionApproved.query.filter_by(transaction_id=id):
            data['approved'] = True
        else:
            data['approved'] = False
        return data

    def from_dict(self, data):
        for field in ['buyer_id', 'item_id', 'quantity']:
            if field in data:
                setattr(self, field, data[field])
    

class TransactionApproved():
    transaction_id = db.Column(db.Integer, db.ForeignKey(Buyer.id))

    def __init__(self, transaction_id):
        self.transaction_id = transaction_id

    transaction = db.relationship("Transaction", lazy='dynamic', backref="approved")