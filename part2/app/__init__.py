#!/usr/bin/python3
"""
Application Factory for HBnB Part 2
"""
from flask import Flask
from flask_restx import Api
from app.config import Config


def create_app(config_class=Config):
    """
    Create and configure the Flask application

    Args:
        config_class: Configuration class to use

    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register the API blueprint
    from app.api.v1 import api_bp
    app.register_blueprint(api_bp)

    return app
