"""Routes for app."""
from flask import Blueprint, request

from fruit_trader.utils.utility import database
from fruit_trader.utils.routes_utility import validations

api = Blueprint("api", __name__)

# database object to store orders.
db = database()


@api.route("/buy", methods=["POST"])
def buy_fruits():
    """Place a Buy order for a fruit."""
    content_type = request.headers.get('Content-Type')
    try:
        if(content_type == "application/json"):
            data = request.get_json()
            fruit = data.get("fruit", None).upper()
            price = float(data.get("price", None))
            quantity = int(data.get("quantity", None))
        elif "multipart/form-data" in content_type:
            fruit = request.form.get("fruit").upper()
            price = float(request.form.get("price"))
            quantity = int(request.form.get("quantity"))
        else:
            return "Content Type not supported", 400
    except Exception:
        return "Unexpected Value Recieved", 400

    message, status = validations(fruit, price, quantity)
    if not status:
        return message, 400
    try:
        status, message = db.buy_order(fruit, price, quantity)
    except Exception:
        return "Unexpected Error Occured", 502

    if status:
        return message, 201
    return f"Could Not complete request due to : {message}", 400


@api.route("/sell", methods=["POST"])
def sell_fruits():
    """Place a Sell order for a fruit."""
    content_type = request.headers.get('Content-Type')
    try:
        if(content_type == "application/json"):
            data = request.get_json()
            fruit = data.get("fruit", None).upper()
            price = float(data.get("price", None))
            quantity = int(data.get("quantity", None))
        elif "multipart/form-data" in content_type:
            fruit = request.form.get("fruit").upper()
            price = float(request.form.get("price"))
            quantity = int(request.form.get("quantity"))
        else:
            return "Content Type not supported", 400
    except Exception:
        return "Unexpected Value Recieved", 400

    message, status = validations(fruit, price, quantity)
    if not status:
        return message, 400

    try:
        status, message = db.sell_order(fruit, price, quantity)
    except Exception:
        return "Unexpected Error Occured", 502
    if status:
        return message, 201
    return f"Could Not complete request due to : {message}", 400


@api.route("/profit", methods=["GET"])
def get_profit():
    """Get Profit for overall orders."""
    try:
        profit = str(db.profit)
    except Exception:
        return "Unexpected Error Occured. Could Not Fetch Profit.", 502
    return profit, 201
