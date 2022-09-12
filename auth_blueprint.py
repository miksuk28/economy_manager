from flask import Blueprint, jsonify, request
from wrappers import json_validator
from auth import Authentication
import auth_exceptions as exc
import json_schemas as schemas

authentication = Blueprint("authentication", __name__)
auth = Authentication()

@authentication.route("/", methods=["POST"])
def login():
    pass

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