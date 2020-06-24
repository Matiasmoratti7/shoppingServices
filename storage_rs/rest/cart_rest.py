from flask import Blueprint, request
from services import cart_service
from exceptions import exceptions
from dtos.mappers import cart_mapper
from check_params.check_params import check_parameters


bp = Blueprint('carts', __name__)


@bp.route('/carts', methods=('POST',))
def create_cart():
    cart_id = cart_service.create_cart()
    return {"cart_id": str(cart_id)}, 201


@bp.route('/carts/<cart_id>', methods=('GET',))
def get_cart(cart_id):
    try:
        cart = cart_service.get_cart(cart_id)
    except exceptions.CartNotFoundException:
        return "", 404
    return cart_mapper.get_cart(cart), 200


@bp.route('/carts/<cart_id>/items/<item_id>', methods=('POST',))
def add_item(cart_id, item_id):
    try:
        cart = cart_service.add_item_to_cart(cart_id, item_id)
    except exceptions.CartNotFoundException:
        return {"message": "Cart " + str(cart_id) + " not found"}, 404
    except exceptions.ItemNotFoundException:
        return {"message": "Item " + str(item_id) + " not found"}, 404
    return cart_mapper.get_cart(cart), 200


@bp.route('/carts/<cart_id>', methods=('PUT',)) #Duda 5
def update_cart(cart_id):
    body = request.get_json()

    possible_params = ["status","payment_method","total_amount","username"]
    try:
        check_parameters(params=body, required=possible_params, possible=possible_params)
    except exceptions.ParamsError as e:
        return {"message": e.message}, 400
    try:
        cart = cart_service.update_cart(cart_id, **body)
    except exceptions.CartNotFoundException:
        return "", 404
    return cart_mapper.get_cart(cart), 200


@bp.route('/carts/<cart_id>', methods=('DELETE',))
def cancel_cart(cart_id):
    try:
        cart_service.cancel_cart(cart_id)
    except exceptions.CartNotFoundException:
        return {"message": "Cart " + str(cart_id) + " not found"}, 404
    return {"message": "Cart " + str(cart_id) + " canceled."}