#!/usr/bin/python3
# Ligne shebang : indique que ce script utilise Python 3

"""
Application Factory for HBnB Part 2
Usine a application (Factory Pattern) pour creer l'application Flask
Ce pattern permet de creer plusieurs instances avec differentes configurations
"""

# Importe la classe Flask qui est le coeur du framework web
from flask import Flask

# Importe Api de flask_restx pour creer une API REST avec documentation Swagger automatique
from flask_restx import Api

# Importe la classe Config qui contient les parametres de configuration
from app.config import Config


def create_app(config_class=Config):
    """
    Create and configure the Flask application
    Cree et configure l'application Flask

    Args:
        config_class: Configuration class to use (classe de configuration a utiliser)
                     Par defaut, utilise la classe Config de base

    Returns:
        Flask application instance (instance de l'application Flask configuree)
    """
    # Cree une nouvelle instance de l'application Flask
    # __name__ indique a Flask ou trouver les ressources (templates, static)
    app = Flask(__name__)

    # Charge la configuration depuis la classe config_class
    # Cela definit SECRET_KEY, DEBUG, etc.
    app.config.from_object(config_class)

    # Importe le blueprint de l'API v1 depuis le module api.v1
    # Un blueprint est un moyen d'organiser les routes en groupes
    from app.api.v1 import api_bp

    # Enregistre le blueprint dans l'application Flask
    # Toutes les routes du blueprint seront ajoutees a l'application
    app.register_blueprint(api_bp)

    # Retourne l'application Flask configuree et prete a l'emploi
    return app
