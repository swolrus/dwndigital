from app.common.models import TimestampMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app.common.extensions import db

class Item(db.Document):
    ref = db.StringField(required=True, primary_key=True)
    name = db.StringField(required=True)
    price = db.IntField(required=True)
    img = db.StringField(required=True)
    active = db.BooleanField(required=True, default=True)
    description = db.StringField()
    
class PurchasedItem(db.EmbeddedDocument):
    item = db.ReferenceField(Item)
    quantity = db.IntField(required=True)

    def to_dict(self):
        item = Item.objects.get(pk=self.item.id)
        data = {
            'name': self.item.name,
            'quantity': self.quantity,
            'price': str(self.item.price) + ' AUD',
            'total': str(self.item.price * self.quantity) + ' AUD',
        }
        return data
        
class Buyer(db.Document):
    email = db.StringField(required=True, primary_key=True)
    name = db.StringField(required=True)
    address = db.StringField(required=True)
    
    def __init__(self, *args, **kwargs):
        # Set given email address to lowercase.
        kwargs.update({'email': kwargs.get('email').lower()})
        super().__init__(*args, **kwargs)

class Transaction(TimestampMixin, db.Document):
    order_id = db.StringField(required=True, primary_key=True)
    status = db.StringField(required=True)
    response = db.StringField()
    buyer = db.ReferenceField(Buyer, required=True)
    items = db.EmbeddedDocumentListField(PurchasedItem)

    def get_total(self):
        total = 0
        for i in self.items:
            total += i.item.price * i.quantity
        return total

    def to_dict(self, include_email=False):
        data = {
            'name': self.buyer.name,
            'address': self.buyer.address,
            'total': str(self.get_total()) + ' AUD',
            'status': self.status,
            'items': []
        }
        for item in self.items:
            data['items'].append(item.to_dict())
        if include_email:
            data['email'] = self.buyer.email
        return data