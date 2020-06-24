from shopping_cart_RS.exceptions import exceptions


def check_parameters(params, required=[], possible=[]):
    for possible_param in params:
        if possible_param not in possible:
            raise exceptions.ParamsError("Invalid parameter: " + possible_param)
    for required_param in required:
        if required_param not in params:

            raise exceptions.ParamsError(required_param + " is required")