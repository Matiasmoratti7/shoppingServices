from flask import Blueprint, request
from services import email_service
from check_params.check_params import check_parameters

bp = Blueprint('email', __name__)


@bp.route('/email/send', methods=('POST',))
def send_email():
    body = request.get_json()

    possible_params = ['subject', 'body']
    check_parameters(params=body, required=possible_params, possible=possible_params)

    try:
        email_service.send_email(body['subject'], body['body'])
    except Exception:
        return "", 500
    return "", 200