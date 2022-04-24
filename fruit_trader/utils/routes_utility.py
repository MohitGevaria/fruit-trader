"""Utility File for Routes."""

import re


def validations(fruit, price, quantity):
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
    if not isinstance(quantity, int):
        return "Quantity should be a number.", False
    if quantity <= 0:
        return "Quantity should be positive.", False
    return "Validated", True
