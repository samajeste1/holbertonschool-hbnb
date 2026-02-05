"""
Amenity model for HBnB Part 3
Modele d'equipement/commodite avec SQLAlchemy
Represente les equipements disponibles dans un logement (WiFi, Piscine, etc.)

Relations:
- Many-to-Many avec Place via la table d'association place_amenity
"""

# Importe la classe de base pour heriter des attributs communs
from app.models.baseclass import BaseModel

# Importe l'instance SQLAlchemy
from app import db


class Amenity(BaseModel):
    """
    Amenity model representing a feature or service available at a place
    Modele SQLAlchemy pour les equipements/commodites
    Table SQL: 'amenities'

    Examples d'amenities:
        - WiFi
        - Piscine (Pool)
        - Parking
        - Climatisation (Air Conditioning)
        - Cuisine (Kitchen)

    Attributes:
        name (str): Nom de l'equipement (unique)
    """

    # Nom de la table dans la base de donnees
    __tablename__ = 'amenities'

    # Colonnes de base heritees de BaseModel:
    # - id: UUID unique
    # - created_at: date de creation
    # - updated_at: date de derniere modification

    # Nom de l'equipement
    # String(128): max 128 caracteres
    # nullable=False: obligatoire
    # unique=True: chaque nom doit etre unique (pas de doublons)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, name):
        """
        Initialize an Amenity instance
        Cree un nouvel equipement

        Args:
            name (str): Nom de l'equipement (doit etre unique)
        """
        # Initialise la classe parente (genere id et timestamps)
        super().__init__()

        # Stocke le nom de l'equipement
        self.name = name

    def to_dict(self, include_relationships=False):
        """
        Convertir l'objet en dictionnaire pour l'API JSON

        Args:
            include_relationships (bool): Si True, inclut la liste des places
                                         qui ont cet equipement

        Returns:
            dict: Donnees de l'equipement
        """
        # Recupere les champs de base (id, created_at, updated_at)
        result = super().to_dict()

        # Ajoute le nom de l'equipement
        result['name'] = self.name

        # Si demande, inclut les lieux associes
        # place_amenities est defini par le backref dans Place.amenities
        if include_relationships:
            result['places'] = [place.to_dict() for place in self.place_amenities]

        return result

    def __repr__(self):
        """
        String representation for debugging
        Representation textuelle pour le debug
        """
        return f"<Amenity {self.id}: {self.name}>"