"""Utility file for app."""

class fruit:
    def __init__(self, buying_price, quantity):
        self.quantity = quantity
        self.buying_price = buying_price
    
class queue:
    def __init__(self):
        self.trading_list = []
        self.running_quantity = 0
    
    def insert(self, price, quantity):
        self.trading_list.append(fruit(price,quantity))
        self.running_quantity += quantity 


    def update(self, req_quantity, sell_price):
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
    def __init__(self):
        self.data = {}
        self.profit = 0

    def buy_order(self, name, buy_price, quantity):
        if name not in self.data:
            self.data[name] = queue()
        
        self.data[name].insert(buy_price, quantity)

    def sell_order(self, name, sell_price, quantity):
        if name not in self.data:
            print("No Quantity")

        if self.data[name].running_quantity >= quantity:
            self.profit += self.data[name].update(quantity, sell_price)
        
        else:
            print("Insufficient Quantity")
        
    def printing(self):
        for i in self.data:
            for j in self.data[i].trading_list:
                print(i, j.buying_price, j.quantity, )
        
        print("profit = ", (self.profit))
