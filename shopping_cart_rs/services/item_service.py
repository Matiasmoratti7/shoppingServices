import requests
from exceptions import exceptions
from services import user_service, email_service
from config import config


def get_items():
    try:
        response = requests.get(config.endpoints.items)
    except Exception:
        raise exceptions.StorageServerError
    if response.status_code == 404:
        raise exceptions.ItemNotFoundException
    elif response.status_code == 200:
        return response.json()['items']
    else:
        raise exceptions.StorageServerError


def get_item(item_id):
    try:
        response = requests.get(config.endpoints.item + item_id)
    except Exception:
        raise exceptions.StorageServerError
    if response.status_code == 404:
        raise exceptions.ItemNotFoundException
    elif response.status_code == 200:
        return response.json()
    else:
        raise exceptions.StorageServerError


def delete_item(item_id, token):
    if user_service.valid_admin(token):
        try:
            response = requests.delete(config.endpoints.item + item_id)
        except Exception:
            raise exceptions.StorageServerError
        if response.status_code == 404:
            raise exceptions.ItemNotFoundException
        elif response.status_code != 200:
            raise exceptions.StorageServerError
    else:
        raise exceptions.NotAnAdmin()


def update_item(item_id, token, **params):
    if user_service.valid_admin(token):
        previous_item = get_item(item_id)
        try:
            response = requests.put(config.endpoints.item + item_id, json=params)
        except Exception:
            raise exceptions.StorageServerError
        if response.status_code == 404:
            raise exceptions.ItemNotFoundException()
        elif response.status_code == 400:
            raise exceptions.BadRequest(response.text)
        elif response.status_code == 200:
            item_updated = response.json()
            if item_updated['price'] != previous_item['price']:
                email_service.send_email("New Price!", "The new price for " + item_updated['name'] + " is " +
                                                str(item_updated['price']))
            return item_updated
        else:
            raise exceptions.StorageServerError()
    else:
        raise exceptions.NotAnAdmin()


def create_item(**params):
    try:
        response = requests.post(config.endpoints.items, json=params)
    except Exception:
        raise exceptions.StorageServerError
    if response.status_code == 400:
        raise exceptions.ItemAlreadyExists
    elif response.status_code == 201:
        email_service.send_email("New Item created", "A new Item has been created")
        return response.json()['item_id']
    raise exceptions.StorageServerError()


