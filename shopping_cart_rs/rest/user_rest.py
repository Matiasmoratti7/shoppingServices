from flask import Blueprint, request
from services import user_service
from check_params.check_params import check_parameters
from exceptions import exceptions

bp = Blueprint('users', __name__)


@bp.route('/users/register', methods=('POST',))
def register_user():
    body = request.get_json()

    possible_params = ['username', 'password', 'role']
    try:
        check_parameters(params=body, required=possible_params, possible=possible_params)
    except exceptions.ParamsError as e:
        return {"message": e.message}, 400

    try:
        user_service.register_user(body['username'], body['password'], body['role'])
    except exceptions.BadRequest as e:
        return e.message, 400
    except exceptions.UserAuthServerError:
        return "", 500

    return "", 201


@bp.route('/users/login', methods=('POST',))
def login_user():
    body = request.get_json()

    possible_params = ['username', 'password']
    try:
        check_parameters(params=body, required=possible_params, possible=possible_params)
    except exceptions.ParamsError as e:
        return {"message": e.message}, 400

    try:
        token = user_service.login_user(body['username'], body['password'])
    except exceptions.InvalidUsernameOrPassword:
        return {"message": "Invalid username or password"}, 400
    except exceptions.UserAuthServerError:
        return "", 500
    return {'token': token}, 200

