import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')

    APP_NAME='dwn digital'
    DEBUG = False

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    # If set to True SQLAlchemy will log all the statements issued to stderr
    # which can be useful for debugging.
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'testing-dwndigital.db')
    TESTING = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    pass

def get_env_obj(key):
    return {
        'development': 'config.DevelopmentConfig',
        'production': 'config.ProductionConfig',
        'testing': 'config.TestingConfig',
    # default --
    }.get(key, 'config.DevelopmentConfig')