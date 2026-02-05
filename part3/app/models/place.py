"""
Place model for HBnB Part 3
Modele de lieu/logement avec SQLAlchemy
Inclut les relations Many-to-Many avec Amenity et One-to-Many avec Review
"""

# Importe la classe de base
from app.models.baseclass import BaseModel

# Importe db pour SQLAlchemy
from app import db


# Table d'association pour la relation Many-to-Many Place-Amenity
# Une table d'association est necessaire car:
# - Un lieu peut avoir plusieurs equipements
# - Un equipement peut etre dans plusieurs lieux
# db.Table cree une table SQL simple (pas un modele Python)
place_amenity = db.Table('place_amenity',
    # Colonne place_id: cle etrangere vers la table places
    # primary_key=True fait partie de la cle primaire composite
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),

    # Colonne amenity_id: cle etrangere vers la table amenities
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    """
    Place model representing a rental property
    Modele SQLAlchemy pour les lieux/logements
    Table SQL: 'places'
    """

    # Nom de la table dans la base de donnees
    __tablename__ = 'places'

    # Definition des colonnes

    # Titre du lieu: max 100 caracteres, obligatoire
    title = db.Column(db.String(100), nullable=False)

    # Description: texte long, optionnel (nullable=True par defaut)
    description = db.Column(db.Text, nullable=True)

    # Prix par nuit: nombre decimal, obligatoire
    price = db.Column(db.Float, nullable=False)

    # Coordonnees GPS: obligatoires
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Cle etrangere vers l'utilisateur proprietaire
    # ForeignKey cree la contrainte de cle etrangere en SQL
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Definition des relations

    # Relation One-to-Many avec Review: un lieu peut avoir plusieurs avis
    # cascade='all, delete-orphan': supprime les reviews si le lieu est supprime
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')

    # Relation Many-to-Many avec Amenity via la table d'association place_amenity
    # secondary=place_amenity: utilise la table d'association
    # backref cree l'attribut inverse sur Amenity
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('place_amenities', lazy='dynamic'))

    def __init__(self, title, price, latitude, longitude, owner_id, description='', **kwargs):
        """
        Initialize a Place instance
        Cree un nouveau lieu

        Args:
            title (str): Titre du lieu
            price (float): Prix par nuit
            latitude (float): Coordonnee latitude
            longitude (float): Coordonnee longitude
            owner_id (str): ID du proprietaire (User)
            description (str): Description optionnelle
            **kwargs: Arguments supplementaires ignores
        """
        # Initialise la classe parente
        super().__init__()

        # Stocke les attributs
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    def add_review(self, review):
        """
        Add a review to the place
        Ajoute un avis a ce lieu

        Args:
            review: Instance Review a ajouter
        """
        # Evite les doublons
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Add an amenity to the place
        Ajoute un equipement a ce lieu

        Args:
            amenity: Instance Amenity a ajouter
        """
        # Evite les doublons dans la relation Many-to-Many
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self, include_owner=False, include_amenities=False, include_reviews=False):
        """
        Return dictionary representation of place
        Convertit en dictionnaire pour l'API JSON

        Args:
            include_owner (bool): Inclure les details du proprietaire
            include_amenities (bool): Inclure les details des equipements
            include_reviews (bool): Inclure les details des avis
        """
        # Recupere les champs de base
        data = super().to_dict()

        # Ajoute les champs specifiques au lieu
        data.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        })

        # Si demande, inclut les details du proprietaire
        if include_owner and self.owner:
            data['owner'] = {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            }

        # Gere l'inclusion des amenities
        if include_amenities:
            # Version detaillee avec id et nom
            data['amenities'] = [
                {'id': amenity.id, 'name': amenity.name}
                for amenity in self.amenities
            ]
        else:
            # Version legere avec seulement les IDs
            data['amenity_ids'] = [amenity.id for amenity in self.amenities]

        # Si demande, inclut les reviews
        if include_reviews:
            data['reviews'] = [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id
                }
                for review in self.reviews
            ]

        return data

    def __repr__(self):
        """
        String representation for debugging
        """
        return f"<Place {self.id}: {self.title}>"
