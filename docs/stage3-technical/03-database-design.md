# HBnB - Database Design (Stage 3)

## Entity-Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATABASE SCHEMA                                    │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌───────────────────┐          ┌───────────────────┐
    │       USER        │          │      AMENITY      │
    ├───────────────────┤          ├───────────────────┤
    │ PK  id (UUID)     │          │ PK  id (UUID)     │
    │     first_name    │          │     name          │
    │     last_name     │          │     created_at    │
    │     email (UNIQUE)│          │     updated_at    │
    │     password_hash │          └─────────┬─────────┘
    │     is_admin      │                    │
    │     created_at    │                    │ M:N
    │     updated_at    │                    │
    └─────────┬─────────┘          ┌─────────▼─────────┐
              │                    │  PLACE_AMENITY    │
              │ 1:N               ├───────────────────┤
              │                    │ FK  place_id      │
    ┌─────────▼─────────┐          │ FK  amenity_id    │
    │       PLACE       │◀─────────┴───────────────────┘
    ├───────────────────┤
    │ PK  id (UUID)     │
    │ FK  owner_id      │──────────▶ USER
    │     title         │
    │     description   │
    │     price         │
    │     latitude      │
    │     longitude     │
    │     created_at    │
    │     updated_at    │
    └─────────┬─────────┘
              │
              │ 1:N
              │
    ┌─────────▼─────────┐
    │      REVIEW       │
    ├───────────────────┤
    │ PK  id (UUID)     │
    │ FK  place_id      │──────────▶ PLACE
    │ FK  user_id       │──────────▶ USER
    │     text          │
    │     rating (1-5)  │
    │     created_at    │
    │     updated_at    │
    └───────────────────┘
```

## Database Schema

### Table: users

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| first_name | VARCHAR(50) | NOT NULL | User's first name |
| last_name | VARCHAR(50) | NOT NULL | User's last name |
| email | VARCHAR(120) | UNIQUE, NOT NULL | User's email address |
| password_hash | VARCHAR(128) | NOT NULL | Bcrypt hashed password |
| is_admin | BOOLEAN | DEFAULT FALSE | Admin privileges flag |
| created_at | DATETIME | NOT NULL | Creation timestamp |
| updated_at | DATETIME | NOT NULL | Last update timestamp |

### Table: places

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| title | VARCHAR(100) | NOT NULL | Place title |
| description | TEXT | | Place description |
| price | FLOAT | NOT NULL, CHECK > 0 | Price per night |
| latitude | FLOAT | NOT NULL, CHECK -90 to 90 | GPS latitude |
| longitude | FLOAT | NOT NULL, CHECK -180 to 180 | GPS longitude |
| owner_id | UUID | FOREIGN KEY (users.id) | Owner reference |
| created_at | DATETIME | NOT NULL | Creation timestamp |
| updated_at | DATETIME | NOT NULL | Last update timestamp |

### Table: reviews

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| text | TEXT | NOT NULL | Review content |
| rating | INTEGER | NOT NULL, CHECK 1-5 | Star rating |
| place_id | UUID | FOREIGN KEY (places.id) | Place reference |
| user_id | UUID | FOREIGN KEY (users.id) | Author reference |
| created_at | DATETIME | NOT NULL | Creation timestamp |
| updated_at | DATETIME | NOT NULL | Last update timestamp |

### Table: amenities

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Amenity name |
| created_at | DATETIME | NOT NULL | Creation timestamp |
| updated_at | DATETIME | NOT NULL | Last update timestamp |

### Table: place_amenity (Association Table)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| place_id | UUID | FOREIGN KEY (places.id), PRIMARY KEY | Place reference |
| amenity_id | UUID | FOREIGN KEY (amenities.id), PRIMARY KEY | Amenity reference |

## Relationships

| Relationship | Type | Description |
|--------------|------|-------------|
| User → Place | One-to-Many | A user can own multiple places |
| User → Review | One-to-Many | A user can write multiple reviews |
| Place → Review | One-to-Many | A place can have multiple reviews |
| Place ↔ Amenity | Many-to-Many | Places can have multiple amenities, amenities can belong to multiple places |

## SQL Schema Definition

```sql
-- Users table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Places table
CREATE TABLE places (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL CHECK (price > 0),
    latitude FLOAT NOT NULL CHECK (latitude >= -90 AND latitude <= 90),
    longitude FLOAT NOT NULL CHECK (longitude >= -180 AND longitude <= 180),
    owner_id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Reviews table
CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    place_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Amenities table
CREATE TABLE amenities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Place-Amenity association table
CREATE TABLE place_amenity (
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);
```

## Technical Justifications

### Why UUID for Primary Keys?
- Globally unique identifiers
- No sequential guessing of IDs (security)
- Allows distributed ID generation

### Why Separate Association Table for Place-Amenity?
- Proper normalization (3NF)
- Efficient many-to-many relationship
- Easy to query amenities per place and vice versa

### Why Bcrypt Hash Storage?
- Industry standard security practice
- Salted hashes prevent rainbow table attacks
- Configurable cost factor for future-proofing
