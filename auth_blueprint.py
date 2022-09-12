from flask import Blueprint, jsonify, request

authentication = Blueprint("authentication", __name__)

@authentication.route("/", methods=["POST"])
def login():
    pass