import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    APP_NAME = 'dwndigital'
    #LOGIN_REDIRECT_ENDPOINT = 'users.index'
    DEBUG = False
    SECRET_KEY = 'secret_key'

    SESSION_COOKIE_SAMESITE = 'lax'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
        or 'sqlite:///' + os.path.join(basedir, 'dwndigital.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # If set to True SQLAlchemy will log all the statements issued to stderr
    # which can be useful for debugging.
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    pass

def get_env_obj(key):
    return {
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig',
    # default --
    }.get(key, 'config.DevelopmentConfig')