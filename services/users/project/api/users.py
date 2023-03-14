from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import exc
from .models import User
from project import db


users_blueprint = Blueprint("users", __name__, template_folder="./templates")


@users_blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        db.session.add(User(username=username, email=email))
        db.session.commit()

    users = User.query.all()
    print(users)
    return render_template("index.html", users=users)


@users_blueprint.route("/users/ping", methods=["GET"])
def ping():
    return jsonify({"status": "success", "message": "pong"})


@users_blueprint.route("/users", methods=["POST"])
def add_user():
    post_data = request.get_json()
    error_response_obj = {"status": "fail", "message": "Invalid payload"}

    if not post_data:
        return jsonify(error_response_obj), 400

    try:
        username = post_data.get("username")
        email = post_data.get("email")

        user = User.query.filter_by(email=email).first()

        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()

            response_obj = {"status": "success",
                            "message": f"{email} was added"}

            return jsonify(response_obj), 201
        else:
            error_response_obj["message"] = "Email already in use"
            return jsonify(error_response_obj), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(error_response_obj), 400


@users_blueprint.route("/users/<user_id>", methods=["GET"])
def get_single_user(user_id):
    """
    Get single user details
    """

    response_object = {"status": "fail", "message": "User does not exist"}

    try:
        user = User.query.filter_by(id=int(user_id)).first()

        if not user:
            return jsonify(response_object), 400

        response_object = {
            "status": "success",
            "data": {
                "id": user_id,
                "username": user.username,
                "email": user.email,
                "active": user.active,
            },
        }

        return jsonify(response_object), 200

    except ValueError:
        return jsonify(response_object), 400


@users_blueprint.route("/users", methods=["GET"])
def get_users():
    """
    Returns a list of all users in the DB
    """

    response_obj = {
        "status": "success",
        "data": {"users": [user.to_json() for user in User.query.all()]},
    }
    return jsonify(response_obj), 200
