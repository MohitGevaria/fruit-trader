"""Utility File for Routes."""

import re
from flask import make_response, jsonify
from fruit_trader.app.utils.error_manager import (
    FruitNameNotFoundError,
    FruitNameNotValidError,
    PriceEmptyError,
    PriceNegativeError,
    PriceNotValidError,
    QuantityEmptyError,
    QuantityNegativeError,
    QuantityNotValidError,
)


class Validations:
    """Validations for different routes."""

    def validation(self, fruit: str, price: float, quantity: float):
        """To perform validations on incoming data."""
        fruit_present = re.search(r"[\W]+", fruit)
        if fruit is None or fruit == "":
            raise FruitNameNotFoundError()
        if fruit_present:
            raise FruitNameNotValidError()
        if price is None:
            raise PriceEmptyError()
        if not isinstance(price, float):
            raise PriceNotValidError()
        if price < 0:
            raise PriceNegativeError()
        if quantity is None:
            raise QuantityEmptyError()
        if not isinstance(quantity, float):
            raise QuantityNotValidError()
        if quantity <= 0:
            raise QuantityNegativeError()


class ToJson:
    """Convert Response to JSON."""

    def response(self, data: dict, status: int, headers={}):
        """Return response."""
        return make_response(
            jsonify(data) if isinstance(data, dict) or isinstance(data, list) else data,
            status,
            {**headers, "Content-Type": "application/json"},
        )


validate = Validations()
tojson = ToJson()
