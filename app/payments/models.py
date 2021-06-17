from app.common.extensions import db
from app.common.models import BaseMixin, TimestampMixin, PaginatedAPIMixin
from werkzeug.security import check_password_hash, generate_password_hash

class Buyer(BaseMixin, db.Model):
    email = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=False)

    def __init__(self, *args, **kwargs):
        # Set given email address to lowercase.
        kwargs.update({'email': kwargs.get('email').lower()})
        super().__init__(*args, **kwargs)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }
        if include_email:
            data['email'] = self.email
        return data


class Item(BaseMixin, PaginatedAPIMixin, db.Model):
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
        }
        return data


class Transaction(BaseMixin, TimestampMixin, db.Model):
    buyer_id = db.Column(db.Integer, db.ForeignKey(Buyer.id))
    item_id = db.Column(db.Integer, db.ForeignKey(Item.id))
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(16), default = 'pending')

    item = db.relationship("Item", backref="transactions")
    buyer = db.relationship("Buyer", backref="transactions")

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'buyer_id': self.buyer.id,
            'buyer': self.buyer.name,
            'email': self.buyer.email,
            'adress': self.buyer.address,
            'item_id': self.item.id,
            'item': self.item.name,
            'quantity': self.quantity,
            'total': self.get_total(),
            'status': self.status,
        }
        return data

    def get_total(self):
        return self.quantity * self.item.price