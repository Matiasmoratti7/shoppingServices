from config import config
from app import app
from rest import item_rest, cart_rest
from exceptions.exceptions import CustomError
from repositories import db

STAGE = '/ini/config.ini'


def run(config_file=STAGE):
    config.set_configs(config_file)

    flask_app()


def flask_app():
    app.config['JSON_SORT_KEYS'] = False
    app.config.from_mapping(SECRET_KEY='dev',
                            MONGODB_SETTINGS={'host': config.configs.db_url}
                            )

    """Run config based on config_file
     ...
    """

    # Initialize de DB
    db.initialize_db(app)

    # Load blueprints
    app.register_blueprint(item_rest.bp)
    app.register_blueprint(cart_rest.bp)

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

    app.run(host='0.0.0.0', port=config.configs.port)


if __name__ == "__main__":
    run(config_file=STAGE)
