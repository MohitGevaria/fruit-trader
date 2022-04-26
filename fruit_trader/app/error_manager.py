from flask import jsonify


class BaseError(Exception):
    """Base Error Class."""

    def __init__(
        self,
        status_code=400,
        message="",
        status="",
        error="",
    ):
        """Initialize."""
        Exception.__init__(self)
        self.status_code = status_code
        self.message = message
        self.status = status
        self.error = error

    def to_json(self):
        """Return the error in form of dict."""
        return jsonify({
            "status_code": self.status_code,
            "message": self.message,
            "status": self.status,
            "error": self.error,
        })


class BadRequestError(BaseError):
    """Handles Bad Request Error (400) from plugin."""

    def __init__(
        self,
        error="Bad Request",
        message="Bad Request",
    ):
        """Initialize."""
        BaseError.__init__(
            self, status_code=400, message=message, error=error
        )
        self.status_code = 400
        self.message = message
        self.error = error
        self.status = "failure"


class ServerError(BaseError):
    """Handles Internal Server Error (500) from plugin."""

    def __init__(
        self,
        error="Internal Server Error",
        message="Something went wrong; Please try again later.",
        status_code=502,
    ):
        """Initialize."""
        BaseError.__init__(
            self,
            status_code=status_code,
            message=message,
            error=error,
        )
        self.status_code = status_code
        self.message = message
        self.error = error
        self.status = "failure"


class NotFoundError(BaseError):
    """Handles Not Found Error (404) from plugin."""

    def __init__(
        self,
        error="Not Found",
        message="Entity not found",
    ):
        """Initialize."""
        BaseError.__init__(
            self, status_code=404, message=message, error=error
        )
        self.status_code = 404
        self.message = message
        self.error = error
        self.status = "failure"