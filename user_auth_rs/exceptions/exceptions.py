class UsernameAlreadyRegistered(Exception):

    def __init__(self):
        self.message = "The username is not available"


class InvalidUsernameOrPassword(Exception):

    def __init__(self):
        self.message = "Invalid username or password"


class UserNotFound(Exception):

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