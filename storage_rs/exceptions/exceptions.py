class ItemNotFoundException(Exception):

    def __init__(self):
        self.message = "The item was not found in the DB"


class CartNotFoundException(Exception):

    def __init__(self):
        self.message = "The cart was not found in the DB"


class UserHasCartException(Exception):

    def __init__(self):
        self.message = "The user already has a cart created"


class UsernameAlreadyRegistered(Exception):

    def __init__(self):
        self.message = "The username is not available"


class InvalidUsernameOrPassword(Exception):

    def __init__(self):
        self.message = "Invalid username or password"


class PaymentError(Exception):

    def __init__(self):
        self.message = "Payment error"


class ItemAlreadyExists(Exception):

    def __init__(self):
        self.message = "There is already an item with that name"


class UserNotFoundException(Exception):

    def __init__(self):
        self.message = "The user was not found in the DB"


class NotAnAdmin(Exception):
    pass


class ParamsError(Exception):

    def __init__(self, message):
        self.message = message


class CustomError(Exception):
    """Custom exception class to be thrown when local error occurs."""
    def __init__(self, message, status=404):
        self.message = message
        self.status = status