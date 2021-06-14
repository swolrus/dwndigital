from flask import Flask
import os, config

def create_app():
    # creates an app instance with config defaulting to the FLASK_ENV
    # if param is passed will be used to set config instead of FLASK_ENV
    # see module config.mode for options

    # create app instance
    app = Flask(__name__)
    
    # read config from file
    app.config.from_object(config.ProductionConfig)

    with app.app_context():
    # context for the app
        from app.routes import default as default_blueprint

        # register each blueprint
        for blueprint in [default_blueprint]:
            app.register_blueprint(blueprint)
        
        return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')