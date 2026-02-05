"""
User Model - Modele representant un utilisateur
Herite de BaseModel pour avoir id et timestamps automatiques
"""

# Importe BaseModel depuis le meme package (models)
# Le point signifie "importer depuis le dossier courant"
from .base_model import BaseModel


class User(BaseModel):
    """
    User model representing a user in the HBnB application
    Modele utilisateur pour l'application de location HBnB
    Un utilisateur peut posseder des places et ecrire des reviews
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a User instance
        Cree un nouvel utilisateur avec ses informations

        Args:
            first_name (str): Prenom de l'utilisateur (max 50 caracteres)
            last_name (str): Nom de famille (max 50 caracteres)
            email (str): Adresse email (doit etre unique dans le systeme)
            is_admin (bool): True si admin, False sinon (defaut: False)
        """
        # Appelle le constructeur de BaseModel pour initialiser id, created_at, updated_at
        # super() fait reference a la classe parente
        super().__init__()

        # Stocke le prenom de l'utilisateur
        self.first_name = first_name

        # Stocke le nom de famille
        self.last_name = last_name

        # Stocke l'email (sera utilise pour identifier l'utilisateur)
        self.email = email

        # Indique si l'utilisateur a des droits administrateur
        self.is_admin = is_admin

        # Initialise une liste vide pour stocker les places possedees par l'utilisateur
        # Important: ne pas utiliser [] comme valeur par defaut dans les parametres
        # car les listes sont mutables et partagees entre instances
        self.place_list = []

        # Liste vide pour les reviews ecrites par cet utilisateur
        self.reviews = []

        # Appelle la methode de validation pour verifier les donnees
        self.validate()

    def validate(self):
        """
        Validate user attributes according to requirements
        Verifie que les attributs respectent les regles metier
        Leve une ValueError si une regle n'est pas respectee
        """
        # Verifie que le prenom existe et n'est pas vide (apres suppression des espaces)
        # strip() enleve les espaces au debut et a la fin
        if not self.first_name or not self.first_name.strip():
            # Leve une exception avec un message d'erreur explicite
            raise ValueError("First name is required")

        # Verifie que le prenom ne depasse pas 50 caracteres
        if len(self.first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")

        # Memes verifications pour le nom de famille
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name is required")

        if len(self.last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")

        # Verifie que l'email existe et n'est pas vide
        if not self.email or not self.email.strip():
            raise ValueError("Email is required")

        # Validation basique du format email:
        # - Doit contenir un @
        # - Doit avoir un . apres le @
        # split('@')[-1] prend la partie apres le @
        if '@' not in self.email or '.' not in self.email.split('@')[-1]:
            raise ValueError("Invalid email format")

    def to_dict(self):
        """
        Return dictionary representation of user
        Convertit l'objet User en dictionnaire pour l'API JSON
        Utile pour serialiser l'objet et l'envoyer en reponse HTTP
        """
        return {
            'id': self.id,                              # Identifiant unique
            'first_name': self.first_name,              # Prenom
            'last_name': self.last_name,                # Nom
            'email': self.email,                        # Email
            'is_admin': self.is_admin,                  # Statut admin
            # isoformat() convertit datetime en string ISO 8601: "2024-01-15T10:30:00"
            'created_at': self.created_at.isoformat(),  # Date de creation
            'updated_at': self.updated_at.isoformat()   # Date de modification
        }

    def __repr__(self):
        """
        String representation for debugging
        Representation textuelle pour le debug et les logs
        Appelee par print() ou lors de l'inspection en debug
        """
        # f-string pour formater la chaine avec les variables
        return f"<User {self.id}: {self.first_name} {self.last_name}>"
