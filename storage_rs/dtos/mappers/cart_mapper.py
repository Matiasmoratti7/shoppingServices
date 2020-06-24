from ..cart_dto import CartDTO
from . import item_mapper


def get_cart(cart):
    items_dto = []
    for item in cart.items:
        items_dto.append(item_mapper.get_item(item))
    return CartDTO(str(cart.id), cart.username, cart.status, items_dto,
                   cart.payment_method if cart.payment_method is not None else "", cart.total_amount).__dict__




