# Task 2: Sequence Diagrams for API Calls

## Overview
This document presents four sequence diagrams illustrating the interaction flow between the Presentation, Business Logic, and Persistence layers for key API operations in the HBnB Evolution application.

---

## 1. User Registration Sequence Diagram

### API Call: POST /api/users (User Registration)

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Service as User Service
    participant Facade
    participant User as User Model
    participant Repo as Repository
    participant DB as Database

    Client->>API: POST /api/users<br/>{first_name, last_name, email, password}

    activate API
    API->>API: Validate request format

    alt Invalid request format
        API-->>Client: 400 Bad Request
    end

    API->>Service: register_user(user_data)
    activate Service

    Service->>Facade: create_user(user_data)
    activate Facade

    Facade->>Facade: Check email uniqueness

    alt Email already exists
        Facade-->>Service: Error: Email exists
        Service-->>API: 409 Conflict
        API-->>Client: 409 Conflict
    end

    Facade->>User: new User(first_name, last_name, email, password)
    activate User

    User->>User: Generate UUID
    User->>User: Set created_at, updated_at
    User->>User: hash_password()
    User->>User: validate_email()

    User-->>Facade: User instance
    deactivate User

    Facade->>Repo: save(user)
    activate Repo

    Repo->>DB: INSERT INTO users...
    activate DB
    DB-->>Repo: Success
    deactivate DB

    Repo-->>Facade: Saved user object
    deactivate Repo

    Facade-->>Service: User created
    deactivate Facade

    Service-->>API: User DTO
    deactivate Service

    API-->>Client: 201 Created<br/>{id, email, created_at}
    deactivate API
```

### Flow Description:
1. **Client** sends POST request with user data to API endpoint
2. **API** validates request format
3. **Service** receives validated data and calls Facade
4. **Facade** checks if email is unique
5. **User Model** is instantiated with:
   - UUID generation
   - Password hashing
   - Email validation
   - Timestamp initialization
6. **Repository** persists user to database
7. **Response** flows back through layers
8. **Client** receives 201 Created with user information

---

## 2. Place Creation Sequence Diagram

### API Call: POST /api/places (Create Place)

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Auth as Auth Middleware
    participant Service as Place Service
    participant Facade
    participant Place as Place Model
    participant User as User Model
    participant Repo as Repository
    participant DB as Database

    Client->>API: POST /api/places<br/>{title, description, price, latitude, longitude, amenities[]}

    activate API
    API->>Auth: Verify authentication token
    activate Auth

    alt Invalid or missing token
        Auth-->>API: 401 Unauthorized
        API-->>Client: 401 Unauthorized
    end

    Auth-->>API: User authenticated (user_id)
    deactivate Auth

    API->>API: Validate request data

    API->>Service: create_place(place_data, user_id)
    activate Service

    Service->>Facade: create_place(place_data, user_id)
    activate Facade

    Facade->>Repo: get_user(user_id)
    activate Repo
    Repo->>DB: SELECT * FROM users WHERE id=?
    activate DB
    DB-->>Repo: User data
    deactivate DB
    Repo-->>Facade: User instance
    deactivate Repo

    alt User not found
        Facade-->>Service: Error: User not found
        Service-->>API: 404 Not Found
        API-->>Client: 404 Not Found
    end

    Facade->>Place: new Place(title, description, price, lat, lon, user_id)
    activate Place

    Place->>Place: Generate UUID
    Place->>Place: Set created_at, updated_at
    Place->>Place: validate_coordinates()
    Place->>Place: validate_price()

    Place-->>Facade: Place instance
    deactivate Place

    loop For each amenity_id in amenities
        Facade->>Repo: get_amenity(amenity_id)
        activate Repo
        Repo->>DB: SELECT * FROM amenities WHERE id=?
        activate DB
        DB-->>Repo: Amenity data
        deactivate DB
        Repo-->>Facade: Amenity instance
        deactivate Repo
        Facade->>Place: add_amenity(amenity)
    end

    Facade->>Repo: save(place)
    activate Repo
    Repo->>DB: INSERT INTO places...
    activate DB
    DB-->>Repo: Success
    deactivate DB
    Repo-->>Facade: Saved place object
    deactivate Repo

    Facade->>Repo: save_place_amenities(place_id, amenity_ids)
    activate Repo
    Repo->>DB: INSERT INTO place_amenities...
    activate DB
    DB-->>Repo: Success
    deactivate DB
    Repo-->>Facade: Success
    deactivate Repo

    Facade-->>Service: Place created
    deactivate Facade

    Service-->>API: Place DTO
    deactivate Service

    API-->>Client: 201 Created<br/>{id, title, price, amenities[], created_at}
    deactivate API
```

