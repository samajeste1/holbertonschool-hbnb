"""
Reviews API Endpoints - Points d'entree API pour les avis
Gere les operations CRUD pour les reviews (avis des utilisateurs sur les lieux)
"""

# Importe les classes necessaires de flask_restx
from flask_restx import Namespace, Resource, fields

# Importe l'instance facade pour la logique metier
from app.services import facade

# Cree le namespace pour les routes d'avis
api = Namespace('reviews', description='Review operations')

# Modele pour la creation et modification d'un avis
# Definit la structure JSON attendue
review_model = api.model('Review', {
    # Texte du commentaire (obligatoire)
    'text': fields.String(required=True, description='Text of the review'),
    # Note de 1 a 5 (obligatoire)
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    # ID de l'utilisateur qui ecrit l'avis (obligatoire)
    'user_id': fields.String(required=True, description='ID of the user'),
    # ID du lieu concerne (obligatoire)
    'place_id': fields.String(required=True, description='ID of the place')
})


# Route pour la liste et creation d'avis
# URL: /api/v1/reviews/
@api.route('/')
class ReviewList(Resource):
    """
    Resource pour lister tous les avis et en creer de nouveaux
    GET: liste de tous les avis
    POST: cree un nouvel avis
    """

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new review
        Cree un nouvel avis
        Methode HTTP: POST /api/v1/reviews/
        """
        # Recupere les donnees JSON de la requete
        data = api.payload

        try:
            # Cree l'avis via la facade
            # La facade verifie que user_id et place_id existent
            review = facade.create_review(data)

            # Retourne l'avis cree avec tous ses details
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 201
        except ValueError as e:
            # Si user_id ou place_id invalide, ou erreur de validation
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews
        Recupere la liste de tous les avis
        Methode HTTP: GET /api/v1/reviews/
        """
        # Recupere tous les avis
        reviews = facade.get_all_reviews()

        # Retourne une liste simplifiee (sans les IDs pour plus de legerete)
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        } for review in reviews], 200


# Route pour un avis specifique
# URL: /api/v1/reviews/<review_id>
@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Resource pour gerer un avis specifique
    GET: details de l'avis
    PUT: modification de l'avis
    DELETE: suppression de l'avis
    """

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get review details by ID
        Recupere les details d'un avis specifique
        Methode HTTP: GET /api/v1/reviews/<review_id>
        """
        # Cherche l'avis
        review = facade.get_review(review_id)

        # Si l'avis n'existe pas
        if not review:
            return {'error': 'Review not found'}, 404

        # Retourne tous les details de l'avis
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """
        Update a review's information
        Met a jour un avis existant
        Methode HTTP: PUT /api/v1/reviews/<review_id>
        """
        # Recupere les nouvelles donnees
        data = api.payload

        try:
            # Met a jour via la facade
            # Note: seuls text et rating peuvent etre modifies
            review = facade.update_review(review_id, data)

            # Si l'avis n'existe pas
            if not review:
                return {'error': 'Review not found'}, 404

            # Message de confirmation
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            # Si la validation echoue (rating invalide, etc.)
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete a review
        Supprime un avis
        Methode HTTP: DELETE /api/v1/reviews/<review_id>
        """
        # Tente de supprimer l'avis via la facade
        success = facade.delete_review(review_id)

        # Si l'avis n'existait pas
        if not success:
            return {'error': 'Review not found'}, 404

        # Confirmation de la suppression
        return {'message': 'Review deleted successfully'}, 200
