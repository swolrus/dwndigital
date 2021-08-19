from flask import current_app as app
from flask import Flask, Blueprint, session, render_template, request, url_for, flash, redirect
from app.payments.models import Item
import json
from app.payments import errors
from app.payments.forms import BuyForm
from app.common.util import toJSON, send_invoice
from app.payments.models import Item, PurchasedItem, Buyer, Transaction, Invoice
from app.common.extensions import paypal

default_routes = Blueprint('app', __name__)

# create app-wide context (dictionary containing templates and navigation) 
@app.context_processor
def inject_dict_for_all_templates():
    return dict(    the_template='base.html')

@app.route('/')
def home():
    return render_template('base.html', home=True, title='WELCOME')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', title='GALLERY')

@app.route('/drops')
def drops():
    items = Item.objects()
    return render_template('items.html', title='A/W 2021 Lush Collection', items=items)

@app.route('/add/<string:ref>', methods=['POST'])
def add(ref):
    # validate the received values
    quantity = int(request.form['quantity'])
    sizes = request.form['options']

    session.modified = True
    if quantity and sizes and request.method == 'POST':
        item = PurchasedItem(item=Item.objects().get_or_404(pk=ref), quantity=quantity, sizes=sizes).to_dict()
        if 'items' in session:
            for i in session['items']:
                if i['ref'] == ref and i['sizes'] == sizes:
                    i['quantity'] += quantity
                    i['total'] += quantity * item.price
                    flash('Successfully added ' + str(quantity) + ' to cart!')
                    return redirect(url_for('drops'))
        else:
            session['items'] = []

        session['items'].append(item)
        flash('Successfully added ' + str(quantity) + ' to cart!')

    return redirect(url_for('drops'))

@app.route('/delete/<string:ref>/<string:sizes>')
def delete(ref, sizes):
    if 'items' in session:
        session['items'] = [i for i in session['items'] if not (ref == i['ref'] and sizes == i['sizes'])]

    return redirect(url_for('checkout'))

@app.route('/empty')
def empty():
    try:
        print(session['items'])
        session.clear()
        flash('Cart emptied! Hope you just changed your mind x')
        return redirect(url_for('drops'))
    except Exception as e:
        print(e)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
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
        'pickup': form.pickup.data,
        'items': []
    }
    if form.validate_on_submit():
        name = data['firstname']
        lastname = data['lastname']
        street = data['street']
        country = data['country']
        city = data['city']
        state = data['state']
        postcode = data['postcode']
        pickup = data['pickup']
        
        buyer = Buyer.objects(email=data['email']).first()
        if not buyer:
            buyer = Buyer(email=data['email'], name=name, lastname=lastname, street=street, country=country, city=city, state=state, postcode=postcode).save()
        
        t = Transaction(status='pending', buyer=buyer)
        
        for i in session['items']:
            print(i)
            item = PurchasedItem(item=Item.objects().get_or_404(pk=i['ref']).ref, quantity=i['quantity'], sizes=i['sizes'])
            t.items.append(item)
            data['items'].append(item.to_dict())

        if not len(data['items']) > 0:
          flash('Please add items to cart first :)')
          return(redirect(url_for('drops')))

        if not pickup:
          item = PurchasedItem(item='shipping', quantity=1, sizes='')
          t.items.append(item)
          data['items'].append(item.to_dict())

        data = paypal.build_request(data)
        result = paypal.create_order(data)

        t.order_id = result.result.id
        t.invoice_id = 0

        t.set_expire_at(900)
        t.save()

        flash('This transaction is available to confirm for 15 minutes :)')
        return redirect(url_for('payment', order_id=t.order_id))

    return render_template('checkout.html', title='Buyer Information', form=form)


@app.route('/payment/<string:order_id>', methods=['GET'])
def payment(order_id):
    t = Transaction.objects().get_or_404(pk=order_id)
    
    return render_template(
        'order.html', 
        title='Last step before your new cop!', 
        transaction=t.to_dict(include_email=True), 
        order_id=order_id)


@app.route('/reciept/<string:order_id>/', methods=['GET'])
def approved(order_id):
    t = Transaction.objects().get_or_404(pk=order_id)
    status = paypal.get_status(order_id)

    if t.invoice_id != 0:
        return render_template('order.html', title='Order Status', transaction=t.to_dict(include_email=True))

    i = Invoice.objects().first()
    invoice = i.invoice
    i.invoice += 1
    i.save()

    t.invoice_id=invoice
    send_invoice(t=t)

    title = "Big ups " + t.buyer.name + "! You'll hear from us soon x"

    t.status = status
    t.time_expires = None
    t.save()
    
    return render_template('checkout.html', title=title, transaction=t.to_dict(include_email=True))
    