import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    # General Settings
    APP_NAME='dwn digital'
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret'
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')

    MONGODB_SETTINGS = {
        'host': os.environ.get('DATABASE_URL')
    }

class TestingConfig(BaseConfig):
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