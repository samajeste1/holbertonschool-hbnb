from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review model representing a user's review of a place"""

    def __init__(self, text, rating, place_id, user_id):
        """
        Initialize a Review instance

        Args:
            text (str): Content of the review (required)
            rating (int): Rating from 1 to 5
            place_id (str): ID of the place being reviewed
            user_id (str): ID of the user who wrote the review
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

        # Validate attributes
        self.validate()

    def validate(self):
        """Validate review attributes according to requirements"""
        if not self.text or not self.text.strip():
            raise ValueError("Review text is required")

        if self.rating is None:
            raise ValueError("Rating is required")
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        if not self.place_id:
            raise ValueError("Place ID is required")

        if not self.user_id:
            raise ValueError("User ID is required")

    def to_dict(self):
        """Return dictionary representation of review"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        """String representation for debugging"""
        return f"<Review {self.id}: {self.rating}/5 for Place {self.place_id}>"
