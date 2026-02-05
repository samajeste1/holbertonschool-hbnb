"""
Place Model - Modele representant un lieu/logement a louer
Herite de BaseModel pour avoir id et timestamps automatiques
"""

# Importe BaseModel avec le chemin complet depuis app.models
from app.models.base_model import BaseModel


class Place(BaseModel):
    """
    Place model representing a rental property in the HBnB application
    Modele representant une propriete a louer (appartement, maison, etc.)
    Contient les informations de localisation, prix et proprietaire
    """

    def __init__(self, title, description, price, latitude, longitude, owner, amenities=None, reviews=None):
        """
        Initialize a Place instance
        Cree un nouveau lieu avec toutes ses caracteristiques

        Args:
            title (str): Titre du lieu (max 100 caracteres, obligatoire)
            description (str): Description detaillee du lieu (optionnel)
            price (float): Prix par nuit en euros (doit etre positif)
            latitude (float): Coordonnee de latitude (-90.0 a 90.0)
            longitude (float): Coordonnee de longitude (-180.0 a 180.0)
            owner: Instance User du proprietaire (obligatoire)
            amenities (list): Liste des equipements/services disponibles (optionnel)
            reviews (list): Liste des avis sur ce lieu (optionnel)
        """
        # Appelle le constructeur parent pour initialiser id et timestamps
        super().__init__()

        # Stocke le titre affiche du lieu
        self.title = title

        # Stocke la description complete
        self.description = description

        # Stocke le prix par nuit (float pour gerer les centimes)
        self.price = price

        # Stocke la latitude (coordonnee Nord-Sud)
        self.latitude = latitude

        # Stocke la longitude (coordonnee Est-Ouest)
        self.longitude = longitude

        # Stocke la reference vers l'objet User proprietaire
        self.owner = owner

        # Initialise la liste des amenities
        # Si amenities est None, cree une liste vide
        # Cela evite le probleme des arguments mutables par defaut
        self.amenities = amenities if amenities is not None else []

        # Initialise la liste des reviews de la meme maniere
        self.reviews = reviews if reviews is not None else []

        # Valide toutes les donnees entrees
        self.validate()

    def validate(self):
        """
        Validate place attributes according to requirements
        Verifie que tous les attributs respectent les contraintes metier
        """
        # Verification du titre: obligatoire et non vide
        if not self.title or not self.title.strip():
            raise ValueError("Title is required")

        # Le titre ne doit pas depasser 100 caracteres
        if len(self.title) > 100:
            raise ValueError("Title must not exceed 100 characters")

        # Le prix est obligatoire
        if self.price is None:
            raise ValueError("Price is required")

        # Le prix doit etre un nombre (int ou float) et strictement positif
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValueError("Price must be a positive value")

        # La latitude est obligatoire
        if self.latitude is None:
            raise ValueError("Latitude is required")

        # La latitude doit etre un nombre entre -90 et 90 degres
        if not isinstance(self.latitude, (int, float)) or not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")

        # La longitude est obligatoire
        if self.longitude is None:
            raise ValueError("Longitude is required")

        # La longitude doit etre un nombre entre -180 et 180 degres
        if not isinstance(self.longitude, (int, float)) or not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")

        # Un proprietaire est obligatoire
        if not self.owner:
            raise ValueError("Owner is required")

    def add_review(self, review):
        """
        Add a review to the place
        Ajoute un avis a la liste des reviews du lieu

        Args:
            review: Instance Review a ajouter
        """
        # Verifie que la review n'est pas deja dans la liste (evite les doublons)
        if review not in self.reviews:
            # Ajoute la review a la fin de la liste
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Add an amenity to the place
        Ajoute un equipement a la liste des amenities du lieu

        Args:
            amenity: Instance Amenity a ajouter
        """
        # Verifie que l'amenity n'est pas deja dans la liste
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self, include_owner=False, include_amenities=False, include_reviews=False):
        """
        Return dictionary representation of place
        Convertit le lieu en dictionnaire JSON avec options d'inclusion

        Args:
            include_owner (bool): Si True, inclut les details du proprietaire
            include_amenities (bool): Si True, inclut les details des equipements
            include_reviews (bool): Si True, inclut les details des avis
        """
        # Cree le dictionnaire de base avec les attributs principaux
        data = {
            'id': self.id,                              # Identifiant unique du lieu
            'title': self.title,                        # Titre
            'description': self.description,            # Description
            'price': self.price,                        # Prix par nuit
            'latitude': self.latitude,                  # Coordonnee latitude
            'longitude': self.longitude,                # Coordonnee longitude
            'created_at': self.created_at.isoformat(),  # Date creation (format ISO)
            'updated_at': self.updated_at.isoformat()   # Date modification (format ISO)
        }

        # Si on veut inclure les details du proprietaire
        if include_owner and self.owner:
            # Ajoute un sous-dictionnaire avec les infos du proprietaire
            data['owner'] = {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            }
        else:
            # Sinon, inclut juste l'ID du proprietaire
            data['owner_id'] = self.owner.id if self.owner else None

        # Si on veut inclure les details des equipements
        if include_amenities:
            # Cree une liste de dictionnaires avec id et nom de chaque amenity
            # List comprehension: [expression for item in liste]
            data['amenities'] = [
                {'id': amenity.id, 'name': amenity.name}
                for amenity in self.amenities
            ]
        else:
            # Sinon, inclut juste la liste des IDs des amenities
            data['amenity_ids'] = [amenity.id for amenity in self.amenities]

        # Si on veut inclure les details des avis
        if include_reviews:
            # Cree une liste de dictionnaires avec les details de chaque review
            data['reviews'] = [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id
                }
                for review in self.reviews
            ]

        # Retourne le dictionnaire complet
        return data

    def __repr__(self):
        """
        String representation for debugging
        Representation textuelle pour le debug
        """
        return f"<Place {self.id}: {self.title}>"
