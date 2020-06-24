from flask import Blueprint, request
from services import user_service
from exceptions import exceptions
from check_params.check_params import check_parameters
from dtos.mappers.user_mapper import UserMapper
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    except exceptions.UsernameAlreadyRegistered:
        return {"message": "Username " + body['username'] + " is already in used."}, 400
    return "", 201


@bp.route('/users/login', methods=('POST',))
def login_user():
    body = request.get_json()

    possible_params = ['username', 'password']
    try:
        check_parameters(params=body, required=possible_params, possible=possible_params)
    except exceptions.ParamsError as e:
        return {"message": e.message}, 400

    username = body['username']
    password = body['password']
    try:
        access_token = user_service.login_user(username, password)
    except exceptions.InvalidUsernameOrPassword:
        return {"message": "Invalid username or password"}, 400
    return {
            'token': access_token
           }, 200


@bp.route('/users/<username>', methods=('GET',))
def get_user(username):
    try:
        user = user_service.get_user(username)
    except exceptions.UserNotFound:
        return 400
    return UserMapper.map_to_dto(user), 200


@bp.route('/users/admin', methods=('GET',))
@jwt_required
def check_admin():
    username = get_jwt_identity()
    try:
        return {"admin": str(user_service.is_admin(username))}, 200
    except exceptions.UserNotFound:
        return "", 404


@bp.route('/users/logged', methods=('GET',))
@jwt_required
def user_logged():
    username = get_jwt_identity()
    return {"user": username}, 200