"""Initialization of app."""
from flask import Flask
from fruit_trader.app.routes.trade_fruit import api as fruit_trade_api
from fruit_trader.app.routes.profit import api as profit_api


def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    app.register_blueprint(fruit_trade_api, url_prefix="/fruittrader")
    app.register_blueprint(profit_api, url_prefix="/fruittrader")
    return app
