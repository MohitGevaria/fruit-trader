"""Class provides printing different messages."""
from fruit_trader.app.utils.fruit import Fruit


class PrintStatus():
    """To print buy and sell status."""

    @staticmethod
    def buy_response(fruit: Fruit):
        """To Return buy message."""
        return f"BOUGHT {fruit.get_quantity()} KG {fruit.get_fruit_name()} AT {fruit.get_price()} RUPEES/KG."

    @staticmethod
    def sell_response(fruit: Fruit):
        """To Return sell message."""
        return f"SOLD {fruit.get_quantity()} KG {fruit.get_fruit_name()} AT {fruit.get_price()} RUPEES/KG."

    @staticmethod
    def insufficient_quantity_msg(name, available_qty):
        """To Return insufficient quantity message."""
        return f"{name} Not Available in Sufficient Quantity. Available Quantity : {round(available_qty, 2)}"
