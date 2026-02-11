"""
Main Flask application for Image Optimization.
"""
import logging
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from routes import main_bp
from cleanup import FileCleanup


def create_app(config_class=Config):
    """
    Application factory for Flask app.

    Args:
        config_class: Configuration class to use

    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize configuration
    config_class.init_app(app)

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[app.config['RATELIMIT_DEFAULT']],
        storage_uri=app.config['RATELIMIT_STORAGE_URL']
    )

    # Register blueprints
    app.register_blueprint(main_bp)

    # Initialize file cleanup
    cleanup_manager = FileCleanup(app)

    # Store cleanup manager in app for access in routes if needed
    app.cleanup_manager = cleanup_manager

    app.logger.info("Image Optimization Flask app initialized successfully")

    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
