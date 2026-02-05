"""
Base model class for all SQLAlchemy models
Classe de base pour tous les modeles SQLAlchemy de Part 3
Fournit id, timestamps et methodes communes pour la persistance en base de donnees
"""

# Importe uuid pour generer des identifiants uniques
import uuid

# Importe datetime pour les horodatages
from datetime import datetime

# Importe l'instance db de SQLAlchemy depuis le package app
from app import db


class BaseModel(db.Model):
    """
    Abstract base class for all models
    Classe abstraite dont heritent tous les modeles SQLAlchemy
    db.Model est la classe de base fournie par Flask-SQLAlchemy
    """

    # __abstract__ = True indique a SQLAlchemy de ne pas creer de table pour cette classe
    # Seules les classes filles auront leurs propres tables
    __abstract__ = True

    # Definition des colonnes communes a tous les modeles
    # db.Column definit une colonne dans la table SQL

    # Colonne ID: cle primaire, chaine de 36 caracteres (format UUID)
    # default=lambda: cree un nouvel UUID a chaque insertion
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Colonne date de creation: datetime, valeur par defaut = maintenant
    # nullable=False signifie que cette colonne ne peut pas etre NULL
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Colonne date de modification: datetime
    # onupdate=datetime.utcnow met a jour automatiquement a chaque modification
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self):
        """
        Initialize base model with timestamps
        Initialise le modele avec un ID unique et les horodatages
        """
        # Genere un nouvel UUID
        self.id = str(uuid.uuid4())

        # Utilise datetime.utcnow() pour avoir l'heure UTC (standard)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """
        Update the updated_at timestamp and commit to database
        Sauvegarde l'objet dans la base de donnees
        """
        # Met a jour le timestamp de modification
        self.updated_at = datetime.utcnow()

        # db.session.add() ajoute l'objet a la session SQLAlchemy
        # Si l'objet existe deja, il sera mis a jour
        db.session.add(self)

        # db.session.commit() persiste les changements dans la base
        db.session.commit()

    def delete(self):
        """
        Delete the object from database
        Supprime l'objet de la base de donnees
        """
        # db.session.delete() marque l'objet pour suppression
        db.session.delete(self)

        # commit() execute la suppression
        db.session.commit()

    def to_dict(self):
        """
        Return dictionary representation of model
        Convertit l'objet en dictionnaire (serialisation JSON)
        Cette methode sera etendue par les classes filles
        """
        return {
            'id': self.id,
            # Convertit datetime en ISO 8601 si existe, sinon None
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
