"""
Amenity Model - Modele representant un equipement/service
Exemples: WiFi, Parking, Piscine, Climatisation, etc.
"""

# Importe BaseModel pour heriter des attributs communs
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity model representing a facility or service available at a place
    Modele representant un equipement ou service disponible dans un lieu
    Les amenities sont partagees entre plusieurs places
    """

    def __init__(self, name):
        """
        Initialize an Amenity instance
        Cree un nouvel equipement avec son nom

        Args:
            name (str): Nom de l'equipement (max 50 caracteres, obligatoire)
                       Exemples: "WiFi", "Parking", "Pool", "Air conditioning"
        """
        # Appelle le constructeur parent pour initialiser id et timestamps
        super().__init__()

        # Stocke le nom de l'equipement
        self.name = name

        # Valide que le nom respecte les contraintes
        self.validate()

    def validate(self):
        """
        Validate amenity attributes according to requirements
        Verifie que le nom de l'equipement est valide
        """
        # Le nom est obligatoire et ne doit pas etre vide
        # strip() enleve les espaces pour eviter les noms avec seulement des espaces
        if not self.name or not self.name.strip():
            raise ValueError("Amenity name is required")

        # Le nom ne doit pas depasser 50 caracteres
        if len(self.name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")

    def to_dict(self, include_timestamps=True):
        """
        Return dictionary representation of amenity
        Convertit l'equipement en dictionnaire JSON

        Args:
            include_timestamps (bool): Si True, inclut created_at et updated_at
                                      Utile pour les reponses API simplifiees
        """
        # Cree le dictionnaire de base
        data = {
            'id': self.id,      # Identifiant unique
            'name': self.name   # Nom de l'equipement
        }

        # Ajoute les timestamps si demande
        if include_timestamps:
            # Convertit datetime en format ISO 8601 pour JSON
            data['created_at'] = self.created_at.isoformat()
            data['updated_at'] = self.updated_at.isoformat()

        return data

    def __repr__(self):
        """
        String representation for debugging
        Representation textuelle pour le debug
        """
        return f"<Amenity {self.id}: {self.name}>"
