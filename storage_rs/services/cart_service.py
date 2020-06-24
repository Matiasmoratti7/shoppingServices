from repositories import cart_repository


def create_cart():
    return cart_repository.create_cart()


def get_cart(cart_id):
    return cart_repository.get_cart(cart_id)


def add_item_to_cart(cart_id, item_id):
    return cart_repository.add_item_to_cart(cart_id, item_id)


def update_cart(cart_id, **params):
    return cart_repository.update_cart(cart_id, **params)


def cancel_cart(cart_id):
    cart_repository.delete_cart(cart_id)



