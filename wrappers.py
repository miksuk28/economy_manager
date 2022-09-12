from functools import wraps
from flask import jsonify, request
from jsonschema import validate, ValidationError


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