from repositories import item_repository


def get_items():
    return item_repository.get_items()


def get_item(item_id):
    return item_repository.get_item(item_id)


def delete_item(item_id):
    return item_repository.delete_item(item_id)


def update_item(item_id, **params):
    return item_repository.update_item(item_id, **params)


def create_item(**params):
    return item_repository.create_item(**params)

