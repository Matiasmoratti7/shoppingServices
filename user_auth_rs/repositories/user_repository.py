from exceptions import exceptions
from model.user import User
from mongoengine import NotUniqueError


def create_user(username, password, role):
    user = User(username=username, password=password, role=role)
    user.hash_password()
    try:
        user.save()
    except NotUniqueError:
        raise exceptions.UsernameAlreadyRegistered()


def get_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise exceptions.UserNotFound()
    return user

