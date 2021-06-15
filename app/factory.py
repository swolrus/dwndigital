from flask import Flask, render_template
import config

def create_app(configkey: str) -> str:
    # creates an app instance with config defaulting to the FLASK_ENV
    # if param is passed will be used to set config instead of FLASK_ENV
    # see module config.mode for options

    # create app instance
    app = Flask(__name__)

    with app.app_context():
    # context for the app
        configure_app(app, configkey)
        configure_blueprints(app)
        configure_jinja(app)
        configure_error_handlers(app)

        return app


def configure_app(app: object, configkey: str) -> None:
    app.config.from_object(config.get_env_obj(configkey))


def configure_blueprints(app: object) -> None:
    from app.routes import default as default_blueprint

    # register each blueprint
    for blueprint in [default_blueprint]:
        app.register_blueprint(blueprint)


def configure_jinja(app: object) -> None:
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    # Globals
    app.jinja_env.globals['APP_NAME'] = app.config['APP_NAME']


def configure_error_handlers(app: object) -> None:
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('/errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('/errors/500.html'), 500