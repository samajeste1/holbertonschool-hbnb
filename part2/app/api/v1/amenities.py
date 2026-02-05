"""
Amenities API Endpoints - Points d'entree API pour les equipements
Gere les operations CRUD pour les amenities (WiFi, Parking, Piscine, etc.)
"""

# Importe les classes necessaires de flask_restx
from flask_restx import Namespace, Resource, fields

# Importe l'instance facade pour acceder a la logique metier
from app.services import facade

# Cree le namespace pour les routes d'equipements
# Ce namespace regroupera toutes les routes /api/v1/amenities/*
api = Namespace('amenities', description='Amenity operations')

# Modele pour la creation / mise a jour d'un amenity
# Definit la structure JSON attendue dans les requetes POST/PUT
amenity_model = api.model('Amenity', {
    # Seul le nom est requis pour un amenity
    'name': fields.String(required=True, description='Name of the amenity')
})


# Route pour la liste des amenities et la creation
# URL: /api/v1/amenities/
@api.route('/')
class AmenityList(Resource):
    """
    Resource pour lister et creer des equipements
    GET: retourne tous les equipements
    POST: cree un nouvel equipement
    """

    # Valide le corps de la requete selon amenity_model
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new amenity
        Cree un nouvel equipement
        Methode HTTP: POST /api/v1/amenities/
        """
        try:
            # Recupere les donnees JSON de la requete
            data = api.payload

            # Appelle la facade pour creer l'equipement
            amenity = facade.create_amenity(data)

            # Retourne l'equipement cree avec code 201 (Created)
            return amenity.to_dict(), 201
        except ValueError as e:
            # Si la validation echoue (nom vide ou trop long)
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities
        Recupere la liste de tous les equipements
        Methode HTTP: GET /api/v1/amenities/
        """
        # Recupere tous les equipements
        amenities = facade.get_all_amenities()

        # Convertit chaque amenity en dictionnaire
        # Retourne une liste JSON
        return [amenity.to_dict() for amenity in amenities], 200


# Route pour un equipement specifique par son ID
# <string:amenity_id> capture l'ID comme parametre de type string
@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    """
    Resource pour gerer un equipement specifique
    GET: recupere les details
    PUT: met a jour l'equipement
    """

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Retrieve a specific amenity by ID
        Recupere un equipement specifique par son identifiant
        Methode HTTP: GET /api/v1/amenities/<amenity_id>
        """
        # Cherche l'equipement par son ID
        amenity = facade.get_amenity(amenity_id)

        # Si l'equipement n'existe pas
        if amenity is None:
            return {'error': 'Amenity not found'}, 404

        # Retourne les details de l'equipement
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an amenity
        Met a jour un equipement existant
        Methode HTTP: PUT /api/v1/amenities/<amenity_id>
        """
        try:
            # Recupere les nouvelles donnees
            data = api.payload

            # Appelle la facade pour mettre a jour
            amenity = facade.update_amenity(amenity_id, data)

            # Si l'equipement n'existe pas
            if amenity is None:
                return {'error': 'Amenity not found'}, 404

            # Retourne l'equipement mis a jour
            return amenity.to_dict(), 200
        except ValueError as e:
            # Si la validation du nouveau nom echoue
            return {'error': str(e)}, 400
