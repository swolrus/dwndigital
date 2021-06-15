from app.app_factory import create_app
import os, config
# read config from file
if os.environ['FLASK_ENV'] == 'production':
    app = create_app(config.ProductionConfig)
else:
    app = create_app(config.DevelopmentConfig)

if __name__ == "__main__":
    app.run(host='0.0.0.0')