from app.common.extensions import db
from app.common.models import BaseMixin
from werkzeug.security import check_password_hash, generate_password_hash

class Buyer(BaseMixin, db.Model):
    email = db.Column(db.String(64), unique=True)
    fullname = db.Column(db.String(64))
    address = db.Column(db.String(256))

class Item(BaseMixin, db.Model):
    name = db.Column(db.String(64))
    price = db.Column(db.Integer)

class Transaction(BaseMixin, db.Model):
    buyer_id = db.Column(db.Integer, db.ForeignKey(Buyer.id))
    item_id = db.Column(db.Integer, db.ForeignKey(Item.id))
    quantity = db.Column(db.Integer, nullable=False)

    item = db.relationship("Item", lazy='dynamic', backref="transactions")
    buyer = db.relationship("Buyer", lazy='dynamic', backref="transactions")