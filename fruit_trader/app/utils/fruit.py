"""Provides a class for fruit related functionalities."""


class Fruit:
    """
    The Fruit object contains a information about quantity and price of fruit.

    Args:
        buying_price (float): Buying Price of fruit.
        quantity (int): Quantity of fruit.
    """

    def __init__(self, fruit: str, buying_price: float, quantity: float):
        """To initialzie Fruit Object."""
        self.name = fruit
        self.quantity = round(quantity, 2)
        self.buying_price = round(buying_price, 2)

    def get_quantity(self):
        """To get quantity."""
        return round(self.quantity, 2)

    def get_price(self):
        """To get price."""
        return round(self.buying_price, 2)

    def get_fruit_name(self):
        """To get fruit name."""
        return self.name
