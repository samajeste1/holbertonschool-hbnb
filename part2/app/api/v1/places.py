"""
Places API Endpoints - Points d'entree API pour les lieux/logements
Gere les operations CRUD pour les places et leurs reviews associees
"""

# Importe les classes necessaires de flask_restx
from flask_restx import Namespace, Resource, fields

# Importe l'instance facade pour la logique metier
from app.services import facade

# Cree le namespace pour les routes de lieux
api = Namespace('places', description='Place operations')

# Modele pour l'affichage d'un amenity dans un lieu
# Version simplifiee avec seulement id et nom
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# Modele pour l'affichage du proprietaire d'un lieu
# Contient les infos de base du user
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Modele pour l'affichage d'un avis sur un lieu
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Modele principal pour la creation/modification d'un lieu
# Definit tous les champs attendus dans le JSON
place_model = api.model('Place', {
    # Titre obligatoire du lieu
    'title': fields.String(required=True, description='Title of the place'),
    # Description optionnelle
    'description': fields.String(description='Description of the place'),
    # Prix par nuit obligatoire
    'price': fields.Float(required=True, description='Price per night'),
    # Coordonnees GPS obligatoires
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    # ID du proprietaire obligatoire
    'owner_id': fields.String(required=True, description='ID of the owner'),
    # Liste des IDs d'amenities (peut etre vide)
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


# Route pour la liste et creation de lieux
# URL: /api/v1/places/
@api.route('/')
class PlaceList(Resource):
    """
    Resource pour lister tous les lieux et en creer de nouveaux
    GET: liste simplifiee de tous les lieux
    POST: cree un nouveau lieu
    """

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new place
        Cree un nouveau lieu
        Methode HTTP: POST /api/v1/places/
        """
        # Recupere les donnees JSON
        data = api.payload

        try:
            # Cree le lieu via la facade
            place = facade.create_place(data)

            # Retourne les infos de base (sans objets imbriques)
            # Pour une reponse POST plus legere
            return {
                'id': place.id,                  # ID genere
                'title': place.title,            # Titre
                'description': place.description, # Description
                'price': place.price,            # Prix
                'latitude': place.latitude,      # Coordonnees
                'longitude': place.longitude,
                'owner_id': place.owner.id       # Juste l'ID du proprietaire
            }, 201
        except ValueError as e:
            # Si owner_id invalide ou autre erreur de validation
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places
        Recupere la liste de tous les lieux (version simplifiee)
        Methode HTTP: GET /api/v1/places/
        """
        # Recupere tous les lieux
        places = facade.get_all_places()

        # Retourne une liste simplifiee pour la performance
        # (pas de details complets pour chaque lieu)
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places], 200


# Route pour un lieu specifique
# URL: /api/v1/places/<place_id>
@api.route('/<place_id>')
class PlaceResource(Resource):
    """
    Resource pour gerer un lieu specifique
    GET: details complets avec proprietaire et amenities
    PUT: mise a jour du lieu
    """

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details by ID
        Recupere les details complets d'un lieu
        Methode HTTP: GET /api/v1/places/<place_id>
        """
        # Cherche le lieu
        place = facade.get_place(place_id)

        # Si le lieu n'existe pas
        if not place:
            return {'error': 'Place not found'}, 404

        # Retourne les details complets avec objets imbriques
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            # Proprietaire avec ses details
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            # Liste des amenities avec leurs details
            # List comprehension pour transformer les objets
            'amenities': [
                {'id': amenity.id, 'name': amenity.name}
                for amenity in place.amenities
            ]
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """
        Update a place's information
        Met a jour les informations d'un lieu
        Methode HTTP: PUT /api/v1/places/<place_id>
        """
        # Recupere les nouvelles donnees
        data = api.payload

        try:
            # Met a jour via la facade
            place = facade.update_place(place_id, data)

            # Message de confirmation
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            # Analyse le message d'erreur pour determiner le code HTTP
            error_message = str(e)

            # Si "not found" dans le message, c'est une erreur 404
            if 'not found' in error_message.lower():
                return {'error': error_message}, 404

            # Sinon c'est une erreur de validation (400)
            return {'error': error_message}, 400


# Route pour les avis d'un lieu specifique
# URL: /api/v1/places/<place_id>/reviews
@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Resource pour recuperer tous les avis d'un lieu
    GET: liste des reviews pour un lieu donne
    """

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place
        Recupere tous les avis pour un lieu specifique
        Methode HTTP: GET /api/v1/places/<place_id>/reviews
        """
        # Verifie d'abord que le lieu existe
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        # Recupere les avis pour ce lieu
        reviews = facade.get_reviews_by_place(place_id)

        # Retourne la liste des avis (version simplifiee)
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        } for review in reviews], 200
