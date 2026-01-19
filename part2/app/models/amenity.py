from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity model representing a facility or service available at a place"""

    def __init__(self, name):
        """
        Initialize an Amenity instance

        Args:
            name (str): Name of the amenity (max 50 chars, required)
        """
        super().__init__()
        self.name = name

        # Validate attributes
        self.validate()

    def validate(self):
        """Validate amenity attributes according to requirements"""
        if not self.name or not self.name.strip():
            raise ValueError("Amenity name is required")
        if len(self.name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")

    def to_dict(self, include_timestamps=True):
        """
        Return dictionary representation of amenity

        Args:
            include_timestamps (bool): Include created_at and updated_at if True
        """
        data = {
            'id': self.id,
            'name': self.name
        }

        if include_timestamps:
            data['created_at'] = self.created_at.isoformat()
            data['updated_at'] = self.updated_at.isoformat()

        return data

    def __repr__(self):
        """String representation for debugging"""
        return f"<Amenity {self.id}: {self.name}>"
