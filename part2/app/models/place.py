from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place model representing a rental property in the HBnB application"""

    def __init__(self, title, description, price, latitude, longitude, owner, amenities=None, reviews=None):
        """
        Initialize a Place instance

        Args:
            title (str): Title of the place (max 100 chars)
            description (str): Detailed description (optional)
            price (float): Price per night (must be positive)
            latitude (float): Latitude coordinate (-90.0 to 90.0)
            longitude (float): Longitude coordinate (-180.0 to 180.0)
            owner: User instance who owns the place
            amenities (list): List of amenity instances (optional)
            reviews (list): List of review instances (optional)
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.amenities = amenities if amenities is not None else []
        self.reviews = reviews if reviews is not None else []

        # Validate attributes
        self.validate()

    def validate(self):
        """Validate place attributes according to requirements"""
        if not self.title or not self.title.strip():
            raise ValueError("Title is required")
        if len(self.title) > 100:
            raise ValueError("Title must not exceed 100 characters")

        if self.price is None:
            raise ValueError("Price is required")
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValueError("Price must be a positive value")

        if self.latitude is None:
            raise ValueError("Latitude is required")
        if not isinstance(self.latitude, (int, float)) or not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")

        if self.longitude is None:
            raise ValueError("Longitude is required")
        if not isinstance(self.longitude, (int, float)) or not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")

        if not self.owner:
            raise ValueError("Owner is required")

    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self, include_owner=False, include_amenities=False, include_reviews=False):
        """
        Return dictionary representation of place

        Args:
            include_owner (bool): Include owner details
            include_amenities (bool): Include amenity details
            include_reviews (bool): Include review details
        """
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        # Include owner details if requested
        if include_owner and self.owner:
            data['owner'] = {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            }
        else:
            data['owner_id'] = self.owner.id if self.owner else None

        # Include amenities if requested
        if include_amenities:
            data['amenities'] = [
                {'id': amenity.id, 'name': amenity.name}
                for amenity in self.amenities
            ]
        else:
            data['amenity_ids'] = [amenity.id for amenity in self.amenities]

        # Include reviews if requested
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
        """String representation for debugging"""
        return f"<Place {self.id}: {self.title}>"
