from flask import Flask, jsonify, request, render_template
from wrappers import json_validator
from economy import EconomyManager
import json_schemas as schemas
import eco_exceptions as exc_eco

from pprint import pprint


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
eco = EconomyManager()

# TESTING
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", receipts=eco.get_all_receipts())


@app.route("/receipt", methods=["POST"])
@json_validator(schemas.create_receipt)
def create_receipt():
    data = request.get_json()
    id = eco.create_receipt(
        items=data["products"],
        store=data.get("store"),
        comment=data.get("comment"),
    )
    for i, product in enumerate(data["products"]):
        data["products"][i]["receipt_id"] = id


    return jsonify({"message": f"Receipt created with id {id}", "id": id, "data": data}), 201


@app.route("/receipts", methods=["GET"])
def get_all_receipts():
    return jsonify(eco.get_all_receipts()), 200
    


@app.route("/receipt/<int:id>", methods=["DELETE"])
def delete_receipt(id):
    try:
        affected_rows = eco.delete_receipt(id)
        return jsonify({
            "message": f"Deleted receipt with id {id}",
            "id": id,
            "affectedRows": affected_rows
        }), 200

    except exc_eco.ReceiptDoesNotExist:
        return jsonify({"error": f"Receipt with id {id} does not exist", "id": id}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)