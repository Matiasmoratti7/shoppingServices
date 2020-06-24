from exceptions import exceptions
from model.item import Item
from mongoengine import NotUniqueError


def get_items():
    items = Item.objects()

    if not items:
        raise exceptions.ItemNotFoundException()
    else:
        return items


def get_item(item_id):
    item = Item.objects.with_id(item_id)
    if item is None:
        raise exceptions.ItemNotFoundException()
    else:
        return item


def delete_item(item_id):
    try:
        Item.objects.get(id=item_id).delete()
    except Item.DoesNotExist:
        raise exceptions.ItemNotFoundException()


def update_item(item_id, **params):
    try:
        Item.objects.get(id=item_id).update(**params)
        return get_item(item_id)
    except NotUniqueError:
        raise exceptions.ItemAlreadyExists()
    except Item.DoesNotExist:
        raise exceptions.ItemNotFoundException()


def create_item(**params):
    try:
        item = Item(**params).save()
    except NotUniqueError:
        raise exceptions.ItemAlreadyExists()
    return item.id

