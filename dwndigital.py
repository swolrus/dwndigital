from app.factory import create_app
from app.common.extensions import db, migrate, login
from app.payments.models import Buyer, Item, Transaction
import os
from dotenv import load_dotenv
load_dotenv()

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
        'migrate': migrate,
        'login': login,
        'Buyer': Buyer,
        'Item': Item,
        'Transaction': Transaction,
        #'User': User,
    }