from flask import Blueprint
from app.users.models import *

users_routes = Blueprint('users', __name__, url_prefix='/users')