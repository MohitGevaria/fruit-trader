"""Routes for app."""
from urllib import response
from flask import Blueprint, request

from fruit_trader.app import data_handler as dh
from fruit_trader.app.utility import validate, tojson
from fruit_trader.app.error_manager import BadRequestError, NotFoundError, ServerError

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
            return BadRequestError(message="Content Type not supported").to_json(), 400

        if not data:
            return NotFoundError(message="Data not found").to_json(), 404

        fruit = data.get("fruit", None).upper()
        price = round(float(data.get("price", None)), 2)
        quantity = round(float(data.get("quantity", None)), 2)

        message, status = validate.validation(fruit, price, quantity)
        if not status:
            return BadRequestError(message=message).to_json(), 400
    except Exception:
        return BadRequestError(message="Unexpected Value Recieved").to_json(), 400
    try:
        status, message = db.buy_order(fruit, price, quantity)
        if status:
            return tojson.response({"message": message, "status": "success", "status_code" : "200"}, 201)
        return BadRequestError(message=f"Could Not complete request due to : {message}").to_json(), 400
    except Exception:
        return ServerError(message="Unexpected Error Occured").to_json(), 502


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
            return BadRequestError(message="Content Type not supported").to_json(), 400

        if not data:
            return NotFoundError(message="Data not found").to_json(), 404

        fruit = data.get("fruit", None).upper()
        price = round(float(data.get("price", None)), 2)
        quantity = round(float(data.get("quantity", None)), 2)

        message, status = validate.validation(fruit, price, quantity)

        if not status:
            return BadRequestError(message=message).to_json(), 400
    except Exception:
        return BadRequestError(message="Unexpected Value Recieved").to_json(), 400

    try:
        status, message = db.sell_order(fruit, price, quantity)
        if status:
            return tojson.response({"message": message, "status": "success", "status_code" : "200"}, 201)
        return BadRequestError(message=f"Could Not complete request due to : {message}").to_json(), 400
    except Exception:
        return ServerError(message="Unexpected Error Occured").to_json(), 502


@api.route("/profit", methods=["GET"])
def get_profit():
    """Get Profit for overall orders."""
    try:
        profit = str(round(db.profit, 2))
        return tojson.response({"profit": profit, "status": "success", "status_code" : "200"}, 200)
    except Exception:
        return ServerError(message="Unexpected Error Occured. Could Not Fetch Profit.").to_json(), 502


@api.route("/<string:fruit>", methods=["GET"])
def get_fruit_quantity(fruit):
    """Get available quantity of particular fruit."""
    try:
        if db.data.get(fruit.upper()):
            available_qty = db.data[fruit.upper()].quantity_available
            return tojson.response({"Quantity Available": str(round(available_qty, 2)), "status": "success", "status_code" : "200"}, 200)
        else:
            return tojson.response({"Quantity Available": str(0), "status": "success", "status_code" : "200"}, 200)

    except Exception:
        return ServerError(message="Unexpected Error Occured").to_json(), 502
