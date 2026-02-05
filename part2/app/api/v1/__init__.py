"""
API v1 Blueprint and Namespace registration
Configuration du Blueprint et enregistrement des Namespaces de l'API v1
Ce fichier organise toutes les routes de l'API REST
"""

# Importe Blueprint de Flask pour creer un groupe de routes
from flask import Blueprint

# Importe Api de flask_restx pour la documentation Swagger automatique
from flask_restx import Api

# Cree le Blueprint qui sera enregistre dans l'application Flask
# 'api' = nom du blueprint (pour reference interne)
# __name__ = module actuel (pour trouver les ressources)
# url_prefix = toutes les routes de ce blueprint commenceront par /api/v1
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Cree l'instance Api de flask_restx qui ajoute:
# - Documentation Swagger automatique
# - Serialisation JSON automatique
# - Gestion des erreurs HTTP
api = Api(
    api_bp,                                    # Attache l'API au blueprint
    title='HBnB API',                          # Titre affiche dans Swagger
    version='1.0',                             # Version de l'API
    description='HBnB Application REST API - Part 2',  # Description
    doc='/doc'                                 # URL de la documentation Swagger
)

# Importe les namespaces depuis les modules de l'API
# Chaque namespace gere un type de ressource (users, places, etc.)
from app.api.v1.users import api as users_ns        # Namespace pour les utilisateurs
from app.api.v1.places import api as places_ns      # Namespace pour les lieux
from app.api.v1.reviews import api as reviews_ns    # Namespace pour les avis
from app.api.v1.amenities import api as amenities_ns  # Namespace pour les equipements

# Enregistre chaque namespace avec son chemin URL
# Les routes seront: /api/v1/users, /api/v1/places, etc.
api.add_namespace(users_ns, path='/users')        # Routes utilisateurs
api.add_namespace(places_ns, path='/places')      # Routes lieux
api.add_namespace(reviews_ns, path='/reviews')    # Routes avis
api.add_namespace(amenities_ns, path='/amenities')  # Routes equipements
