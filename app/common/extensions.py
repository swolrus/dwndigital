from flask_login import LoginManager
from flask_mongoengine import MongoEngine

# Initialize Firestore DB
db = MongoEngine()
login = LoginManager()