"""
Users API Endpoints - Points d'entree API pour les utilisateurs
Gere les operations CRUD (Create, Read, Update, Delete) pour les users
"""

# Importe les classes necessaires de flask_restx
# Namespace: groupe de routes liees (comme un sous-blueprint)
# Resource: classe de base pour definir les endpoints REST
# fields: pour definir les modeles de donnees (schema)
from flask_restx import Namespace, Resource, fields

# Importe l'instance facade depuis le module services
# La facade gere toute la logique metier
from app.services import facade

# Cree un namespace pour les routes utilisateur
# 'users' = nom du namespace
# description = affichee dans Swagger
api = Namespace('users', description='User operations')

# Definit le modele de donnees pour la validation et la documentation Swagger
# Ce modele decrit la structure des donnees attendues pour creer/modifier un user
user_model = api.model('User', {
    # Champ prenom: obligatoire, type string
    'first_name': fields.String(required=True, description='First name of the user'),
    # Champ nom: obligatoire, type string
    'last_name': fields.String(required=True, description='Last name of the user'),
    # Champ email: obligatoire, type string
    'email': fields.String(required=True, description='Email of the user'),
    # Champ admin: optionnel, booleen, defaut False
    'is_admin': fields.Boolean(required=False, default=False, description='Admin privileges')
})


# Decorateur @api.route definit le chemin URL pour cette classe
# '/' = racine du namespace = /api/v1/users/
@api.route('/')
class UserList(Resource):
    """
    Resource pour lister tous les users et creer un nouveau user
    Gere les requetes GET (liste) et POST (creation) sur /api/v1/users/
    """

    # @api.expect: valide le corps de la requete selon le modele
    # validate=True: rejette les requetes avec des champs manquants
    @api.expect(user_model, validate=True)
    # @api.response: documente les codes de retour possibles
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user
        Cree un nouvel utilisateur
        Methode HTTP: POST /api/v1/users/
        """
        # api.payload contient le corps JSON de la requete (deja parse)
        user_data = api.payload

        # Verifie si l'email est deja utilise (unicite)
        existing_user = facade.get_user_by_email(user_data['email'])

        # Si un utilisateur avec cet email existe deja
        if existing_user:
            # Retourne une erreur 400 (Bad Request)
            return {'error': 'Email already registered'}, 400

        # Tente de creer l'utilisateur
        try:
            # Appelle la facade pour creer l'utilisateur
            new_user = facade.create_user(user_data)
            # Retourne les donnees du user et le code 201 (Created)
            return new_user.to_dict(), 201
        except ValueError as e:
            # Si la validation echoue, retourne l'erreur avec code 400
            return {'error': str(e)}, 400

    # Documente la reponse reussie
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Retrieve all users
        Recupere la liste de tous les utilisateurs
        Methode HTTP: GET /api/v1/users/
        """
        # Recupere tous les utilisateurs via la facade
        users = facade.get_all_users()

        # Convertit chaque user en dictionnaire et retourne la liste
        # List comprehension pour transformer la liste d'objets en liste de dicts
        return [user.to_dict() for user in users], 200


# Route avec parametre dynamique <user_id>
# Le parametre sera passe a la methode en argument
@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource pour gerer un utilisateur specifique par son ID
    Gere GET (lecture) et PUT (modification) sur /api/v1/users/<id>
    """

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID
        Recupere les details d'un utilisateur par son identifiant
        Methode HTTP: GET /api/v1/users/<user_id>
        """
        # Cherche l'utilisateur par son ID
        user = facade.get_user(user_id)

        # Si l'utilisateur n'existe pas
        if not user:
            # Retourne erreur 404 (Not Found)
            return {'error': 'User not found'}, 404

        # Retourne les donnees de l'utilisateur
        return user.to_dict(), 200

    # Attend le modele user_model dans le corps de la requete
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        Update user information
        Met a jour les informations d'un utilisateur
        Methode HTTP: PUT /api/v1/users/<user_id>
        """
        # Recupere les nouvelles donnees
        user_data = api.payload

        try:
            # Appelle la facade pour mettre a jour
            updated_user = facade.update_user(user_id, user_data)

            # Si l'utilisateur n'a pas ete trouve
            if not updated_user:
                return {'error': 'User not found'}, 404

            # Retourne les donnees mises a jour
            return updated_user.to_dict(), 200
        except ValueError as e:
            # Si la validation echoue
            return {'error': str(e)}, 400
