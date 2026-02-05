"""
User Repository implementation
"""
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from app import db
from sqlalchemy.exc import SQLAlchemyError


class UserRepository(SQLAlchemyRepository):
    """Repository for User model operations"""

    def __init__(self):
        """Initialize with User model"""
        super().__init__(db.session, User)

    def is_email_available(self, email, exclude_user_id=None):
        """
        Check if an email is available

        Args:
            email: Email to check
            exclude_user_id: Optional user ID to exclude from check

        Returns:
            True if email is available, False otherwise
        """
        query = self.session.query(User).filter(User.email == email)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        return query.first() is None

    def get_by_email(self, email):
        """
        Get user by email

        Args:
            email: User's email address

        Returns:
            User if found, None otherwise
        """
        return self.session.query(User).filter(User.email == email).first()

    def get_admins(self):
        """
        Get all admin users

        Returns:
            List of admin users
        """
        return self.session.query(User).filter(User.is_admin == True).all()

    def search_by_name(self, name):
        """
        Search users by name (first or last)

        Args:
            name: Name to search for

        Returns:
            List of matching users
        """
        search_term = f"%{name}%"
        return self.session.query(User).filter(
            db.or_(
                User.first_name.ilike(search_term),
                User.last_name.ilike(search_term)
            )
        ).all()
