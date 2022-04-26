"""File To run the server."""
from fruit_trader.app import create_app

app = create_app()


@app.errorhandler(404)
def invalid_route(e):
    return "Route not found", 404


if __name__ == '__main__':
    app.run()
