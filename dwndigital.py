from app.factory import create_app
from app.common.extensions import login, db
from app.admin.models import User
from app.payments.models import Buyer, Item, PurchasedItem, Transaction, Invoice
import os, logging

configkey = os.environ.get('FLASK_ENV') or 'development'
app = create_app(configkey)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.shell_context_processor
def make_shell_context():
    
    ''' Populate the shell.
    Use `flask shell`.
    '''
    return {
        'app': app,
        'db': db,
        'login': login,
        'Buyer': Buyer,
        'Item': Item,
        'PurchasedItem': PurchasedItem,
        'Transaction': Transaction,
        'User': User,
        'Invoice': Invoice,
    }