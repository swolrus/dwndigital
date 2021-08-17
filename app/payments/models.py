from app.common.models import TimestampMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app.common.extensions import db

class Invoice(db.Document):
    invoice = db.IntField(required=True)

class Item(db.Document):
    ref = db.StringField(required=True, primary_key=True)
    name = db.StringField(required=True)
    price = db.IntField(required=True)
    img = db.StringField()
    active = db.BooleanField(default=True)
    description = db.StringField()
    
class PurchasedItem(db.EmbeddedDocument):
    item = db.ReferenceField(Item)
    quantity = db.IntField(required=True)
    sizes = db.StringField()

    def to_dict(self):
        item = Item.objects.get(pk=self.item.pk)
        data = {
            'ref': self.item.pk,
            'name': self.item.name,
            'quantity': self.quantity,
            'price_int': self.item.price,
            'price': '$' + str(self.item.price) + ' AUD',
            'total_int': int(self.item.price * self.quantity),
            'total': '$' + str(self.item.price * self.quantity) + ' AUD',
            'sizes': self.sizes
        }
        return data
        
class Buyer(db.Document):
    email = db.StringField(required=True, primary_key=True)
    name = db.StringField(required=True)
    lastname = db.StringField(required=True)
    street = db.StringField(required=True)
    country = db.StringField(required=True)
    state = db.StringField(required=True)
    postcode = db.IntField(required=True)
    city = db.StringField(required=True)
    
    def __init__(self, *args, **kwargs):
        # Set given email address to lowercase.
        kwargs.update({'email': kwargs.get('email').lower()})
        super().__init__(*args, **kwargs)

class Transaction(TimestampMixin, db.Document):
    order_id = db.StringField(required=True, primary_key=True)
    invoice_id = db.IntField()
    status = db.StringField(required=True)
    response = db.StringField()
    buyer = db.ReferenceField(Buyer, required=True)
    items = db.EmbeddedDocumentListField(PurchasedItem)

    def get_total(self):
        total = 0
        for i in self.items:
            total += i.item.price * i.quantity
        return total

    def get_shipping(self):
        return self.buyer.name + ' ' + self.buyer.lastname + '<br>' + self.buyer.street + '<br>' + self.buyer.city + ' ' + self.buyer.country + ' ' + self.buyer.state + '<br>' + str(self.buyer.postcode)

    def to_dict(self, include_email=False):
        data = {
            'invoice_id': 'LUSH' + str(self.invoice_id).zfill(3),
            'name': self.buyer.name + ' ' + self.buyer.lastname,
            'address': self.buyer.street + ', ' + self.buyer.city + ' ' + self.buyer.country + ' ' + self.buyer.state + ', ' + str(self.buyer.postcode),
            'total': '$' + str(self.get_total()) + ' AUD',
            'status': self.status,
            'items': []
        }
        for item in self.items:
            data['items'].append(item.to_dict())
        if include_email:
            data['email'] = self.buyer.email
        return data