### Flow Description:
1. **Client** sends POST request with place data
2. **Auth Middleware** verifies user authentication
3. **API** validates request data format
4. **Facade** verifies user exists
5. **Place Model** is instantiated with validation:
   - Coordinates validation
   - Price validation
   - UUID generation
6. **Facade** retrieves and associates amenities
7. **Repository** persists place and amenity associations
8. **Client** receives 201 Created with place details

---

## 3. Review Submission Sequence Diagram

### API Call: POST /api/places/{place_id}/reviews (Submit Review)

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Auth as Auth Middleware
    participant Service as Review Service
    participant Facade
    participant Review as Review Model
    participant Place as Place Model
    participant Repo as Repository
    participant DB as Database

    Client->>API: POST /api/places/{place_id}/reviews<br/>{text, rating}

    activate API
    API->>Auth: Verify authentication token
    activate Auth

    alt Invalid token
        Auth-->>API: 401 Unauthorized
        API-->>Client: 401 Unauthorized
    end

    Auth-->>API: User authenticated (user_id)
    deactivate Auth

    API->>API: Validate request data<br/>(rating 1-5, text not empty)

    API->>Service: create_review(place_id, user_id, review_data)
    activate Service

    Service->>Facade: create_review(place_id, user_id, review_data)
    activate Facade

    Facade->>Repo: get_place(place_id)
    activate Repo
    Repo->>DB: SELECT * FROM places WHERE id=?
    activate DB
    DB-->>Repo: Place data
    deactivate DB
    Repo-->>Facade: Place instance
    deactivate Repo

    alt Place not found
        Facade-->>Service: Error: Place not found
        Service-->>API: 404 Not Found
        API-->>Client: 404 Not Found
    end

    Facade->>Facade: Check if user already reviewed this place

    Facade->>Repo: get_review_by_user_and_place(user_id, place_id)
    activate Repo
    Repo->>DB: SELECT * FROM reviews WHERE user_id=? AND place_id=?
    activate DB
    DB-->>Repo: Review data or null
    deactivate DB
    Repo-->>Facade: Existing review or null
    deactivate Repo

    alt User already reviewed
        Facade-->>Service: Error: Already reviewed
        Service-->>API: 409 Conflict
        API-->>Client: 409 Conflict<br/>"You have already reviewed this place"
    end

    Facade->>Review: new Review(text, rating, user_id, place_id)
    activate Review

    Review->>Review: Generate UUID
    Review->>Review: Set created_at, updated_at
    Review->>Review: validate_rating()
    Review->>Review: validate_text()

    Review-->>Facade: Review instance
    deactivate Review

    Facade->>Repo: save(review)
    activate Repo
    Repo->>DB: INSERT INTO reviews...
    activate DB
    DB-->>Repo: Success
    deactivate DB
    Repo-->>Facade: Saved review object
    deactivate Repo

    Facade->>Place: add_review(review)

    Facade-->>Service: Review created
    deactivate Facade

    Service-->>API: Review DTO
    deactivate Service

    API-->>Client: 201 Created<br/>{id, rating, text, created_at}
    deactivate API
