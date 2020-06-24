from repositories import user_repository
from flask_jwt_extended import create_access_token
import datetime
from exceptions import exceptions


def register_user(username, password, role):
    user_repository.create_user(username, password, role)


def login_user(username, password):
    try:
        user = get_user(username)
    except exceptions.UserNotFound:
        raise exceptions.InvalidUsernameOrPassword
    if not user.check_password(password):
        raise exceptions.InvalidUsernameOrPassword
    else:
        expires = datetime.timedelta(days=7)
        return create_access_token(identity=str(username), expires_delta=expires)


def get_user(username):
    return user_repository.get_user(username)


def is_admin(username):
    user = get_user(username)
    return user.role == "admin"

