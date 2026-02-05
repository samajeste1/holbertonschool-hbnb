"""
User model for HBnB Part 3
Modele utilisateur avec SQLAlchemy et hachage de mot de passe bcrypt
Inclut l'authentification securisee et les relations avec places et reviews
"""

# Importe la classe de base pour heriter des attributs communs
from app.models.baseclass import BaseModel

# Importe db (SQLAlchemy) et bcrypt (hachage) depuis le package app
from app import db, bcrypt


class User(BaseModel):
    """
    User model representing a user in the HBnB application
    Modele SQLAlchemy pour les utilisateurs
    Table SQL: 'users'
    """

    # Nom de la table dans la base de donnees
    __tablename__ = 'users'

    # Definition des colonnes specifiques aux utilisateurs

    # Prenom: chaine de max 50 caracteres, obligatoire
    first_name = db.Column(db.String(50), nullable=False)

    # Nom: chaine de max 50 caracteres, obligatoire
    last_name = db.Column(db.String(50), nullable=False)

    # Email: chaine de max 120 caracteres, obligatoire et unique
    # unique=True cree un index unique dans la base
    email = db.Column(db.String(120), nullable=False, unique=True)

    # Hash du mot de passe: chaine de 128 caracteres pour stocker le hash bcrypt
    # On ne stocke JAMAIS le mot de passe en clair!
    password_hash = db.Column(db.String(128), nullable=False)

    # Flag admin: booleen, False par defaut
    is_admin = db.Column(db.Boolean, default=False)

    # Definition des relations avec les autres modeles

    # Relation One-to-Many avec Place: un user peut avoir plusieurs places
    # backref='owner' cree un attribut owner sur Place pour acceder au proprietaire
    # lazy=True charge les places a la demande (pas automatiquement)
    # foreign_keys specifie quelle colonne utiliser pour la relation
    places = db.relationship('Place', backref='owner', lazy=True, foreign_keys='Place.owner_id')

    # Relation One-to-Many avec Review: un user peut ecrire plusieurs reviews
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        """
        Initialize a User instance
        Cree un nouvel utilisateur avec hachage automatique du mot de passe

        Args:
            first_name (str): Prenom
            last_name (str): Nom
            email (str): Email (doit etre unique)
            password (str): Mot de passe en clair (sera hache)
            is_admin (bool): Droits administrateur
            **kwargs: Arguments supplementaires ignores
        """
        # Appelle le constructeur parent pour initialiser id et timestamps
        super().__init__()

        # Stocke les attributs utilisateur
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        # Initialise le hash a vide
        self.password_hash = ''

        # Si un mot de passe est fourni, le hacher
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """
        Hash the password using bcrypt
        Hache le mot de passe de maniere securisee avec bcrypt

        Args:
            password (str): Mot de passe en clair a hacher
        """
        # bcrypt.generate_password_hash() cree un hash securise avec salt
        # .decode('utf-8') convertit les bytes en string pour stockage
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verify the password against the hash
        Verifie si le mot de passe fourni correspond au hash stocke

        Args:
            password (str): Mot de passe a verifier

        Returns:
            bool: True si le mot de passe est correct, False sinon
        """
        # bcrypt.check_password_hash() compare de maniere securisee
        # Protege contre les attaques timing
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Return dictionary representation of user
        Convertit en dictionnaire pour l'API JSON
        Note: ne jamais inclure password_hash!
        """
        # Recupere les champs de base depuis le parent
        data = super().to_dict()

        # Ajoute les champs specifiques a l'utilisateur
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
            # password_hash n'est PAS inclus pour des raisons de securite
        })

        return data

    def __repr__(self):
        """
        String representation for debugging
        Representation textuelle pour le debug
        """
        return f"<User {self.id}: {self.first_name} {self.last_name}>"
