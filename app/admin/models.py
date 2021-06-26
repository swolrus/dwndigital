from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from app.common.extensions import db, login
from app.common.models import TimestampMixin


class User(db.Document, UserMixin, TimestampMixin):
    email = db.StringField(required=True, primary_key=True)
    password = db.StringField(required=True)

    def __init__(self, *args, **kwargs):
        # Set given email address to lowercase.
        kwargs.update({'email': kwargs.get('email').lower()})
        super().__init__(*args, **kwargs)

    def set_password(self, password: str) -> object:
        self.password = generate_password_hash(password)
        return self

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

@login.user_loader
def load_user(email):
    return User.objects().get(email=email)