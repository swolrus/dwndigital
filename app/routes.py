from flask import current_app as app
from flask import Flask, Blueprint, render_template, request, url_for, flash, redirect
from app.common.models import *

default_routes = Blueprint('app', __name__)

# create app-wide context (dictionary containing templates and navigation) 
@app.context_processor
def inject_dict_for_all_templates():
    return dict(    base_template='/templates/template-base.html')

@app.route('/')
def home():
    return render_template('/home.html')