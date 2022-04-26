"""Utility File for Routes."""

import re
from flask import make_response, jsonify


class Validations:
    """Validations for different routes."""

    def validation(self, fruit: str, price: float, quantity: float):
        """To perform validations on incoming data."""
        fruit_present = re.search(r"[\W]+", fruit)
        if fruit is None or fruit == "":
            return "Fruit Name cannot be empty.", False
        if fruit_present:
            return "Invalid Name for Fruit. No special characters allowed.", False
        if price is None:
            return "Price cannot be Empty."
        if not isinstance(price, float):
            return "Price should be a number.", False
        if price < 0:
            return "Price cannot be negative.", False
        if quantity is None:
            return "Quantity cannot be empty.", False
        if not isinstance(quantity, float):
            return "Quantity should be a number.", False
        if quantity <= 0:
            return "Quantity should be positive.", False
        return "Validated", True


class ToJson():
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
