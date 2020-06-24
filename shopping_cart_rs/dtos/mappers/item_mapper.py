from ..item_dto import ItemDTO
from types import SimpleNamespace
from config import config


def get_dto(item):
    return ItemDTO(item['id'], item['name'], item['description'], item['price'], item['supplier'], item['category'])


def get_item(item):
    return get_dto(item).__dict__


def get_items(items):
    get_items_version = config.mappings.get_items_version
    if get_items_version == "2":
        return get_items_custom_mapping(items)
    else:
        return get_items_plain(items)


def get_items_plain(items):
    items_dto = []
    for item in items:
        item_dto = get_item(item)
        items_dto.append(item_dto)
    return {'items': items_dto}


def get_items_custom_mapping(items):
    items_dto = []
    categories = SimpleNamespace()
    suppliers = SimpleNamespace()
    for item in items:
        item_dto = get_item(item)
        items_dto.append(item_dto)
        if hasattr(categories, item['category']):
            setattr(categories, item['category'], getattr(categories, item['category']) + 1)
        else:
            setattr(categories, item['category'], 1)

        if hasattr(suppliers, item['supplier']):
            setattr(suppliers, item['supplier'], getattr(suppliers, item['supplier']) + 1)
        else:
            setattr(suppliers, item['supplier'], 1)

    return {"total": len(items_dto),
            "categories": categories.__dict__,
            "suppliers": suppliers.__dict__,
            "data": items_dto}
