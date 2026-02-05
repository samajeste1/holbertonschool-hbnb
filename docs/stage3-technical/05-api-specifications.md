# HBnB - API Specifications (Stage 3)

## Base URL

```
Development: http://localhost:5001/api/v1
Production: https://your-domain.com/api/v1
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

---

## External APIs

**None required** - HBnB is a self-contained application.

---

## Internal API Endpoints

### Authentication Endpoints

#### POST /auth/login
Authenticate user and get JWT token.

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| email | body | string | Yes | User email |
| password | body | string | Yes | User password |

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

---

### User Endpoints

#### GET /users
Get all users.

**Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "is_admin": false
  }
]
```

#### GET /users/{user_id}
Get user by ID.

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "is_admin": false
}
```

#### POST /users
Create new user (Admin only).

**Headers:** `Authorization: Bearer <admin_token>`

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "password123",
  "is_admin": false
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "is_admin": false
}
```

#### PUT /users/{user_id}
Update user.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "first_name": "Jane",
  "last_name": "Doe"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "john@example.com"
}
```

---

### Place Endpoints

#### GET /places
Get all places.

**Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "title": "Beach House",
    "description": "Beautiful beach house",
    "price": 150.0,
    "latitude": 25.7617,
    "longitude": -80.1918,
    "owner_id": "owner-uuid"
  }
]
```

#### GET /places/{place_id}
Get place details with reviews and amenities.

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Beach House",
  "description": "Beautiful beach house",
  "price": 150.0,
  "latitude": 25.7617,
  "longitude": -80.1918,
  "owner": {
    "id": "owner-uuid",
    "first_name": "John",
    "last_name": "Doe"
  },
  "amenities": [
    {"id": "amenity-uuid", "name": "WiFi"},
    {"id": "amenity-uuid", "name": "Pool"}
  ],
  "reviews": [
    {
      "id": "review-uuid",
      "text": "Great place!",
      "rating": 5,
      "user_id": "user-uuid"
    }
  ]
}
```

#### POST /places
Create new place (Authenticated).

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "title": "Beach House",
  "description": "Beautiful beach house",
  "price": 150.0,
  "latitude": 25.7617,
  "longitude": -80.1918,
  "amenities": ["amenity-uuid-1", "amenity-uuid-2"]
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "title": "Beach House",
  "description": "Beautiful beach house",
  "price": 150.0,
  "latitude": 25.7617,
  "longitude": -80.1918,
  "owner_id": "current-user-uuid"
}
```

#### PUT /places/{place_id}
Update place (Owner only).

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "title": "Updated Beach House",
  "price": 175.0
}
```

---

### Review Endpoints

#### GET /reviews
Get all reviews.

#### GET /reviews/{review_id}
Get review by ID.

#### GET /places/{place_id}/reviews
Get all reviews for a place.

**Response (200 OK):**
```json
[
  {
    "id": "review-uuid",
    "text": "Amazing stay!",
    "rating": 5,
    "user_id": "user-uuid",
    "place_id": "place-uuid"
  }
]
```

#### POST /reviews
Create new review (Authenticated).

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "text": "Great experience!",
  "rating": 5,
  "place_id": "place-uuid"
}
```

**Validation:**
- Rating must be 1-5
- User cannot review own place
- Place must exist

#### PUT /reviews/{review_id}
Update review (Author only).

#### DELETE /reviews/{review_id}
Delete review (Author only).

---

### Amenity Endpoints

#### GET /amenities
Get all amenities.

**Response (200 OK):**
```json
[
  {"id": "uuid", "name": "WiFi"},
  {"id": "uuid", "name": "Pool"},
  {"id": "uuid", "name": "Parking"}
]
```

#### GET /amenities/{amenity_id}
Get amenity by ID.

#### POST /amenities
Create amenity (Admin only).

**Request:**
```json
{
  "name": "Air Conditioning"
}
```

#### PUT /amenities/{amenity_id}
Update amenity (Admin only).

---

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing/invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 500 | Internal Server Error |

## API Documentation

Interactive Swagger documentation available at:
```
http://localhost:5001/api/v1/doc/
```
