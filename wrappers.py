from functools import wraps
from flask import jsonify, request
from jsonschema import validate, ValidationError
from auth import Authentication
import auth_exceptions as auth_exc

auth = Authentication()

def json_validator(schema, *args, **kwargs):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json_data = request.get_json()

            if json_data == {}:
                return jsonify({"error": "No JSON body"}), 400

            try:
                validate(instance=json_data, schema=schema)
            except ValidationError as e:
                return jsonify({"error": "JSON Validation error", "errorMessage": e.message, "expectedSchema": schema}), 400

            return f(*args, **kwargs)
        return wrapper
    return decorator


def authenticate(*args, **kwargs):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_token = request.headers.get("Authentication")
            if auth_token in ("", None):
                return jsonify({"error": "Missing Authentication header containing token"}), 400

            try:
                session = auth.auth(auth_token)
                            
            except auth_exc.InvalidToken:
                return jsonify({"error": "Authentication token is incorrect. Please sign in again"}), 403

            except auth_exc.TokenExpired:
                return jsonify({"error": "Authentication token has expired. Please sign in again."}), 403
            
            return f(session=session, *args, **kwargs)
        return wrapper
    return decorator