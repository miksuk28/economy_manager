from flask import Blueprint, jsonify, request
from wrappers import json_validator
from auth import Authentication
import auth_exceptions as exc
import json_schemas as schemas

authentication = Blueprint("authentication", __name__)
auth = Authentication()

@authentication.route("/", methods=["POST"])
@json_validator(schemas.login)
def login():
    data = request.get_json()

    try:
        session = auth.login(data["username"], data["password"])
        return jsonify(session)
    
    except exc.IncorrectPassword:
        return jsonify({"error": "Incorrect password. Please try signing in again"}), 403

    except exc.LoginBlocked:
        return jsonify({"error": f"{data['username']} is blocked from logging in. Contact the admin if you believe this is an error", "username": data["username"]}), 403


@authentication.route("/register", methods=["POST"])
@json_validator(schemas.register_user)
def register():
    data = request.get_json()
    try:
        id = auth.create_user(
            username=data["username"],
            password=data["password"],
            fname=data.get("fname"),
            lname=data.get("lname"),
            logon_allowed=data.get("logon_allowed", True)
        )

        return jsonify({"message": "User successfully created", "username": data["username"], "id": id}), 201

    except exc.UserAlreadyExists:
        return jsonify({"error": f"User {data['username']} already exists"}), 409