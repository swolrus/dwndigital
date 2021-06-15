from app.app_factory import create_app
import os, config

configkey = os.environ.get('FLASK_ENV') or 'development'
app = create_app(config.get_env_obj(configkey))

if __name__ == "__main__":
    app.run(host='0.0.0.0')