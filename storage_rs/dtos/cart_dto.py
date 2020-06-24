class CartDTO(object):

    def __init__(self, id, username, status, items=[], payment_method="", total_amount=0):
        self.id = id
        self.username = username
        self.status = status
        self.items = items
        self.payment_method = payment_method
        self.total_amount = total_amount

