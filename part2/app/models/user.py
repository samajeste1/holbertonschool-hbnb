from .base_model import BaseModel

class User(BaseModel):
    """User model representing a user in the HBnB application"""

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a User instance

        Args:
            first_name (str): User's first name (max 50 chars)
            last_name (str): User's last name (max 50 chars)
            email (str): User's email address (must be unique)
            is_admin (bool): Admin privileges flag (default: False)
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.place_list = []  # Initialize empty list (not mutable default)
        self.reviews = []     # Initialize empty list (not mutable default)

        # Validate attributes
        self.validate()

    def validate(self):
        """Validate user attributes according to requirements"""
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name is required")
        if len(self.first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")

        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name is required")
        if len(self.last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")

        if not self.email or not self.email.strip():
            raise ValueError("Email is required")
        # Basic email format validation
        if '@' not in self.email or '.' not in self.email.split('@')[-1]:
            raise ValueError("Invalid email format")

    def to_dict(self):
        """Return dictionary representation of user"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        """String representation for debugging"""
        return f"<User {self.id}: {self.first_name} {self.last_name}>"
