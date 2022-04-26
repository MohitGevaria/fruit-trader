"""Initialization of app."""
from flask import Flask


def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    from fruit_trader.app.routes import api
    app.register_blueprint(api, url_prefix="/fruittrader")

    return app
