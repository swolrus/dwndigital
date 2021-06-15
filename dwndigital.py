from app.factory import create_app
import os

if __name__ == "__main__":
    configkey = os.environ.get('FLASK_ENV') or 'development'
    app = create_app(configkey)
    app.run(host='0.0.0.0')