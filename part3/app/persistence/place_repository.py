"""
Place Repository implementation
"""
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository
from app import db
from sqlalchemy.exc import SQLAlchemyError
from math import radians, cos, sin, asin, sqrt


class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place model operations"""

    def __init__(self):
        """Initialize with Place model"""
        super().__init__(db.session, Place)

    def get_places_by_location(self, latitude, longitude, radius=10):
        """
        Get places within a radius of a location (in km)
        Uses Haversine formula for distance calculation

        Args:
            latitude: Center latitude
            longitude: Center longitude
            radius: Search radius in kilometers

        Returns:
            List of places within the radius
        """
        places = self.get_all()
        nearby_places = []

        for place in places:
            distance = self._haversine(latitude, longitude, place.latitude, place.longitude)
            if distance <= radius:
                nearby_places.append(place)

        return nearby_places

    def _haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points

        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates

        Returns:
            Distance in kilometers
        """
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of Earth in kilometers
        return c * r

    def get_places_by_price_range(self, min_price, max_price):
        """
        Get places within a price range

        Args:
            min_price: Minimum price
            max_price: Maximum price

        Returns:
            List of places within the price range
        """
        return self.session.query(Place).filter(
            Place.price.between(min_price, max_price)
        ).all()

    def get_places_by_title(self, title):
        """
        Search places by title (partial match)

        Args:
            title: Title to search for

        Returns:
            List of matching places
        """
        return self.session.query(Place).filter(
            Place.title.ilike(f"%{title}%")
        ).all()

    def get_places_by_owner(self, owner_id):
        """
        Get all places owned by a user

        Args:
            owner_id: Owner's user ID

        Returns:
            List of places owned by the user
        """
        return self.session.query(Place).filter(Place.owner_id == owner_id).all()

    def update_location(self, place_id, latitude, longitude):
        """
        Update the location of a place

        Args:
            place_id: Place ID
            latitude: New latitude
            longitude: New longitude

        Returns:
            Updated place if found, None otherwise
        """
        try:
            place = self.get(place_id)
            if place:
                place.latitude = latitude
                place.longitude = longitude
                self.session.commit()
                return place
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            raise
