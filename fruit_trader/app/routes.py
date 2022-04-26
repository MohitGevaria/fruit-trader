"""Routes for app."""
from urllib import response
from flask import Blueprint, request

from fruit_trader.app import data_handler as dh
from fruit_trader.app.utility import validate, tojson
api = Blueprint("api", __name__)

# object of data strucutre used as database to store orders.
db = dh.Singleton.get_database_instance()


@api.route("/buy", methods=["POST"])
def buy_fruits():
    """Place a Buy order for a fruit."""
    try:
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            data = request.get_json()
        elif "multipart/form-data" in content_type:
            data = request.form
        else:
            return tojson.tojson.response({"message": "Content Type not supported", "result": "error"}, 400)

        fruit = data.get("fruit", None).upper()
        price = float(data.get("price", None))
        quantity = float(data.get("quantity", None))

        message, status = validate.validation(fruit, price, quantity)
        if not status:
            return tojson.response({"message": message, "result": "error"}, 400)
    except Exception:
        return tojson.response({"message": "Unexpected Value Recieved", "result": "error"}, 400)
    try:
        status, message = db.buy_order(fruit, price, quantity)
        if status:
            return tojson.response({"message": message, "result": "success"}, 201)
        return tojson.response({"message": f"Could Not complete request due to : {message}", "result": "error"}, 400)
    except Exception:
        return tojson.response({"message": "Unexpected Error Occured", "result": "error"}, 502)


@api.route("/sell", methods=["POST"])
def sell_fruits():
    """Place a Sell order for a fruit."""
    try:
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            data = request.get_json()
        elif "multipart/form-data" in content_type:
            data = request.form
        else:
            return tojson.response({"message": "Content Type not supported", "result": "error"}, 400)

        fruit = data.get("fruit", None).upper()
        price = float(data.get("price", None))
        quantity = float(data.get("quantity", None))
        message, status = validate.validation(fruit, price, quantity)

        if not status:
            return tojson.response({"message": message, "result": "error"}, 400)
    except Exception:
        return tojson.response({"message": "Unexpected Value Recieved", "result": "error"}, 400)

    try:
        status, message = db.sell_order(fruit, price, quantity)
        if status:
            return tojson.response({"message": message, "result": "success"}, 201)
        return tojson.response({"message": f"Could Not complete request due to : {message}", "result": "error"}, 400)
    except Exception:
        return tojson.response({"message": "Unexpected Error Occured", "result": "error"}, 502)


@api.route("/profit", methods=["GET"])
def get_profit():
    """Get Profit for overall orders."""
    try:
        profit = str(round(db.profit, 2))
        return tojson.response({"profit": profit, "result": "success"}, 200)
    except Exception:
        return tojson.response({"message": "Unexpected Error Occured. Could Not Fetch Profit.", "result": "error"}, 502)


@api.route("/<string:fruit>", methods=["GET"])
def get_fruit_quantity(fruit):
    """Get available quantity of particular fruit."""
    try:
        if db.data.get(fruit.upper()):
            available_qty = db.data[fruit.upper()].quantity_available
            return tojson.response({"Quantity Available": str(available_qty), "result": "success"}, 200)
        else:
            return tojson.response({"Quantity Available": str(0), "result": "success"}, 200)

    except Exception:
        return tojson.response({"message": "Unexpected Error Occured", "result": "error"}, 502)
