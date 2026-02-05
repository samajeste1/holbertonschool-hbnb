"""
HBnB Facade Pattern Implementation
Implementation du pattern Facade pour HBnB
La Facade fournit une interface simplifiee vers la logique metier complexe
Elle cache la complexite des repositories et de la validation aux couches superieures
"""

# Importe les modeles metier
from app.models.user import User          # Modele utilisateur
from app.models.place import Place        # Modele lieu/logement
from app.models.review import Review      # Modele avis
from app.models.amenity import Amenity    # Modele equipement

# Importe le repository en memoire pour stocker les donnees
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """
    Main facade to manage business logic for users, places, reviews, and amenities.
    Facade principale qui gere la logique metier pour tous les modeles
    Point d'entree unique pour toutes les operations CRUD
    Utilise le pattern Facade pour simplifier l'interface
    """

    def __init__(self):
        """
        Initialize facade with in-memory repositories
        Initialise la facade avec un repository pour chaque type d'entite
        Chaque repository est independant et stocke ses propres objets
        """
        # Repository pour stocker les utilisateurs
        self.user_repo = InMemoryRepository()

        # Repository pour stocker les lieux
        self.place_repo = InMemoryRepository()

        # Repository pour stocker les avis
        self.review_repo = InMemoryRepository()

        # Repository pour stocker les equipements
        self.amenity_repo = InMemoryRepository()

    # ===== USER METHODS =====
    # Methodes pour gerer les utilisateurs

    def create_user(self, user_data):
        """
        Create a new user and add it to the repository.
        Cree un nouvel utilisateur et l'ajoute au repository

        Args:
            user_data (dict): Dictionnaire avec les infos utilisateur
                             {'first_name': 'John', 'last_name': 'Doe', 'email': 'john@test.com'}

        Returns:
            User: L'instance User creee
        """
        # Cree un objet User en deballant le dictionnaire avec **
        # **user_data transforme {'first_name': 'John'} en first_name='John'
        user = User(**user_data)

        # Ajoute l'utilisateur au repository
        self.user_repo.add(user)

        # Retourne l'utilisateur cree
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by ID.
        Recupere un utilisateur par son identifiant

        Args:
            user_id (str): L'identifiant unique de l'utilisateur

        Returns:
            User: L'instance User ou None si non trouve
        """
        # Delegue la recherche au repository
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a user by email.
        Recherche un utilisateur par son email (utile pour la connexion)

        Args:
            email (str): L'adresse email a rechercher

        Returns:
            User: L'instance User ou None si non trouve
        """
        # Utilise get_by_attribute pour chercher par email
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Return all users.
        Retourne la liste de tous les utilisateurs

        Returns:
            list: Liste de toutes les instances User
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        """
        Update an existing user with new data.
        Met a jour un utilisateur existant

        Args:
            user_id (str): L'identifiant de l'utilisateur a modifier
            update_data (dict): Les nouvelles valeurs a appliquer

        Returns:
            User: L'utilisateur mis a jour ou None si non trouve
        """
        # Recupere l'utilisateur existant
        user = self.get_user(user_id)

        # Si l'utilisateur n'existe pas, retourne None
        if not user:
            return None

        # Parcourt les donnees a mettre a jour
        for key, value in update_data.items():
            # Verifie que l'attribut existe et n'est pas protege
            # id et created_at ne doivent jamais etre modifies
            if hasattr(user, key) and key not in ['id', 'created_at']:
                # Met a jour l'attribut
                setattr(user, key, value)

        # Met a jour le timestamp updated_at
        user.save()

        return user

    # ===== PLACE METHODS =====
    # Methodes pour gerer les lieux

    def create_place(self, place_data):
        """
        Create a new place.
        Cree un nouveau lieu

        Args:
            place_data (dict): Dictionnaire avec les infos du lieu

        Returns:
            Place: L'instance Place creee

        Raises:
            ValueError: Si owner_id est invalide
        """
        # Recupere l'ID du proprietaire depuis les donnees
        owner_id = place_data.get('owner_id')

        # Cherche le proprietaire dans le repository des users
        owner = self.user_repo.get(owner_id)

        # Si le proprietaire n'existe pas, leve une erreur
        if not owner:
            raise ValueError("Invalid owner_id")

        # Prepare la liste des amenities
        amenities = []

        # Si des amenities sont fournis dans les donnees
        if 'amenities' in place_data:
            # Parcourt les IDs d'amenities fournis
            for amenity_id in place_data['amenities']:
                # Recupere chaque amenity par son ID
                amenity = self.amenity_repo.get(amenity_id)
                # Ajoute seulement si l'amenity existe
                if amenity:
                    amenities.append(amenity)

        # Cree le lieu avec les parametres nommes
        place = Place(
            title=place_data['title'],                    # Titre obligatoire
            description=place_data.get('description', ''), # Description optionnelle
            price=place_data['price'],                    # Prix obligatoire
            latitude=place_data['latitude'],              # Latitude obligatoire
            longitude=place_data['longitude'],            # Longitude obligatoire
            owner=owner,                                  # Objet User proprietaire
            amenities=amenities,                          # Liste d'objets Amenity
            reviews=[]                                    # Liste vide de reviews
        )

        # Ajoute le lieu au repository
        self.place_repo.add(place)

        return place

    def get_place(self, place_id):
        """
        Retrieve a place by ID.
        Recupere un lieu par son identifiant

        Args:
            place_id (str): L'identifiant unique du lieu

        Returns:
            Place: L'instance Place ou None
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Return all places.
        Retourne tous les lieux

        Returns:
            list: Liste de toutes les instances Place
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, update_data):
        """
        Update an existing place with new data.
        Met a jour un lieu existant

        Args:
            place_id (str): L'identifiant du lieu
            update_data (dict): Les nouvelles valeurs

        Returns:
            Place: Le lieu mis a jour

        Raises:
            ValueError: Si le lieu n'existe pas
        """
        # Recupere le lieu existant
        place = self.place_repo.get(place_id)

        # Si le lieu n'existe pas, leve une erreur
        if not place:
            raise ValueError("Place not found")

        # Liste des champs modifiables (securite)
        allowed_fields = ['title', 'description', 'price', 'latitude', 'longitude']

        # Met a jour seulement les champs autorises
        for key, value in update_data.items():
            if key in allowed_fields:
                setattr(place, key, value)

        # Met a jour le timestamp
        place.save()

        return place

    # ===== AMENITY METHODS =====
    # Methodes pour gerer les equipements

    def create_amenity(self, amenity_data):
        """
        Create a new amenity if valid.
        Cree un nouvel equipement

        Args:
            amenity_data (dict): Dictionnaire avec le nom de l'equipement

        Returns:
            Amenity: L'instance Amenity creee
        """
        # Cree l'amenity avec le nom fourni
        amenity = Amenity(name=amenity_data['name'])

        # Ajoute au repository
        self.amenity_repo.add(amenity)

        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID.
        Recupere un equipement par son identifiant

        Args:
            amenity_id (str): L'identifiant de l'equipement

        Returns:
            Amenity: L'instance Amenity ou None
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Return all amenities.
        Retourne tous les equipements

        Returns:
            list: Liste de toutes les instances Amenity
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity with new data.
        Met a jour un equipement existant

        Args:
            amenity_id (str): L'identifiant de l'equipement
            amenity_data (dict): Les nouvelles valeurs

        Returns:
            Amenity: L'equipement mis a jour ou None

        Raises:
            ValueError: Si le nom est invalide
        """
        # Recupere l'equipement existant
        amenity = self.get_amenity(amenity_id)

        # Si l'equipement n'existe pas, retourne None
        if not amenity:
            return None

        # Si un nouveau nom est fourni
        if 'name' in amenity_data:
            # Met a jour le nom
            amenity.name = amenity_data['name']
            # Re-valide apres modification (peut lever ValueError)
            amenity.validate()
            # Met a jour le timestamp
            amenity.save()

        return amenity

    # ===== REVIEW METHODS =====
    # Methodes pour gerer les avis

    def create_review(self, review_data):
        """
        Create a new review.
        Cree un nouvel avis

        Args:
            review_data (dict): Dictionnaire avec les donnees de l'avis

        Returns:
            Review: L'instance Review creee

        Raises:
            ValueError: Si place_id ou user_id est invalide
        """
        # Verifie que le lieu existe
        place = self.place_repo.get(review_data['place_id'])
        # Verifie que l'utilisateur existe
        user = self.user_repo.get(review_data['user_id'])

        # Si le lieu n'existe pas
        if not place:
            raise ValueError("Invalid place_id")
        # Si l'utilisateur n'existe pas
        if not user:
            raise ValueError("Invalid user_id")

        # Cree l'avis avec les donnees fournies
        review = Review(
            text=review_data['text'],           # Texte du commentaire
            rating=review_data['rating'],       # Note (1-5)
            place_id=review_data['place_id'],   # ID du lieu
            user_id=review_data['user_id']      # ID de l'auteur
        )

        # Ajoute l'avis au repository
        self.review_repo.add(review)

        # Ajoute aussi l'avis a la liste des reviews du lieu
        place.add_review(review)

        return review

    def get_review(self, review_id):
        """
        Retrieve a review by ID.
        Recupere un avis par son identifiant

        Args:
            review_id (str): L'identifiant de l'avis

        Returns:
            Review: L'instance Review ou None
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Return all reviews.
        Retourne tous les avis

        Returns:
            list: Liste de toutes les instances Review
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Return all reviews for a specific place.
        Retourne tous les avis pour un lieu donne

        Args:
            place_id (str): L'identifiant du lieu

        Returns:
            list: Liste des avis pour ce lieu
        """
        # List comprehension: filtre les reviews par place_id
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def get_reviews_by_user(self, user_id):
        """
        Return all reviews by a specific user.
        Retourne tous les avis ecrits par un utilisateur

        Args:
            user_id (str): L'identifiant de l'utilisateur

        Returns:
            list: Liste des avis de cet utilisateur
        """
        # Filtre les reviews par user_id
        return [review for review in self.review_repo.get_all() if review.user_id == user_id]

    def update_review(self, review_id, update_data):
        """
        Update an existing review.
        Met a jour un avis existant

        Args:
            review_id (str): L'identifiant de l'avis
            update_data (dict): Les nouvelles valeurs

        Returns:
            Review: L'avis mis a jour ou None
        """
        # Recupere l'avis existant
        review = self.get_review(review_id)

        # Si l'avis n'existe pas
        if not review:
            return None

        # Champs modifiables (on ne peut pas changer place_id ou user_id)
        allowed_fields = ['text', 'rating']

        # Met a jour seulement les champs autorises
        for key, value in update_data.items():
            if key in allowed_fields:
                setattr(review, key, value)

        # Re-valide apres modification
        review.validate()
        # Met a jour le timestamp
        review.save()

        return review

    def delete_review(self, review_id):
        """
        Delete a review by ID.
        Supprime un avis

        Args:
            review_id (str): L'identifiant de l'avis

        Returns:
            bool: True si supprime, False si non trouve
        """
        # Verifie d'abord que l'avis existe
        review = self.review_repo.get(review_id)

        if review:
            # Supprime du repository
            self.review_repo.delete(review_id)
            return True

        return False
