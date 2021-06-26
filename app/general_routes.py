from flask import current_app as app
from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect
from app.payments.models import Item
import requests
from app import payments
from app.payments import errors

default_routes = Blueprint('app', __name__)

# create app-wide context (dictionary containing templates and navigation) 
@app.context_processor
def inject_dict_for_all_templates():
    return dict(    the_template='base.html')

@app.route('/')
def home():
    data = Item.objects()
    return render_template('items.html', items=data)

@app.route('/buy')
def checkout():
    pk = request.args.get('item')
    item = Item.objects(pk=pk).get_or_404()
    return render_template('buy.html', item=item)