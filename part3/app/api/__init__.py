"""
API package initialization with JWT configuration
"""
from flask_jwt_extended import JWTManager


def configure_jwt(jwt_manager: JWTManager):
    """Configure JWT callbacks."""
    from app.services.facade import hbnb_facade as facade

    @jwt_manager.user_identity_loader
    def user_identity_lookup(user):
        if isinstance(user, str):
            return user
        if isinstance(user, dict):
            return user['id']
        return str(user.id)

    @jwt_manager.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return facade.get_user(identity)

    @jwt_manager.additional_claims_loader
    def add_claims_to_access_token(identity):
        try:
            if isinstance(identity, dict):
                return {'is_admin': identity.get('is_admin', False)}

            user = facade.get_user(identity)
            if user:
                return {'is_admin': user.is_admin}
            else:
                return {'is_admin': False}
        except Exception as e:
            print(f"[JWT] Error in add_claims: {e}")
            return {'is_admin': False}

    @jwt_manager.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired'}, 401

    @jwt_manager.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token'}, 401

    @jwt_manager.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Authorization token is missing'}, 401

