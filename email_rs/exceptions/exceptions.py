class EmailServerError(Exception):

    def __init__(self):
        self.message = "Email server general error"


class ParamsError(Exception):

    def __init__(self, message):
        self.message = message


class CustomError(Exception):
    """Custom exception class to be thrown when local error occurs."""
    def __init__(self, message, status=404):
        self.message = message
        self.status = status