```

### Flow Description:
1. **Client** sends POST request to review a place
2. **Auth Middleware** verifies user is authenticated
3. **API** validates review data (rating range, text presence)
4. **Facade** verifies place exists
5. **Facade** checks if user has already reviewed this place
6. **Review Model** is created with validation:
   - Rating must be 1-5
   - Text must not be empty
7. **Repository** persists review
8. **Place** is updated with new review reference
9. **Client** receives 201 Created with review details

---

## 4. Fetching List of Places Sequence Diagram

### API Call: GET /api/places (Fetch All Places)

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Service as Place Service
    participant Facade
    participant Repo as Repository
    participant DB as Database

    Client->>API: GET /api/places?limit=20&offset=0

    activate API
    API->>API: Parse query parameters<br/>(pagination, filters)

    API->>Service: get_places(filters, pagination)
    activate Service

    Service->>Facade: fetch_places(filters, pagination)
    activate Facade

    Facade->>Repo: get_all_places(filters, limit, offset)
    activate Repo

    Repo->>DB: SELECT * FROM places<br/>WHERE ... LIMIT ? OFFSET ?
    activate DB
    DB-->>Repo: List of place records
    deactivate DB

    Repo-->>Facade: List of Place instances
    deactivate Repo

    loop For each place
        Facade->>Repo: get_amenities_for_place(place_id)
        activate Repo
        Repo->>DB: SELECT amenities.* FROM amenities<br/>JOIN place_amenities...
        activate DB
        DB-->>Repo: Amenity records
        deactivate DB
        Repo-->>Facade: List of Amenity instances
        deactivate Repo

        Facade->>Repo: get_reviews_for_place(place_id)
        activate Repo
        Repo->>DB: SELECT * FROM reviews<br/>WHERE place_id=?
        activate DB
        DB-->>Repo: Review records
        deactivate DB
        Repo-->>Facade: List of Review instances
        deactivate Repo

        Facade->>Facade: Calculate average rating
    end

    Facade->>Repo: get_total_count(filters)
    activate Repo
    Repo->>DB: SELECT COUNT(*) FROM places WHERE...
    activate DB
    DB-->>Repo: Total count
    deactivate DB
    Repo-->>Facade: Total count
    deactivate Repo

    Facade-->>Service: Places list with metadata
    deactivate Facade

    Service->>Service: Format DTOs (exclude sensitive data)

    Service-->>API: Places DTOs + pagination metadata
    deactivate Service

    API-->>Client: 200 OK<br/>{places: [...], total: N, limit: 20, offset: 0}
    deactivate API
```

### Flow Description:
1. **Client** sends GET request with optional filters and pagination
2. **API** parses query parameters
3. **Service** requests places from Facade
4. **Repository** queries database with filters and pagination
5. **Facade** enriches each place with:
   - Associated amenities
   - Reviews
   - Average rating calculation
6. **Repository** also fetches total count for pagination
7. **Service** formats data transfer objects
8. **Client** receives 200 OK with paginated places list

---

## Common Patterns Across All Sequences

### 1. Layer Communication
All diagrams demonstrate the three-layer architecture:
- **Presentation** (API, Services): Input validation and response formatting
- **Business Logic** (Facade, Models): Business rules and entity management
- **Persistence** (Repository, Database): Data storage and retrieval

### 2. Facade Pattern
The Facade serves as the single entry point from Services to Business Logic, coordinating:
- Multiple model interactions
- Business rule validation
- Data integrity checks

### 3. Error Handling
Each sequence includes error scenarios:
- Authentication failures (401)
- Not Found errors (404)
- Conflict errors (409)
- Bad Request errors (400)

### 4. Validation Layers
Validation occurs at multiple levels:
- **API Layer**: Format and schema validation
- **Business Logic**: Business rules and constraints
- **Model Layer**: Entity-specific validation

### 5. Security Considerations
- Authentication middleware for protected endpoints
- Password hashing before storage
- Sensitive data filtering in responses

---

## Additional API Calls (Brief Overview)

### 5. Update User Profile: PUT /api/users/{user_id}
- Authenticates user
- Validates update data
- Checks user owns the profile (or is admin)
- Updates user model
- Persists changes

### 6. Delete Place: DELETE /api/places/{place_id}
- Authenticates user
- Verifies ownership
- Cascades deletion to reviews
- Removes amenity associations
- Deletes place

### 7. Get Place Details: GET /api/places/{place_id}
- Fetches place by ID
- Loads associated amenities
- Loads reviews with user information
- Calculates statistics (avg rating, review count)
- Returns enriched place object

### 8. List User's Places: GET /api/users/{user_id}/places
- Optionally authenticates (public profile)
- Fetches all places owned by user
- Includes basic amenity and review info
- Supports pagination

---

## Conclusion

These sequence diagrams provide a comprehensive view of the interaction flows in the HBnB Evolution application, demonstrating:

1. **Clear separation of concerns** across three layers
2. **Proper use of the Facade pattern** for coordinating business logic
3. **Robust error handling** at each layer
4. **Data validation** at multiple levels
5. **Security considerations** with authentication and authorization
6. **Efficient data retrieval** with proper database queries

These diagrams will serve as implementation guides for the development team, ensuring consistent architecture and interaction patterns throughout the application.
