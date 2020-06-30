class CustomError(Exception):
    """Custom exception class to be thrown when local error occurs."""
    def __init__(self, message):
        self.message = message