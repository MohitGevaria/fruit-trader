"""Routes for Profit and Remaining Quantity."""
from flask import Blueprint

from fruit_trader.app.utils.common_utility import tojson
from fruit_trader.app.utils.error_manager import ServerError
from fruit_trader.app.utils.singleton import Singleton

api = Blueprint("profit", __name__)

# object of data strucutre used as database to store orders.
db = Singleton.get_database_instance()


@api.route("/profit", methods=["GET"])
def get_profit():
    """Get Profit for overall orders."""
    try:
        profit = str(round(db.profit, 2))
        return tojson.response({"profit": profit, "status": "success", "status_code": "200"}, 200)
    except Exception:
        return ServerError(message="Unexpected Error Occured. Could Not Fetch Profit.").to_json(), 502


@api.route("/<string:fruit>", methods=["GET"])
def get_fruit_quantity(fruit):
    """Get available quantity of particular fruit."""
    try:
        if db.data.get(fruit.upper()):
            available_qty = db.data[fruit.upper()].quantity_available
            return tojson.response(
                {"Quantity Available": str(round(available_qty, 2)), "status": "success", "status_code": "200"}, 200
            )
        else:
            return tojson.response({"Quantity Available": str(0), "status": "success", "status_code": "200"}, 200)

    except Exception:
        return ServerError(message="Unexpected Error Occured").to_json(), 502
