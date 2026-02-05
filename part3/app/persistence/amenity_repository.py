"""
Amenity Repository implementation
"""
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository
from app import db
from sqlalchemy.exc import SQLAlchemyError


class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity model operations"""

    def __init__(self):
        """Initialize with Amenity model"""
        super().__init__(db.session, Amenity)

    def get_amenity_by_name(self, name):
        """
        Get an amenity by name

        Args:
            name: Amenity name

        Returns:
            Amenity if found, None otherwise
        """
        return self.session.query(Amenity).filter(Amenity.name == name).first()

    def get_amenities_by_place(self, place_id):
        """
        Get all amenities for a place

        Args:
            place_id: Place ID

        Returns:
            List of amenities for the place
        """
        from app.models.place import Place
        place = self.session.query(Place).filter(Place.id == place_id).first()
        if place:
            return place.amenities
        return []

    def get_places_with_amenity(self, amenity_id):
        """
        Get all places that have a specific amenity

        Args:
            amenity_id: Amenity ID

        Returns:
            List of places with the amenity
        """
        amenity = self.get(amenity_id)
        if amenity:
            return list(amenity.place_amenities)
        return []

    def update_name(self, amenity_id, new_name):
        """
        Update the name of an amenity

        Args:
            amenity_id: Amenity ID
            new_name: New name

        Returns:
            Updated amenity if found, None otherwise
        """
        try:
            amenity = self.get(amenity_id)
            if amenity:
                amenity.name = new_name
                self.session.commit()
                return amenity
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def search_by_name(self, name):
        """
        Search amenities by name (partial match)

        Args:
            name: Name to search for

        Returns:
            List of matching amenities
        """
        return self.session.query(Amenity).filter(
            Amenity.name.ilike(f"%{name}%")
        ).all()
