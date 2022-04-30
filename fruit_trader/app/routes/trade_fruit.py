"""Routes for buy and sell."""
from flask import Blueprint, request

from fruit_trader.app.utils.fruit import Fruit
from fruit_trader.app.utils.common_utility import validate, tojson
from fruit_trader.app.utils.error_manager import BadRequestError, Error, NotFoundError, ServerError
from fruit_trader.app.utils.singleton import Singleton

api = Blueprint("fruit_trade", __name__)

# object of data strucutre used as database to store orders.
db = Singleton.get_database_instance()


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
        price = float(data.get("price", None))
        quantity = float(data.get("quantity", None))
        validate.validation(fruit, price, quantity)
    except Error as e:
        return BadRequestError(message=e.message).to_json(), 400
    except Exception:
        return BadRequestError(message="Unexpected Value Recieved").to_json(), 400
    try:
        fruit_object = Fruit(fruit, price, quantity)
        status, message = db.buy_order(fruit_object)
        if status:
            return tojson.response({"message": message, "status": "success", "status_code": "200"}, 201)
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
        price = float(data.get("price", None))
        quantity = float(data.get("quantity", None))
        validate.validation(fruit, price, quantity)

    except Error as e:
        return BadRequestError(message=e.message).to_json(), 400
    except Exception:
        return BadRequestError(message="Unexpected Value Recieved").to_json(), 400

    try:
        fruit_object = Fruit(fruit, price, quantity)
        status, message = db.sell_order(fruit_object)
        if status:
            return tojson.response({"message": message, "status": "success", "status_code": "200"}, 201)
        return BadRequestError(message=f"Could Not complete request due to : {message}").to_json(), 400
    except Exception:
        return ServerError(message="Unexpected Error Occured").to_json(), 502
