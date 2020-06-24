from exceptions import exceptions
from . import item_repository
from model.cart import Cart


def create_cart():
    cart = Cart(status="shopping", items=[], total_amount=0).save()
    return cart.id


def get_cart(cart_id):
    try:
        return Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        raise exceptions.CartNotFoundException()


def user_has_cart(username):
    try:
        cart = Cart.objects.get(username=username)
    except Cart.DoesNotExist:
        return False
    return cart


def get_cart_items(cart_id):
    return Cart.objects.get(id=cart_id).items


def add_item_to_cart(cart_id, item_id):
    cart = get_cart(cart_id)  # Valido si existe el carrito sino se propaga la excepción
    item = item_repository.get_item(item_id)  # Valido si existe el item sino se propaga la excepción
    cart.items.append(item)
    cart.total_amount += item.price
    cart.save()
    return cart


def update_cart(cart_id, **params):
    try:
        Cart.objects.get(id=cart_id).update(**params)
        return get_cart(cart_id)
    except Cart.DoesNotExist:
        raise exceptions.CartNotFoundException()


def delete_cart(cart_id):
    get_cart(cart_id) # Valido si existe el carrito sino se propaga la excepción
    Cart.objects.with_id(cart_id).delete()

