import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate


db = SQLAlchemy()
toolbar = DebugToolbarExtension()
migrate = Migrate()


# Application factory
def create_app(script_info=None):
    # instantiate app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # start toolbar
    toolbar.init_app(app)

    # setup migrations
    migrate.init_app(app, db)

    # register blueprints
    from project.api.users import users_blueprint

    app.register_blueprint(users_blueprint)

    # shell context from flask cli
    app.shell_context_processor({"app": app, "db": db})

    return app
