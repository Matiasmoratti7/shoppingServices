from config import config
from app import app
from rest import email_rest
from services import email_service
from exceptions.exceptions import CustomError

STAGE = '/ini/config.ini'


def run(config_file=STAGE):
    config.set_configs(config_file)

    flask_app()


def flask_app():
    app.config['JSON_SORT_KEYS'] = False

    """Run config based on config_file
     ...
    """

    # Load blueprints
    app.register_blueprint(email_rest.bp)

    # Handling errors
    @app.errorhandler(CustomError)
    def handle_custom_error(error):
        """Catch CustomError exception globally, serialize into JSON, and respond with specified status."""
        payload = dict()
        payload['status'] = error.status
        payload['message'] = error.message
        return payload, error.status

    @app.errorhandler(400)
    def handle_bad_request(error):
        raise CustomError(error.description, 400)

    email_service.set_server()

    app.run(host='0.0.0.0', port=config.configs.port)


if __name__ == "__main__":
    run(config_file=STAGE)
