"""
Review Model - Modele representant un avis utilisateur
Permet aux utilisateurs de noter et commenter les lieux visites
"""

# Importe BaseModel pour heriter des attributs communs
from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Review model representing a user's review of a place
    Modele representant l'avis d'un utilisateur sur un lieu
    Contient un texte de commentaire et une note de 1 a 5
    """

    def __init__(self, text, rating, place_id, user_id):
        """
        Initialize a Review instance
        Cree un nouvel avis avec son contenu et sa note

        Args:
            text (str): Contenu du commentaire (obligatoire, ne peut pas etre vide)
            rating (int): Note de 1 a 5 etoiles (obligatoire, entier)
            place_id (str): ID du lieu concerne (obligatoire)
            user_id (str): ID de l'utilisateur qui ecrit l'avis (obligatoire)
        """
        # Appelle le constructeur parent pour initialiser id et timestamps
        super().__init__()

        # Stocke le texte du commentaire
        self.text = text

        # Stocke la note (1 a 5)
        self.rating = rating

        # Stocke l'ID du lieu concerne (pas l'objet, juste l'ID)
        self.place_id = place_id

        # Stocke l'ID de l'auteur de l'avis
        self.user_id = user_id

        # Valide toutes les donnees
        self.validate()

    def validate(self):
        """
        Validate review attributes according to requirements
        Verifie que tous les attributs respectent les regles metier
        """
        # Le texte du commentaire est obligatoire et ne doit pas etre vide
        if not self.text or not self.text.strip():
            raise ValueError("Review text is required")

        # La note est obligatoire
        if self.rating is None:
            raise ValueError("Rating is required")

        # La note doit etre un entier entre 1 et 5 inclus
        # isinstance() verifie le type de la variable
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        # L'ID du lieu est obligatoire
        if not self.place_id:
            raise ValueError("Place ID is required")

        # L'ID de l'utilisateur est obligatoire
        if not self.user_id:
            raise ValueError("User ID is required")

    def to_dict(self):
        """
        Return dictionary representation of review
        Convertit l'avis en dictionnaire JSON pour l'API
        """
        return {
            'id': self.id,                              # Identifiant unique de l'avis
            'text': self.text,                          # Texte du commentaire
            'rating': self.rating,                      # Note (1-5)
            'place_id': self.place_id,                  # ID du lieu concerne
            'user_id': self.user_id,                    # ID de l'auteur
            'created_at': self.created_at.isoformat(),  # Date de creation
            'updated_at': self.updated_at.isoformat()   # Date de modification
        }

    def __repr__(self):
        """
        String representation for debugging
        Representation textuelle pour le debug
        Affiche la note et le lieu concerne
        """
        return f"<Review {self.id}: {self.rating}/5 for Place {self.place_id}>"
