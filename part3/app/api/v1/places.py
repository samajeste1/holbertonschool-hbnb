"""
Places API Endpoints - Points d'entree API pour les lieux/logements
Gere les operations CRUD sur les lieux

Endpoints:
    GET  /places/          - Liste tous les lieux
    POST /places/          - Cree un nouveau lieu (auth requise)
    GET  /places/<id>      - Details d'un lieu
    PUT  /places/<id>      - Modifie un lieu (proprietaire ou admin)
"""

# Flask-RESTx pour creer l'API REST avec documentation Swagger
from flask_restx import Namespace, Resource, fields

# Importe la facade pour acceder aux operations metier
from app.services import facade

# JWT pour l'authentification et l'autorisation
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

# Cree le namespace pour les lieux
# Toutes les routes seront prefixees par /api/v1/places/
api = Namespace('places', description='Place operations')

# ============================================
# MODELES DE DONNEES POUR LA VALIDATION
# ============================================
# Ces modeles definissent la structure des donnees attendues/retournees
# Utilises par Swagger pour la documentation et la validation

# Modele pour les equipements inclus dans un lieu
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String,      # UUID de l'equipement
    'name': fields.String     # Nom de l'equipement (ex: "WiFi")
})

# Modele pour le proprietaire d'un lieu
user_model = api.model('PlaceUser', {
    'id': fields.String,          # UUID du proprietaire
    'first_name': fields.String,  # Prenom
    'last_name': fields.String,   # Nom
    'email': fields.String        # Email
})

# Modele principal pour creer/modifier un lieu
place_model = api.model('Place', {
    'title': fields.String(required=True),       # Titre du lieu (obligatoire)
    'description': fields.String,                 # Description (optionnel)
    'price': fields.Float(required=True),         # Prix par nuit (obligatoire)
    'latitude': fields.Float(required=True),      # Coordonnee GPS latitude
    'longitude': fields.Float(required=True),     # Coordonnee GPS longitude
    'owner_id': fields.String(required=True),     # ID du proprietaire
    'amenities': fields.List(fields.String, required=False),  # Liste d'IDs d'equipements
})

# ============================================
# ENDPOINT: /places/
# ============================================
@api.route('/')
class PlaceList(Resource):
    """
    Resource pour la liste des lieux
    GET  : Recupere tous les lieux (public)
    POST : Cree un nouveau lieu (authentification requise)
    """

    @api.expect(place_model)           # Valide le corps de la requete
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @jwt_required()                     # Requiert un token JWT valide
    def post(self):
        """
        Create a new place
        Cree un nouveau lieu/logement

        Le proprietaire est automatiquement defini comme l'utilisateur connecte.
        Validation: titre, prix positif, coordonnees GPS valides.
        """
        # Recupere l'ID de l'utilisateur depuis le token JWT
        current_user_id = get_jwt_identity()
        data = api.payload
        
        # Vérifier que l'utilisateur est bien propriétaire du lieu
        if data.get('owner_id') and data['owner_id'] != current_user_id:
            return {'error': 'Cannot create place for another user'}, 403
            
        # Forcer l'owner_id à être l'ID de l'utilisateur actuel
        data['owner_id'] = current_user_id

        try:
            # Valider les données avant la création
            if not data.get('title') or not isinstance(data['title'], str):
                return {'error': 'Title is required and must be a string'}, 400
            if not isinstance(data.get('price'), (int, float)) or data['price'] <= 0:
                return {'error': 'Price must be a positive number'}, 400
            if not isinstance(data.get('latitude'), (int, float)) or not isinstance(data.get('longitude'), (int, float)):
                return {'error': 'Latitude and longitude must be numbers'}, 400

            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except PermissionError:
            return {'error': 'Unauthorized'}, 401

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Get all places
        Recupere la liste de tous les lieux disponibles

        Endpoint public - pas d'authentification requise.
        Retourne un tableau JSON de tous les lieux.
        """
        # Recupere tous les lieux via la facade
        places = facade.get_all_places()

        # Convertit chaque lieu en dictionnaire pour la reponse JSON
        return [place.to_dict() for place in places], 200


# ============================================
# ENDPOINT: /places/<place_id>
# ============================================
@api.route('/<place_id>')
class PlaceResource(Resource):
    """
    Resource pour un lieu specifique
    GET : Recupere les details d'un lieu (public)
    PUT : Modifie un lieu (proprietaire ou admin seulement)
    """

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details
        Recupere les details complets d'un lieu

        Inclut: proprietaire, equipements, avis
        Endpoint public - pas d'authentification requise.
        """
        try:
            # Recupere le lieu avec ses relations
            place = facade.get_place(place_id)

            # include_relationships=True : inclut owner, amenities, reviews
            return place.to_dict(include_relationships=True), 200
        except ValueError:
            return {'error': 'Place not found'}, 404

    @api.expect(place_model)
    @api.response(200, 'Lieu mis à jour')
    @api.response(404, 'Lieu non trouvé')
    @api.response(400, 'Données invalides')
    @api.response(403, 'Action non autorisée')
    @jwt_required()    # Requiert authentification
    def put(self, place_id):
        """
        Update a place
        Modifie les informations d'un lieu

        Seuls le proprietaire ou un admin peuvent modifier.
        Valide les donnees avant la mise a jour.
        """
        # Recupere les claims du JWT (contient is_admin)
        claims = get_jwt()

        # Recupere l'ID de l'utilisateur connecte
        current_user_id = get_jwt_identity()

        # Donnees de mise a jour depuis le corps de la requete
        data = api.payload

        try:
            # Récupérer le lieu
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Lieu non trouvé'}, 404

            # Les administrateurs peuvent modifier tous les lieux
            if not claims.get('is_admin') and place.owner_id != current_user_id:
                return {'error': 'Action non autorisée'}, 403

            # Valider les données
            if data.get('title') and not isinstance(data['title'], str):
                return {'error': 'Le titre doit être une chaîne de caractères'}, 400
            if data.get('price') and (not isinstance(data['price'], (int, float)) or data['price'] <= 0):
                return {'error': 'Le prix doit être un nombre positif'}, 400
            if (data.get('latitude') and not isinstance(data['latitude'], (int, float))) or \
               (data.get('longitude') and not isinstance(data['longitude'], (int, float))):
                return {'error': 'La latitude et la longitude doivent être des nombres'}, 400

            # Mettre à jour le lieu
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'error': 'Échec de la mise à jour du lieu'}, 500

            return updated_place.to_dict(), 200

        except Exception as e:
            return {'error': 'Erreur interne du serveur'}, 500
