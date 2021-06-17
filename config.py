import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    APP_NAME = 'dwndigital'
    #LOGIN_REDIRECT_ENDPOINT = 'users.index'
    DEBUG = False
    SECRET_KEY = 'secret_key'

    SESSION_COOKIE_SAMESITE = 'lax'

    # If set to True SQLAlchemy will log all the statements issued to stderr
    # which can be useful for debugging.
    SQLALCHEMY_ECHO = False

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
        or 'sqlite:///' + os.path.join(basedir, 'testing-dwndigital.db')
    TESTING = True
    DEBUG = True

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
        or 'sqlite:///' + os.path.join(basedir, 'dwndigital.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dwndigital:2007@localhost:3306/dwndigital.db'

def get_env_obj(key):
    return {
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig',
        'testing': 'config.TestingConfig',
    # default --
    }.get(key, 'config.DevelopmentConfig')