import os
from flask import Flask, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app_settings = os.getenv("APP_SETTINGS")
app.config.from_object("project.config.DevelopmentConfig")

db = SQLAlchemy(app)


# Application factory
def create_app(script_info=None):
    # instantiate app
    app = Flask(__name__)

    # set config
    app.settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from project.api.users import users_blueprint

    app.register_blueprint(users_blueprint)

    # shell context from flask cli
    app.shell_context_processor({"app": app, "db": db})
    
    return app


@app.route("/", methods=["GET"])
def index():
    return jsonify({"1": "hallooo", "2": "yessss"})
