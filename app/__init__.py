
from flask import Flask, request
import re
from sqlalchemy import create_engine
from fruit_trader.utility import database
import os

POSTGRES_URL = os.get_evn("POSTGRES_URL")
engine = create_engine(POSTGRES_URL)
db = engine.connect()

app = Flask(__name__)

@app.route("/fruittrader/buy", methods = ["POST"])
def buy_fruits():
    fruit = request.form.get("fruit")
    price = float(request.form.get("price"))
    quantity = int(request.form.get("quantity"))
    fruit_present = re.match("\w+", fruit)
    if fruit is None or not fruit_present:
        return "Fruit is Not available.", 400
    if price <= 0 or price is None:
        return "Price is Not Valid.", 400
    if quantity <= 0 or quantity is None:
        return "Price is Not Valid.", 400
    results = (db.engine.execute(f"insert into buy_orders (fruit, price, quantity, remaining_quantity) values ('{fruit}', {price}, {quantity}, {quantity})"))
    return "Buy Order Placed", 201


@app.route("/fruittrader/sell", methods=["POST"])
def sell_fruits():
    fruit = request.form.get("fruit")
    price = float(request.form.get("price"))
    quantity = int(request.form.get("quantity"))
    fruit_present = re.match("\w+", fruit)
    if fruit is None or not fruit_present:
        return "Fruit is Not available.", 400
    if price <= 0 or price is None:
        return "Price is Not Valid.", 400
    if quantity <= 0 or quantity is None:
        return "Price is Not Valid.", 400
    quantity_available = list(db.engine.execute(f"select sum(remaining_quantity) from buy_orders where fruit = '{fruit}';"))[0][0]
    
    if quantity_available is None or quantity_available < quantity:
        return "Not sufficient quantity Available", 200

    buy_orders = db.engine.execute(f"select * from buy_orders where fruit = '{fruit}' and remaining_quantity > 0 order by created_at asc;")
    rem_quantity = quantity;
    orders_to_update = []
    for each_order in buy_orders:
        orders_to_update.append((each_order[0], max(each_order[5]-rem_quantity, 0)))
        rem_quantity = rem_quantity - each_order[5]
        
        if(rem_quantity <=0):
            break
    
    for each_update in orders_to_update:
        db.engine.execute(f"insert into sell_orders (price, quantity, buy_id) values ({price}, {each_update[1]}, {each_update[0]});")
        db.engine.execute(f"update buy_orders set remaining_quantity={each_update[1]} where id={each_update[0]};")
        
    return "Sell Order Placed.", 201


@app.route("/fruittrader/profit")
def get_profit():
    profit = 0
    profit_cal = list(db.engine.execute(f"select sum((orders.selling_price - orders.buying_price)* orders.selling_quantity) from (select bo.price as buying_price, so.price as selling_price, bo.fruit, bo.quantity as buying_quantity, so.quantity as selling_quantity from sell_orders so inner join buy_orders bo on bo.id = so.buy_id) as orders;"))
    if profit_cal[0][0] is not None:
        profit = profit_cal[0][0]
    return str(profit), 200


if __name__ == "__main__":
    app.run()