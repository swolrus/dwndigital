from app.common.models import TimestampMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app.common.extensions import db
from bson.objectid import ObjectId

class Item(db.Document):
    name = db.StringField(required=True)
    price = db.IntField(required=True)
    img = db.StringField(required=True)
    active = db.BooleanField(required=True, default=True)
    description = db.StringField()
    
    def get_pk():
        return str(self.pk)
    
class PurchasedItem(db.EmbeddedDocument):
    item = db.ReferenceField(Item)
    quantity = db.IntField(required=True)

    def to_dict(self):
        data = {
            'name': self.name,
            'quantity': self.quantity,
        }
        return data
        
class Transaction(db.EmbeddedDocument, TimestampMixin):
    status = db.StringField(required=True)
    items = db.ListField(db.EmbeddedDocumentField(PurchasedItem), default=list)

    def get_total(self):
        total = 0
        for i in self.items:
            total += i.item.price * i.quantity
        return total

class Buyer(db.Document):
    email = db.StringField(required=True, primary_key=True)
    name = db.StringField(required=True)
    address = db.StringField(required=True)

    transactions = db.ListField(db.EmbeddedDocumentField(Transaction), default=list)
    
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