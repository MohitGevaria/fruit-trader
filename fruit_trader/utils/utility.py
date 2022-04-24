"""Utility file for app."""

class fruit:
    """
    The Fruit object contains a information about quantity and price of fruit.

    Args:
        buying_price (float): Buying Price of fruit.
        quantity (int): Quantity of fruit.
    """
    def __init__(self, buying_price, quantity):
        self.quantity = quantity
        self.buying_price = buying_price

    
class queue:
    """
    The Queue is FIFO implelented to keep track of buy and sell orders.
    """
    def __init__(self):
        self.trading_list = []
        self.running_quantity = 0

    
    def insert(self, price, quantity):
        """
        Insert data into queue.
        Parameters:
            price (float): Buy/Sell price of Fruit.
            quantity (int): Quantity of Fruit.
        """
        self.trading_list.append(fruit(price,quantity))
        self.running_quantity += quantity


    def update(self, req_quantity, sell_price):
        """"
        Update data into queue.
        Parameters:
            price (float): Buy/Sell price of Fruit.
            req_quantity (int): Quantity of Fruit.

        Returns:
            profit(int):Profit earned after sell of Fruits.
        """
        profit = 0
        while(req_quantity > 0):
            if self.trading_list[0].quantity-req_quantity > 0:
                profit += (sell_price - self.trading_list[0].buying_price) * req_quantity
                self.trading_list[0].quantity -= req_quantity
                self.running_quantity -= req_quantity
                req_quantity = 0
            else:
                profit += (sell_price - self.trading_list[0].buying_price) * self.trading_list[0].quantity
                self.running_quantity -= self.trading_list[0].quantity
                req_quantity -= self.trading_list.pop(0).quantity
        
        return profit

class database:
    """
    The database object is used to store queues for different fruits.
    
    Attributes:
        data (list): map of queues to store data,
        profit (int): Profit Value calculated after sell orders. 
    """
    def __init__(self):
        self.data = {}
        self.profit = 0

    def buy_order(self, name, buy_price, quantity):
        """"
        Update data into queue.

        Parameters:
            name (str) : Name of the fruit.
            buy_price (float): Buy/Sell price of Fruit.
            quantity (int): Quantity of Fruit.
        Returns:
            (Status, msg)(bool, str):Returns Status and message for each status.
        """
        if name not in self.data:
            self.data[name] = queue()
        
        self.data[name].insert(buy_price, quantity)

        return (True, "Buy Order Placed")

    def sell_order(self, name, sell_price, quantity):
        """"
        Update data into queue.

        Parameters:
            name (str) : Name of the fruit.
            sell_price (float): Buy/Sell price of Fruit.
            quantity (int): Quantity of Fruit.
        Returns:
            (Status, msg)(bool, str):Returns Status and message for each status.
        """
        if name not in self.data:
            return (False, "Fruit Not Available.")

        if self.data[name].running_quantity >= quantity:
            self.profit += self.data[name].update(quantity, sell_price)
            return (True, "Sell Order Placed.")

        else:
            return (False, "Fruit Not Available in Sufficient Quantity.")
