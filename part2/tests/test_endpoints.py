#!/usr/bin/env python3
"""
Unit tests for HBnB Part 2 API Endpoints
Usage: python -m pytest tests/test_endpoints.py -v
       or
       python -m unittest tests/test_endpoints.py
"""

import unittest
import json
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    """Test cases for User endpoints"""

    def setUp(self):
        """Set up test client"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_create_user_success(self):
        """Test successful user creation"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'Jane')
        self.assertEqual(data['email'], 'jane.doe@example.com')

    def test_create_user_invalid_email(self):
        """Test user creation with invalid email"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_fields(self):
        """Test user creation with empty required fields"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "test@test.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email"""
        # Create first user
        self.client.post('/api/v1/users/', json={
            "first_name": "First",
            "last_name": "User",
            "email": "duplicate@test.com"
        })
        # Try to create second user with same email
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Second",
            "last_name": "User",
            "email": "duplicate@test.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        """Test retrieving all users"""
        # Create a user first
        self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@test.com"
        })
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_user_by_id(self):
        """Test retrieving a user by ID"""
        # Create a user
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Get",
            "last_name": "Test",
            "email": "get.test@test.com"
        })
        user_id = json.loads(create_response.data)['id']

        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)

    def test_get_user_not_found(self):
        """Test retrieving a non-existent user"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """Test updating a user"""
        # Create a user
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Update",
            "last_name": "Test",
            "email": "update.test@test.com"
        })
        user_id = json.loads(create_response.data)['id']

        # Update the user
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated.user@test.com"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')


class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for Amenity endpoints"""

    def setUp(self):
        """Set up test client"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_create_amenity_success(self):
        """Test successful amenity creation"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Wi-Fi')

    def test_create_amenity_empty_name(self):
        """Test amenity creation with empty name"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        # Create an amenity first
        self.client.post('/api/v1/amenities/', json={"name": "Pool"})

        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_update_amenity(self):
        """Test updating an amenity"""
        # Create amenity
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Old Name"
        })
        amenity_id = json.loads(create_response.data)['id']

        # Update amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "New Name"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Amenity updated successfully')


class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for Place endpoints"""

    def setUp(self):
        """Set up test client and create required entities"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        # Create a user to be owner
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner@test.com"
        })
        self.owner_id = json.loads(user_response.data)['id']

        # Create an amenity
        amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "Parking"
        })
        self.amenity_id = json.loads(amenity_response.data)['id']

    def test_create_place_success(self):
        """Test successful place creation"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": [self.amenity_id]
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Cozy Apartment')

    def test_create_place_invalid_price(self):
        """Test place creation with negative price"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": -50.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        """Test place creation with out-of-range latitude"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": 100.0,  # Invalid
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        """Test place creation with out-of-range longitude"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -200.0,  # Invalid
            "owner_id": self.owner_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        """Test retrieving all places"""
        # Create a place
        self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        })

        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_place_with_details(self):
        """Test retrieving a place with owner and amenities details"""
        # Create place
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Detailed Place",
            "price": 150.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": [self.amenity_id]
        })
        place_id = json.loads(create_response.data)['id']

        # Get place details
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('owner', data)
        self.assertIn('amenities', data)

    def test_update_place(self):
        """Test updating a place"""
        # Create place
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Old Title",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        })
        place_id = json.loads(create_response.data)['id']

        # Update place
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "New Title",
            "price": 200.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Place updated successfully')


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for Review endpoints"""

    def setUp(self):
        """Set up test client and create required entities"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        # Create user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "reviewer@test.com"
        })
        self.user_id = json.loads(user_response.data)['id']

        # Create owner
        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Place",
            "last_name": "Owner",
            "email": "placeowner@test.com"
        })
        self.owner_id = json.loads(owner_response.data)['id']

        # Create place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        })
        self.place_id = json.loads(place_response.data)['id']

    def test_create_review_success(self):
        """Test successful review creation"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['rating'], 5)

    def test_create_review_invalid_rating(self):
        """Test review creation with invalid rating"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Test review",
            "rating": 10,  # Invalid
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        """Test retrieving all reviews"""
        # Create a review
        self.client.post('/api/v1/reviews/', json={
            "text": "Good!",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_reviews_by_place(self):
        """Test retrieving reviews for a specific place"""
        # Create review
        self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })

        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_update_review(self):
        """Test updating a review"""
        # Create review
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Old text",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = json.loads(create_response.data)['id']

        # Update review
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated text",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Review updated successfully')

    def test_delete_review(self):
        """Test deleting a review"""
        # Create review
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "To be deleted",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = json.loads(create_response.data)['id']

        # Delete review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Review deleted successfully')

        # Verify it's deleted
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
