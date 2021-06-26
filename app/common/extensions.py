from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from app.payments.paypalSDK import PayPalClient

# Initialize Firestore DB
db = MongoEngine()
login = LoginManager()
paypal = PayPalClient()