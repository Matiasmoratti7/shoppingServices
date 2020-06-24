from flask import Blueprint, request
from services import cart_service
from exceptions import exceptions
from dtos.mappers import cart_mapper
from check_params.check_params import check_parameters


bp = Blueprint('carts', __name__)


@bp.route('/carts', methods=('POST',))
def create_cart():
    try:
        cart_id = cart_service.create_cart()
    except exceptions.UserHasCartException as e:
        return {"message": e.message}, 400
    except exceptions.StorageServerError:
        return "", 500
    return {"CartID": str(cart_id)}, 201


@bp.route('/carts/<cart_id>', methods=('GET',))
def get_cart(cart_id):
    try:
        cart = cart_service.get_cart(cart_id)
    except exceptions.CartNotFoundException:
        return "", 404
    except exceptions.StorageServerError:
        return "", 500
    return cart_mapper.get_cart(cart)


@bp.route('/carts/<cart_id>/items/<item_id>', methods=('POST',))
def add_item(cart_id, item_id):
    try:
        cart = cart_service.add_item_to_cart(cart_id, item_id)
    except exceptions.CartOrItemNotFoundException as e:
        return {"message": e.message}, 404
    except exceptions.StorageServerError:
        return "", 500
    return cart_mapper.get_cart(cart), 200


@bp.route('/carts/<cart_id>', methods=('PUT',))
def checkout_cart(cart_id):
    body = request.get_json()

    required_params = ["payment_method"]
    try:
        check_parameters(params=body, required=required_params, possible=required_params)
    except exceptions.ParamsError as e:
        return {"message": e.message}, 400

    try:
        cart = cart_service.checkout_cart(body, cart_id, request.headers.environ.get('HTTP_AUTHORIZATION'))
    except exceptions.PaymentError:
        return {"message": "Payment error"}, 500
    except exceptions.CartNotFoundException:
        return "", 404
    except (exceptions.StorageServerError, exceptions.UserAuthServerError):
        return "", 500
    except exceptions.InvalidPaymentMethod:
        return {"message": "Invalid payment method " + body['payment_method']}, 400
    return cart_mapper.get_cart(cart), 200


@bp.route('/carts/<cart_id>', methods=('DELETE',))
def cancel_cart(cart_id):
    try:
        cart_service.cancel_cart(cart_id)
    except exceptions.CartNotFoundException:
        return "", 404
    return "", 200

