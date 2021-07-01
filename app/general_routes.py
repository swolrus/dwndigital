from flask import current_app as app
from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect
from app.payments.models import Item
import json
from app.payments import errors
from app.payments.forms import BuyForm
from app.common.util import toJSON
from app.payments.models import Item, PurchasedItem, Buyer, Transaction
from app.common.extensions import paypal

default_routes = Blueprint('app', __name__)

# create app-wide context (dictionary containing templates and navigation) 
@app.context_processor
def inject_dict_for_all_templates():
    return dict(    the_template='base.html')

@app.route('/')
def home():
    return render_template('base.html', home=True, title='WELCOME')

@app.route('/drops')
def drops():
    items = Item.objects()
    return render_template('items.html', title='DROPS', items=items)

@app.route('/buy/<ref>', methods=['GET', 'POST'])
def buy(ref):
    form = BuyForm()
    data = {
        'firstname': form.firstname.data,
        'lastname': form.lastname.data,
        'email': form.email.data,
        'street': form.street.data,
        'country': form.country.data,
        'state': form.state.data,
        'city': form.city.data,
        'postcode': str(form.postcode.data),
        'items': [{
            'id': ref,
            'quantity': form.quantity.data,
            'sizes': form.sizes.data
        }]
    }
    if form.validate_on_submit():
        address = data['street'] + ' ' + data['country'] + ' ' + data['city'] + ' ' + data['state'] + ' ' + data['postcode']
        name = data['firstname'] + ' ' + data['lastname']
        
        buyer = Buyer.objects(email=data['email']).first()
        if not buyer:
            buyer = Buyer(email=data['email'], name=name, address=address).save()
        
        t = Transaction(status='pending', buyer=buyer)
        
        for i in data['items']:
            if not Item.objects().get(pk=i['id']):
                return errors.bad_request('Request contains invalid items (ಠ¿ಠ)')
            item = PurchasedItem(item=i['id'], quantity=i['quantity'], sizes=i['sizes'])
            t.items.append(item)
        
        data = paypal.build_request(data)
        result = paypal.create_order(data)

        t.order_id = result.result.id
        t.set_expire_at(900)
        t.save()

        flash('This transaction is available to confirm for 15 minutes :)')
        return redirect(url_for('checkout', order_id=t.order_id))

    item = Item.objects().get_or_404(pk=ref)
    return render_template('details.html', title='Buyer Information', form=form, item=item)


@app.route('/checkout/<order_id>', methods=['GET'])
def checkout(order_id):
    t = Transaction.objects().get_or_404(pk=order_id)
    return render_template(
        'checkout.html', 
        title='Last step before your new cop!', 
        transaction=t.to_dict(include_email=True), 
        order_id=order_id)

@app.route('/reciept/<order_id>/', methods=['GET'])
def approved(order_id):
    t = Transaction.objects().get_or_404(pk=order_id)
    status = paypal.get_status(order_id)
    print(status)
    title = "Big ups " + t.buyer.name.split(" ")[0] + "! You'll hear from us soon x"
    t.status = status
    t.time_expires = None
    t.save()
    
    return render_template('checkout.html', title=title, transaction=t.to_dict(include_email=True))
    