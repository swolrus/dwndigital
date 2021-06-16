from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.common.extensions import db, login
from app.common.models import BaseMixin

class User(UserMixin, BaseMixin, db.Model):
    username = db.Column(db.String(35), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Buyer', backref='buyer', lazy='dynamic', order_by='desc(Post.created)')

    def __init__(self, *args, **kwargs):
        # Set given email address to lowercase.
        kwargs.update({'email': kwargs.get('email').lower()})
        super().__init__(*args, **kwargs)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))