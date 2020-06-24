from ..item_dto import ItemDTO


def get_dto(item):
    return ItemDTO(str(item.id), item.name, item.description, item.price, item.supplier, item.category)


def get_item(item):
    return get_dto(item).__dict__


def get_items(items):
    items_dto = []
    for item in items:
        item_dto = get_item(item)
        items_dto.append(item_dto)
    return items_dto
