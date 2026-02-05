"""
SQLAlchemy Repository base class implementation
"""
from abc import ABC, abstractmethod
from app import db
from sqlalchemy.exc import SQLAlchemyError


class Repository(ABC):
    """Abstract base repository class"""

    @abstractmethod
    def add(self, obj):
        """Add an object to the repository"""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by ID"""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects"""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object"""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object"""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute"""
        pass


class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of the repository pattern"""

    def __init__(self, session, model_class):
        """
        Initialize the repository with a session and model class

        Args:
            session: SQLAlchemy session
            model_class: The model class this repository manages
        """
        self.session = session
        self.model_class = model_class

    def add(self, obj):
        """
        Add an object to the database

        Args:
            obj: Object to add

        Returns:
            The added object
        """
        try:
            self.session.add(obj)
            self.session.commit()
            return obj
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def get(self, obj_id):
        """
        Retrieve an object by ID

        Args:
            obj_id: Unique identifier

        Returns:
            Object if found, None otherwise
        """
        return self.session.query(self.model_class).filter_by(id=obj_id).first()

    def get_all(self):
        """
        Retrieve all objects

        Returns:
            List of all objects
        """
        return self.session.query(self.model_class).all()

    def update(self, obj_id, data):
        """
        Update an object with new data

        Args:
            obj_id: Unique identifier
            data: Dictionary of attributes to update

        Returns:
            Updated object if found, None otherwise
        """
        try:
            obj = self.get(obj_id)
            if obj:
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                self.session.commit()
                return obj
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def delete(self, obj_id):
        """
        Delete an object by ID

        Args:
            obj_id: Unique identifier

        Returns:
            True if deleted, False if not found
        """
        try:
            obj = self.get(obj_id)
            if obj:
                self.session.delete(obj)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            raise

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve objects matching an attribute value

        Args:
            attr_name: Name of the attribute
            attr_value: Value to match

        Returns:
            List of matching objects or single object
        """
        if hasattr(self.model_class, attr_name):
            results = self.session.query(self.model_class).filter(
                getattr(self.model_class, attr_name) == attr_value
            ).all()
            # Return single result if only one, otherwise return list
            if len(results) == 1:
                return results[0]
            return results if results else None
        return None
