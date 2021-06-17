from app.factory import create_app
from app.common.extensions import db, migrate, login
from app.payments.models import Buyer, Item, Transaction
import os
from flask import g

configkey = os.environ.get('FLASK_ENV') or 'development'
app = create_app(configkey)

if configkey=='production':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'

@app.shell_context_processor
def make_shell_context():
    ''' Populate the shell.
    Use `flask shell`.
    '''
    return {
        'app': app,
        'db': db,
        'migrate': migrate,
        'login': login,
        'Buyer': Buyer,
        'Item': Item,
        'Transaction': Transaction,
        #'user': User,
    }