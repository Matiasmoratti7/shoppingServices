import requests
from exceptions import exceptions
from config import config


def register_user(username, password, role):
    try:
        response = requests.post(config.endpoints.user_register, json={"username": username, "password": password,
                                                            "role": role})
    except Exception:
        raise exceptions.UserAuthServerError()
    if response.status_code == 400:
        raise exceptions.BadRequest(response.text)
    elif response.status_code != 201:
        raise exceptions.UserAuthServerError()


def login_user(username, password):
    try:
        response = requests.post(config.endpoints.user_login, json={"username": username, "password": password})
    except Exception:
        raise exceptions.UserAuthServerError()
    if response.status_code == 400:
        raise exceptions.InvalidUsernameOrPassword()
    elif response.status_code != 200:
        raise exceptions.UserAuthServerError()
    else:
        return response.json()['token']


def valid_admin(token):
    try:
        response = requests.get(config.endpoints.user_admin, headers={"Authorization": token})
    except Exception:
        raise exceptions.UserAuthServerError()
    if response.status_code == 200:
        return response.json()['admin'] == 'True'
    else:
        raise exceptions.UserAuthServerError()


def user_logged(token):
    try:
        response = requests.get(config.endpoints.user_logged, headers={"Authorization": token})
    except Exception:
        raise exceptions.UserAuthServerError()
    if response.status_code == 200:
        return response.json()['user']
    else:
        return None