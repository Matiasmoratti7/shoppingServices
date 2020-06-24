import requests
from exceptions import exceptions
from services import email_service, user_service
from abc import ABC, abstractmethod
from config import config


def create_cart():
    try:
        response = requests.post(config.endpoints.carts)
    except Exception:
        raise exceptions.StorageServerError()
    if response.status_code == 201:
        return response.json()['cart_id']
    else:
        raise exceptions.StorageServerError()


def get_cart(cart_id):
    try:
        response = requests.get(config.endpoints.cart + cart_id)
    except Exception:
        raise exceptions.StorageServerError()
    if response.status_code == 404:
        raise exceptions.CartNotFoundException
    elif response.status_code == 200:
        return response.json()
    else:
        raise exceptions.StorageServerError()


def checkout_cart(payment_data, cart_id, token):
    user = user_service.user_logged(token)
    if user:
        cart = Cart(payment_data, cart_id)
        return cart.checkout()
    else:
        raise exceptions.NotLoggedIn()


def add_item_to_cart(cart_id, item_id):
    try:
        response = requests.post(config.endpoints.cart + cart_id + '/items/' + item_id)
    except Exception:
        raise exceptions.StorageServerError()
    if response.status_code == 404:
        raise exceptions.CartOrItemNotFoundException(response.json['message'])
    elif response.status_code == 200:
        return response.json()
    else:
        raise exceptions.StorageServerError()


def cancel_cart(cart_id):
    try:
        response = requests.delete(config.endpoints.cart + cart_id)
    except Exception:
        raise exceptions.StorageServerError()
    if response.status_code == 404:
        raise exceptions.CartNotFoundException
    elif response.status_code == 200:
        return response.json()
    else:
        raise exceptions.StorageServerError()


class Cart(object):

    def __init__(self, payment_data, cart_id):
        self._cart_id = cart_id
        self._cart_db = get_cart(cart_id)
        self._payment_method = payment_data['payment_method']
        if self._payment_method == 'CC':
            self._discount_strategy = CreditCardStrategy(payment_data['name'], payment_data['cc_number'],
                                                         self._cart_db['total_amount'])
        elif self._payment_method == 'P':
            self._discount_strategy = PaypalStrategy(payment_data['emaii'], payment_data['password'],
                                                     self._cart_db['total_amount'], self._cart_db['items'])
        elif self._payment_method == 'C':
            self._discount_strategy = CashStrategy(self._cart_db['total_amount'], self._cart_db['items'])

    def apply_discount(self):
        return self._discount_strategy.apply_discount()

    def checkout(self):
        to_charge = self.apply_discount()
        try:
            response = requests.put(config.endpoints.cart + self._cart_id, json={'status': 'Checked out',
                                                                                      'payment_method': self._payment_method,
                                                                                      'total_amount': to_charge,
                                                                                      'username': self._cart_db['username']})
        except Exception:
            raise exceptions.StorageServerError()
        # Esto también podría ejecutarse en un thread separado ya que ya se le cobró al cliente...
        if response.status_code == 200:
            email_service.send_email("You sold!", "A new " + self._payment_method + " transaction was made.")
            return response.json()
        else:
            # Haría rollback del cobro con la pasarela
            raise exceptions.StorageServerError()


class PaymentStrategy(ABC):

    @abstractmethod
    def apply_discount(self, **kargs):
        pass


class CreditCardStrategy(PaymentStrategy):
    def apply_discount(self, **kwargs):
        to_charge = kwargs['total_amount'] - ((10 * kwargs['total_amount']) / 100)  # Apply discount
        if FakePaymentGateway.credit_card_payment(kwargs['name'], kwargs['cc_number'], to_charge):
            return to_charge
        else:
            raise exceptions.PaymentError()


class PaypalStrategy(PaymentStrategy):
    def apply_discount(self, **kwargs):
        cheapest = None
        for item in kwargs['items']:
            if not cheapest or cheapest["price"] > item["price"]:
                cheapest = item
        to_charge = kwargs['total_amount'] - cheapest["price"]
        if FakePaymentGateway.paypal_payment(kwargs['email'], kwargs['password'], to_charge):
            return to_charge
        else:
            raise exceptions.PaymentError()


class CashStrategy(PaymentStrategy):
    def apply_discount(self, **kwargs):
        expensive = None
        for item in kwargs['items']:
            if not expensive or expensive["price"] < item["price"]:
                expensive = item
        to_charge = kwargs['total_amount'] - ((90 * expensive["price"]) / 100)  # Apply discount
        return to_charge


class FakePaymentGateway(object):

    @staticmethod
    def credit_card_payment(name, ccnumber, to_charge):
        """Magic..."""
        return True

    @staticmethod
    def paypal_payment(email, password, to_charge):
        """Magic..."""
        return True
