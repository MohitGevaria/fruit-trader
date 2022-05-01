"""Utility file for app."""
from fruit_trader.app.utils.fruit import Fruit
from fruit_trader.app.utils.print_helper import PrintStatus


class Queue:
    """The Queue is FIFO implelented to keep track of buy and sell orders."""

    def __init__(self):
        """To Initialize Queue object."""
        self.orders_list = []
        self.quantity_available = 0

    def insert(self, fruit: Fruit):
        """
        Insert data into queue.
        Parameters:
            price (float): Buy/Sell price of Fruit.
            quantity (int): Quantity of Fruit.
        """
        self.orders_list.append(fruit)
        self.quantity_available += fruit.get_quantity()

    def update(self, fruit: Fruit):
        """
        Update data into queue.
        Parameters:
            price (float): Buy/Sell price of Fruit.
            req_quantity (int): Quantity of Fruit.

        Returns:
            profit(int):Profit earned after sell of Fruits.
        """
        profit = 0
        req_quantity = fruit.get_quantity()
        sell_price = fruit.get_price()

        while req_quantity > 0:
            if self.orders_list[0].quantity - req_quantity > 0:
                profit += (sell_price - self.orders_list[0].buying_price) * req_quantity
                self.orders_list[0].quantity -= req_quantity
                self.quantity_available -= req_quantity
                req_quantity = 0
            else:
                profit += (sell_price - self.orders_list[0].buying_price) * self.orders_list[0].quantity
                self.quantity_available -= self.orders_list[0].quantity
                req_quantity -= self.orders_list.pop(0).quantity

        return profit


class Database:
    """
    The database object is used to store queues for different fruits.

    Attributes:
        data (list): map of queues to store data,
        profit (int): Profit Value calculated after sell orders.
    """

    def __init__(self):
        """To Initialize Database object."""
        self.data = {}
        self.profit = 0

    def buy_order(self, fruit: Fruit):
        """
        Update data into queue.

        Parameters:
            name (str) : Name of the fruit.
            buy_price (float): Buy/Sell price of Fruit.
            quantity (int): Quantity of Fruit.
        Returns:
            (Status, msg)(bool, str):Returns Status and message for each status.
        """

        if fruit.get_fruit_name() not in self.data:
            self.data[fruit.get_fruit_name()] = Queue()

        self.data[fruit.get_fruit_name()].insert(fruit)

        # printing in console as per requirements.
        print(PrintStatus.buy_response(fruit))
        return (True, PrintStatus.buy_response(fruit))

    def sell_order(self, fruit: Fruit):
        """
        Update data into queue.

        Parameters:
            name (str) : Name of the fruit.
            sell_price (float): Buy/Sell price of Fruit.
            quantity (int): Quantity of Fruit.
        Returns:
            (Status, msg)(bool, str):Returns Status and message for each status.
        """
        if fruit.get_fruit_name() not in self.data:
            return (False, PrintStatus.insufficient_quantity_msg(fruit.get_fruit_name(), 0))

        if self.data[fruit.get_fruit_name()].quantity_available >= fruit.get_quantity():
            self.profit += self.data[fruit.get_fruit_name()].update(fruit)

            # printing in console as per requirements.
            print(PrintStatus.sell_response(fruit))
            return (True, PrintStatus.sell_response(fruit))

        else:
            return (
                False,
                PrintStatus.insufficient_quantity_msg(
                    fruit.get_fruit_name(), self.data[fruit.get_fruit_name()].quantity_available
                ),
            )
