from flask import Blueprint, request
from services import item_service
from exceptions import exceptions
from dtos.mappers import item_mapper
from check_params.check_params import check_parameters

bp = Blueprint('items', __name__)


@bp.route('/items', methods=('GET',))
def get_items():
    try:
        items = item_service.get_items()
    except exceptions.ItemNotFoundException:
        return "", 404
    except exceptions.StorageServerError:
        return "", 500

    return item_mapper.get_items(items), 200


@bp.route('/items/<item_id>', methods=('GET',))
def get_item(item_id):
    try:
        item = item_service.get_item(item_id)
    except exceptions.ItemNotFoundException:
        return "", 404
    except exceptions.StorageServerError:
        return "", 500
    return item_mapper.get_item(item), 200


@bp.route('/items', methods=('POST',))
def create_item():
    body = request.get_json()

    required_params = ["name", "description", "price", "supplier", "category"]
    try:
        check_parameters(params=body, required=required_params, possible=required_params)
    except exceptions.ParamsError as e:
        return {"message": e.message}, 400

    try:
        item_id = item_service.create_item(**body)
    except exceptions.ItemAlreadyExists:
        return {"message": "There is already an item with the name " + body['name']}, 400
    except exceptions.BadRequest as e:
        return e.message, 400
    except exceptions.StorageServerError:
        return "", 500

    return {"item_id": item_id}, 201


@bp.route('/items/<item_id>', methods=('DELETE',))
def delete_item(item_id):
    try:
        item_service.delete_item(item_id, request.headers.environ.get('HTTP_AUTHORIZATION'))
    except exceptions.ItemNotFoundException:
        return "", 404
    except exceptions.NotAnAdmin:
        return {"message": "Only admin users can perform this operation"}, 401
    except exceptions.StorageServerError:
        return "", 500
    except exceptions.UserAuthServerError:
        return "", 500
    return "", 200


@bp.route('/items/<item_id>', methods=('PUT',))
def update_item(item_id):
    body = request.get_json()
    possible_params = ["name", "description", "price", "supplier", "category"]
    try:
        check_parameters(params=body, possible=possible_params)
    except exceptions.ParamsError as e:
        return {"message": e.message}, 400

    try:
        item_updated = item_service.update_item(item_id, request.headers.environ.get('HTTP_AUTHORIZATION'), **body)
    except exceptions.ItemNotFoundException:
        return "", 404
    except exceptions.NotAnAdmin:
        return {"message": "Only admin users can perform this operation"}, 401
    except exceptions.BadRequest as e:
        return e.message, 400
    except exceptions.StorageServerError:
        return "", 500
    except exceptions.UserAuthServerError:
        return "", 500

    return item_mapper.get_item(item_updated), 200

