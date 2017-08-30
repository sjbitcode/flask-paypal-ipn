import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap

from .database import db
from . import settings
from .views import main

bootstrap = Bootstrap()


def create_app():

    # Create application.
    app = Flask(
        import_name=__name__,
        static_folder=settings.STATIC_DIR,
        template_folder=settings.TEMPLATE_DIR
    )

    # Load configuration.
    app.config.from_object(settings)

    # Register blueprints.
    app.register_blueprint(main)

    # Initialize Flask Bootstrap.
    bootstrap.init_app(app)

    # Initialize database & create tables.
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Configure logging.
    configure_logging(app)

    return app


def configure_logging(app):

    # Create a file handler and set its level to DEBUG.
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=512000,
        backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)

    # Create a log formatter and set it to the file handler.
    format_str = (
        '[%(asctime)s] {%(filename)s:%(lineno)d} '
        '%(levelname)s - %(message)s'
    )
    formatter = logging.Formatter(format_str, '%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger.
    app.logger.addHandler(file_handler)

    # Set the logger's level to DEBUG.
    app.logger.setLevel(logging.DEBUG)
