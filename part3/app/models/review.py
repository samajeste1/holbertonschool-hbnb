"""
Review model for HBnB Part 3
Modele d'avis/commentaire avec SQLAlchemy
Permet aux utilisateurs de noter et commenter les lieux

Relations:
- Appartient a un Place (Many-to-One)
- Appartient a un User (Many-to-One)
"""

# Importe la classe de base pour heriter des attributs communs (id, timestamps)
from app.models.baseclass import BaseModel

# Importe l'instance SQLAlchemy pour definir les colonnes
from app import db


class Review(BaseModel):
    """
    Review model representing a user's review of a place
    Modele SQLAlchemy pour les avis utilisateurs
    Table SQL: 'reviews'

    Attributes:
        text (str): Contenu textuel de l'avis
        rating (int): Note de 1 a 5 etoiles
        place_id (str): ID du lieu concerne (cle etrangere)
        user_id (str): ID de l'auteur (cle etrangere)
    """

    # Nom de la table dans la base de donnees
    __tablename__ = 'reviews'

    # Colonnes de la table

    # Texte de l'avis: type TEXT pour permettre de longs commentaires
    text = db.Column(db.Text, nullable=False)

    # Note: entier de 1 a 5 (validation dans __init__)
    rating = db.Column(db.Integer, nullable=False)

    # Cle etrangere vers la table places
    # String(36) pour stocker les UUIDs
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Cle etrangere vers la table users (auteur de l'avis)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id, **kwargs):
        """
        Initialize a Review instance
        Cree un nouvel avis avec validation automatique

        Args:
            text (str): Contenu de l'avis (obligatoire, non vide)
            rating (int): Note de 1 a 5
            place_id (str): UUID du lieu
            user_id (str): UUID de l'auteur
            **kwargs: Arguments supplementaires ignores

        Raises:
            ValueError: Si les donnees sont invalides
        """
        # Initialise la classe parente (genere id et timestamps)
        super().__init__()

        # Stocke les attributs
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

        # Valide les donnees avant de sauvegarder
        self.validate()

    def validate(self):
        """
        Validate review attributes
        Verifie que les donnees de l'avis sont valides

        Raises:
            ValueError: Si le texte est vide ou la note invalide
        """
        # Verifie que le texte n'est pas vide
        if not self.text or not self.text.strip():
            raise ValueError("Review text is required")

        # Verifie que la note est fournie
        if self.rating is None:
            raise ValueError("Rating is required")

        # Verifie que la note est un entier entre 1 et 5
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

    def to_dict(self):
        """
        Return dictionary representation of review
        Convertit l'avis en dictionnaire pour l'API JSON

        Returns:
            dict: Donnees de l'avis incluant id, timestamps, text, rating, place_id, user_id
        """
        # Recupere les champs de base (id, created_at, updated_at)
        data = super().to_dict()

        # Ajoute les champs specifiques a l'avis
        data.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
        })

        return data

    def __repr__(self):
        """
        String representation for debugging
        Representation textuelle pour le debug et les logs
        """
        return f"<Review {self.id}: {self.rating}/5 for Place {self.place_id}>"
