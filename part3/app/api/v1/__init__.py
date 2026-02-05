"""
API v1 Blueprint and Namespace registration
"""
from flask import Blueprint
from flask_restx import Api

# Create the Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Create the API with Swagger documentation
api = Api(
    api_bp,
    title='HBnB API',
    version='1.0',
    description='HBnB Application REST API - Part 3 with Authentication',
    doc='/doc',
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using Bearer scheme. Example: "Bearer {token}"'
        }
    },
    security='Bearer'
)

# Import and register namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.auth import auth_ns

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(amenities_ns, path='/amenities')
