"""
HBnB Facade Pattern Implementation
This module provides a simplified interface to the business logic layer
"""
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """Main facade to manage business logic for users, places, reviews, and amenities."""

    def __init__(self):
        """Initialize facade with in-memory repositories"""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ===== USER METHODS =====

    def create_user(self, user_data):
        """
        Create a new user and add it to the repository.

        Args:
            user_data (dict): Dictionary containing user information

        Returns:
            User: The created user instance
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by ID.

        Args:
            user_id (str): The user's unique identifier

        Returns:
            User: The user instance or None
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a user by email.

        Args:
            email (str): The user's email address

        Returns:
            User: The user instance or None
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Return all users.

        Returns:
            list: List of all user instances
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        """
        Update an existing user with new data.

        Args:
            user_id (str): The user's unique identifier
            update_data (dict): Dictionary containing updated user information

        Returns:
            User: The updated user instance or None if not found
        """
        user = self.get_user(user_id)
        if not user:
            return None

        # Update only allowed fields
        for key, value in update_data.items():
            if hasattr(user, key) and key not in ['id', 'created_at']:
                setattr(user, key, value)

        user.save()  # Update timestamp
        return user

    # ===== PLACE METHODS =====

    def create_place(self, place_data):
        """
        Create a new place.

        Args:
            place_data (dict): Dictionary containing place information

        Returns:
            Place: The created place instance

        Raises:
            ValueError: If owner_id is invalid
        """
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Invalid owner_id")

        # Get amenities if provided
        amenities = []
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    amenities.append(amenity)

        # Create place with proper attribute names
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner,
            amenities=amenities,
            reviews=[]
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Retrieve a place by ID.

        Args:
            place_id (str): The place's unique identifier

        Returns:
            Place: The place instance or None
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Return all places.

        Returns:
            list: List of all place instances
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, update_data):
        """
        Update an existing place with new data.

        Args:
            place_id (str): The place's unique identifier
            update_data (dict): Dictionary containing updated place information

        Returns:
            Place: The updated place instance

        Raises:
            ValueError: If place not found
        """
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        # Update only allowed fields
        allowed_fields = ['title', 'description', 'price', 'latitude', 'longitude']
        for key, value in update_data.items():
            if key in allowed_fields:
                setattr(place, key, value)

        place.save()  # Update timestamp
        return place

    # ===== AMENITY METHODS =====

    def create_amenity(self, amenity_data):
        """
        Create a new amenity if valid.

        Args:
            amenity_data (dict): Dictionary containing amenity information

        Returns:
            Amenity: The created amenity instance
        """
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID.

        Args:
            amenity_id (str): The amenity's unique identifier

        Returns:
            Amenity: The amenity instance or None
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Return all amenities.

        Returns:
            list: List of all amenity instances
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity with new data.

        Args:
            amenity_id (str): The amenity's unique identifier
            amenity_data (dict): Dictionary containing updated amenity information

        Returns:
            Amenity: The updated amenity instance or None if not found

        Raises:
            ValueError: If amenity name is invalid
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
            amenity.validate()  # Re-validate after update
            amenity.save()

        return amenity

    # ===== REVIEW METHODS =====

    def create_review(self, review_data):
        """
        Create a new review.

        Args:
            review_data (dict): Dictionary containing review information

        Returns:
            Review: The created review instance

        Raises:
            ValueError: If place_id or user_id is invalid
        """
        # Verify that place and user exist
        place = self.place_repo.get(review_data['place_id'])
        user = self.user_repo.get(review_data['user_id'])

        if not place:
            raise ValueError("Invalid place_id")
        if not user:
            raise ValueError("Invalid user_id")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )
        self.review_repo.add(review)

        # Add review to place's review list
        place.add_review(review)

        return review

    def get_review(self, review_id):
        """
        Retrieve a review by ID.

        Args:
            review_id (str): The review's unique identifier

        Returns:
            Review: The review instance or None
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Return all reviews.

        Returns:
            list: List of all review instances
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Return all reviews for a specific place.

        Args:
            place_id (str): The place's unique identifier

        Returns:
            list: List of review instances for the place
        """
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def get_reviews_by_user(self, user_id):
        """
        Return all reviews by a specific user.

        Args:
            user_id (str): The user's unique identifier

        Returns:
            list: List of review instances by the user
        """
        return [review for review in self.review_repo.get_all() if review.user_id == user_id]

    def update_review(self, review_id, update_data):
        """
        Update an existing review.

        Args:
            review_id (str): The review's unique identifier
            update_data (dict): Dictionary containing updated review information

        Returns:
            Review: The updated review instance or None if not found
        """
        review = self.get_review(review_id)
        if not review:
            return None

        # Update only allowed fields
        allowed_fields = ['text', 'rating']
        for key, value in update_data.items():
            if key in allowed_fields:
                setattr(review, key, value)

        review.validate()  # Re-validate after update
        review.save()

        return review

    def delete_review(self, review_id):
        """
        Delete a review by ID.

        Args:
            review_id (str): The review's unique identifier

        Returns:
            bool: True if deleted, False if not found
        """
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False
