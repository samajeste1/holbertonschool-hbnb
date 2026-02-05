"""
Base Model - Classe de base pour tous les modeles
Fournit les attributs et methodes communs a tous les objets du projet
"""

# Importe uuid pour generer des identifiants uniques universels
import uuid

# Importe datetime pour gerer les dates et heures
from datetime import datetime


class BaseModel:
    """
    Base class for all models with common attributes and methods
    Classe mere dont heritent tous les autres modeles (User, Place, etc.)
    Fournit id unique et timestamps automatiques
    """

    def __init__(self):
        """
        Initialize base model with id and timestamps
        Initialise le modele de base avec un ID unique et les horodatages
        Cette methode est appelee automatiquement a la creation d'un objet
        """
        # Genere un UUID v4 (identifiant unique aleatoire) et le convertit en string
        # Exemple: "550e8400-e29b-41d4-a716-446655440000"
        self.id = str(uuid.uuid4())

        # Stocke la date et heure actuelles comme date de creation
        # datetime.now() retourne l'instant present
        self.created_at = datetime.now()

        # Stocke aussi la date de derniere modification (identique a la creation au debut)
        self.updated_at = datetime.now()

    def save(self):
        """
        Update the updated_at timestamp whenever the object is modified
        Met a jour l'horodatage updated_at quand l'objet est modifie
        Doit etre appelee apres chaque modification de l'objet
        """
        # Remplace updated_at par l'instant present
        self.updated_at = datetime.now()

    def update(self, data: dict):
        """
        Update the attributes of the object based on the provided dictionary
        Met a jour les attributs de l'objet a partir d'un dictionnaire

        Args:
            data (dict): Dictionnaire contenant les nouvelles valeurs
                        Exemple: {'first_name': 'John', 'email': 'john@test.com'}
        """
        # Parcourt chaque paire cle-valeur du dictionnaire
        for key, value in data.items():
            # Verifie si l'objet possede deja cet attribut (securite)
            # hasattr() retourne True si l'attribut existe
            if hasattr(self, key):
                # setattr() modifie la valeur de l'attribut dynamiquement
                # Equivalent a: self.key = value (mais avec un nom de variable)
                setattr(self, key, value)

        # Appelle save() pour mettre a jour le timestamp updated_at
        self.save()
