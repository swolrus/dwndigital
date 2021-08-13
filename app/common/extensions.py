from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from app.payments.paypalSDK import PayPalClient

# Initialize Firestore DB
db = MongoEngine()
login = LoginManager()
mail = Mail()
paypal = PayPalClient()