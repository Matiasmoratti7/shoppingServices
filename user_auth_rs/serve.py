from config import config
from app import app
from rest import user_rest
from exceptions.exceptions import CustomError
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from repositories import db

STAGE = '/ini/config.ini'


def run(config_file=STAGE):
    config.set_configs(config_file)

    flask_app()


def flask_app():
    app.config['JSON_SORT_KEYS'] = False
    app.config.from_mapping(SECRET_KEY='dev',
                            JWT_SECRET_KEY=config.configs.jwt_secret_key,
                            MONGODB_SETTINGS={'host': config.configs.db_url,
                                              }
                            )

    """Run config based on config_file
     ...
    """

    # Initialize the DB
    db.initialize_db(app)

    # Load blueprints
    app.register_blueprint(user_rest.bp)

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

    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    
    app.run(host='0.0.0.0', port=config.configs.port)


if __name__ == "__main__":
    run(config_file=STAGE)
