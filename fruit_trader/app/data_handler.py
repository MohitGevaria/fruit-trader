"""Utility file for app."""


class Fruit:
    """
    The Fruit object contains a information about quantity and price of fruit.

    Args:
        buying_price (float): Buying Price of fruit.
        quantity (int): Quantity of fruit.
    """

    def __init__(self, buying_price: float, quantity: float):
        self.quantity = quantity
        self.buying_price = buying_price


class Queue:
    """
    The Queue is FIFO implelented to keep track of buy and sell orders.
    """

    def __init__(self):
        self.orders_list = []
        self.quantity_available = 0

    def insert(self, price: float, quantity: float):
        """
        Insert data into queue.
        Parameters:
            price (float): Buy/Sell price of Fruit.
            quantity (int): Quantity of Fruit.
        """
        self.orders_list.append(Fruit(price, quantity))
        self.quantity_available += quantity

    def update(self, req_quantity: float, sell_price: float):
        """
        Update data into queue.
        Parameters:
            price (float): Buy/Sell price of Fruit.
            req_quantity (int): Quantity of Fruit.

        Returns:
            profit(int):Profit earned after sell of Fruits.
        """
        profit = 0
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
        self.data = {}
        self.profit = 0

    def buy_order(self, name: str, buy_price: float, quantity: float):
        """
        Update data into queue.

        Parameters:
            name (str) : Name of the fruit.
            buy_price (float): Buy/Sell price of Fruit.
            quantity (int): Quantity of Fruit.
        Returns:
            (Status, msg)(bool, str):Returns Status and message for each status.
        """
        if name not in self.data:
            self.data[name] = Queue()

        self.data[name].insert(buy_price, quantity)

        # printing in console as per requirements.
        print(f"BOUGHT {round(quantity,2)} KG {name} AT {buy_price} RUPEES/KG.")
        return (True, f"BOUGHT {round(quantity,2)} KG {name} AT {round(buy_price,2)} RUPEES/KG.")

    def sell_order(self, name: str, sell_price: float, quantity: float):
        """
        Update data into queue.

        Parameters:
            name (str) : Name of the fruit.
            sell_price (float): Buy/Sell price of Fruit.
            quantity (int): Quantity of Fruit.
        Returns:
            (Status, msg)(bool, str):Returns Status and message for each status.
        """
        if name not in self.data:
            return (False, f"{name} Not Available in Sufficient Quantity. Available Quantity : 0")

        if self.data[name].quantity_available >= quantity:
            self.profit += self.data[name].update(quantity, sell_price)

            # printing in console as per requirements.
            print(f"SOLD {round(quantity,2)} KG {name} AT {sell_price} RUPEES/KG.")
            return (True, f"SOLD {round(quantity,2)} KG {name} AT {round(sell_price, 2)} RUPEES/KG.")

        else:
            return (
                False,
                f"{name} Not Available in Sufficient Quantity. Available Quantity : {round(self.data[name].quantity_available, 2)}",
            )


class Singleton:
    """The Singleton class."""

    __database = None

    def __init__(self):
        """Initialize database."""
        if not Singleton.__database:
            self.__database = Database()
            Singleton.__database = self.__database

    @staticmethod
    def get_database_instance():
        """Get database instance."""
        if Singleton.__database is None:
            Singleton()

        return Singleton.__database
