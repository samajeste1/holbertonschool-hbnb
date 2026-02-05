"""
Authentication API Endpoints - Points d'entree API pour l'authentification
Gere la connexion et la generation de tokens JWT
Inclut un endpoint pour obtenir un token admin (developpement)
"""

# Importe les classes de flask_restx pour creer l'API
from flask_restx import Namespace, Resource, fields

# Importe create_access_token pour generer des tokens JWT
from flask_jwt_extended import create_access_token

# Importe la facade pour acceder aux donnees utilisateur
from app.services.facade import hbnb_facade as facade

# Importe les decorateurs JWT pour proteger les routes
from flask_jwt_extended import jwt_required, get_jwt_identity

# Importe le modele User (pour la documentation)
from app.models.user import User

# Importe datetime et timedelta pour gerer l'expiration des tokens
from datetime import datetime, timedelta

# Configuration de l'utilisateur administrateur par defaut
# Utilise pour le developpement et les tests
DEFAULT_ADMIN = {
    'id': '00000000-0000-0000-0000-000000000000',    # ID fixe pour l'admin
    'email': 'admin@hbnb.com',                        # Email de connexion
    'password': 'hbnb_admin_123!',                    # Mot de passe (changer en prod!)
    'first_name': 'Admin',                            # Prenom
    'last_name': 'System',                            # Nom
    'is_admin': True                                  # Flag administrateur
}


def get_or_create_default_admin():
    """
    Cree ou recupere l'utilisateur administrateur par defaut
    Cette fonction s'assure qu'un admin existe toujours dans le systeme

    Returns:
        User: L'instance de l'utilisateur admin
    """
    try:
        # Essaie de recuperer l'admin existant par son email
        admin = facade.get_user_by_email(DEFAULT_ADMIN['email'])

        # Si l'admin n'existe pas, le creer
        if not admin:
            print("[AUTH] Creating default admin user...")

            # Prepare les donnees pour la creation
            admin_data = {
                'email': DEFAULT_ADMIN['email'],
                'first_name': DEFAULT_ADMIN['first_name'],
                'last_name': DEFAULT_ADMIN['last_name'],
                'password': DEFAULT_ADMIN['password'],
                'is_admin': True  # Important: definit les droits admin
            }

            # Cree l'utilisateur via la facade
            admin = facade.create_user(admin_data)
            print(f"[AUTH] Created admin user: {admin.id}, is_admin: {admin.is_admin}")
        else:
            # L'admin existe deja
            print(f"[AUTH] Admin user found: {admin.id}, is_admin: {admin.is_admin}")

        return admin

    except Exception as e:
        # Log l'erreur avec le traceback complet
        print(f"[AUTH] Error in get_or_create_default_admin: {str(e)}")
        import traceback
        traceback.print_exc()
        raise  # Re-leve l'exception


# Cree le namespace pour l'authentification
# Toutes les routes seront sous /api/v1/auth/
auth_ns = Namespace('auth', description='Authentication operations')

# Modele pour la validation des donnees de connexion
# Definit les champs attendus dans le JSON de la requete POST /login
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),      # Email obligatoire
    'password': fields.String(required=True, description='User password')  # Mot de passe obligatoire
})


# Route de connexion
# URL: POST /api/v1/auth/login
@auth_ns.route('/login')
class Login(Resource):
    """Resource pour l'authentification des utilisateurs"""

    @auth_ns.expect(login_model)  # Valide le corps de la requete
    def post(self):
        """
        Authenticate user and return a JWT token
        Authentifie un utilisateur et retourne un token JWT

        Process:
        1. Recupere les credentials de la requete
        2. Verifie que l'utilisateur existe
        3. Verifie le mot de passe
        4. Genere et retourne un token JWT
        """
        # Etape 1: Recupere les credentials depuis le corps JSON de la requete
        credentials = auth_ns.payload

        # Etape 2: Recherche l'utilisateur par email
        user = facade.get_user_by_email(credentials['email'])

        # Etape 3: Verifie l'existence de l'utilisateur ET la validite du mot de passe
        # verify_password() utilise bcrypt pour comparer de maniere securisee
        if not user or not user.verify_password(credentials['password']):
            # Retourne une erreur generique pour ne pas reveler si l'email existe
            return {'error': 'Invalid credentials'}, 401

        # Etape 4: Cree un token JWT avec l'ID de l'utilisateur comme identite
        # Le token contiendra: {"sub": user_id, "exp": expiration_time, ...}
        access_token = create_access_token(identity=str(user.id))

        # Retourne le token au client
        return {'access_token': access_token}, 200


# Route pour obtenir un token admin (developpement uniquement)
# URL: GET /api/v1/auth/admin-token
@auth_ns.route('/admin-token')
class AdminToken(Resource):
    """Resource pour obtenir un token admin (developpement)"""

    @auth_ns.doc(description='Get an admin token for development purposes')
    # Documente la reponse attendue pour Swagger
    @auth_ns.response(200, 'Success', auth_ns.model('AdminTokenResponse', {
        'access_token': fields.String(description='JWT token'),
        'user': fields.Nested(auth_ns.model('AdminUser', {
            'id': fields.String(description='User ID'),
            'email': fields.String(description='User email'),
            'first_name': fields.String(description='User first name'),
            'last_name': fields.String(description='User last name'),
            'is_admin': fields.Boolean(description='Is admin')
        }))
    }))
    @auth_ns.response(500, 'Failed to generate admin token')
    def get(self):
        """
        Get an admin token for development purposes
        Retourne un token admin pour faciliter le developpement
        """
        try:
            # Recupere ou cree l'utilisateur admin
            admin = get_or_create_default_admin()

            # Genere un token JWT pour l'admin
            # expires_delta=timedelta(days=1): token valable 24 heures
            access_token = create_access_token(
                identity=str(admin.id),
                expires_delta=timedelta(days=1)
            )

            # Retourne le token et les infos de l'admin
            return {
                'access_token': access_token,
                'user': {
                    'id': admin.id,
                    'email': admin.email,
                    'first_name': admin.first_name,
                    'last_name': admin.last_name,
                    'is_admin': admin.is_admin
                }
            }, 200

        except Exception as e:
            # Log et retourne une erreur en cas de probleme
            print(f"[AUTH] Error generating admin token: {str(e)}")
            return {'error': 'Failed to generate admin token'}, 500


# Route protegee pour tester l'authentification
# URL: GET /api/v1/auth/protected
@auth_ns.route('/protected')
class Protected(Resource):
    """Resource protegee pour tester l'authentification JWT"""

    @auth_ns.doc(description='Protected endpoint that requires a valid JWT token')
    @jwt_required()  # Decorateur: requiert un token JWT valide
    def get(self):
        """
        Protected endpoint that requires a valid JWT token
        Endpoint protege pour verifier que l'authentification fonctionne
        """
        # Importe get_jwt pour acceder aux claims complets du token
        from flask_jwt_extended import get_jwt

        # Recupere l'ID de l'utilisateur depuis le token
        # get_jwt_identity() extrait le champ "sub" du token
        current_user_id = get_jwt_identity()

        # Recupere tous les claims du token (metadata)
        claims = get_jwt()

        # Recupere les infos de l'utilisateur depuis la base
        user = facade.get_user(current_user_id)

        # Retourne les informations de debug
        return {
            'message': f"Hello, user {current_user_id}",
            'claims': claims,  # Contient exp, iat, type, etc.
            'user_from_db': {
                'id': user.id if user else None,
                'is_admin': user.is_admin if user else None
            }
        }, 200
