import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

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

    # Upload Settings
    UPLOAD_STATIC_FOLDER = 'img/items'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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