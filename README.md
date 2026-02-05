# HBnB - Holberton AirBnB Clone

A full-stack web application for managing rental properties, inspired by Airbnb. Built with Flask (Python) backend and HTML/CSS/JavaScript frontend.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Database Design](#database-design)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)

## Features

- **User Management**: Registration, authentication with JWT tokens
- **Place Listings**: Create, view, and manage rental properties
- **Reviews**: Leave ratings and reviews for places
- **Amenities**: Manage property amenities (WiFi, Pool, Parking, etc.)
- **Search & Filter**: Filter places by price
- **Role-Based Access**: Admin and regular user permissions

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (HTML/CSS/JS)                   │
│                    - Login Page                             │
│                    - Places Listing                         │
│                    - Place Details                          │
│                    - Add Review                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask REST API                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ /api/v1/auth│  │/api/v1/users│  │ /api/v1/places      │ │
│  │ /api/v1/    │  │/api/v1/     │  │ /api/v1/reviews     │ │
│  │  amenities  │  │             │  │                     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer (Facade)                   │
│              Business logic and validation                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLAlchemy ORM                           │
│         User | Place | Review | Amenity Models              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database                                 │
│            SQLite (dev) / PostgreSQL (prod)                 │
└─────────────────────────────────────────────────────────────┘
```

## Database Design

### Entity-Relationship Diagram

```
┌───────────────────┐          ┌───────────────────┐
│       USER        │          │      AMENITY      │
├───────────────────┤          ├───────────────────┤
│ PK  id (UUID)     │          │ PK  id (UUID)     │
│     first_name    │          │     name          │
│     last_name     │          └─────────┬─────────┘
│     email (UNIQUE)│                    │
│     password_hash │                    │ M:N
│     is_admin      │                    │
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
└───────────────────┘
```

### Relationships

| Relationship | Type | Description |
|--------------|------|-------------|
| User → Place | One-to-Many | User owns multiple places |
| User → Review | One-to-Many | User writes multiple reviews |
| Place → Review | One-to-Many | Place has multiple reviews |
| Place ↔ Amenity | Many-to-Many | Via place_amenity table |

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.8+, Flask 2.3+ |
| API | Flask-RESTx |
| Database ORM | SQLAlchemy |
| Authentication | JWT (Flask-JWT-Extended) |
| Password Hashing | Bcrypt |
| Database | SQLite (dev), PostgreSQL (prod) |
| Frontend | HTML5, CSS3, JavaScript |
| API Docs | Swagger/OpenAPI |

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/holbertonschool-hbnb.git
   cd holbertonschool-hbnb
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   cd part3
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the API**
   - API: http://localhost:5001/api/v1/
   - Swagger Docs: http://localhost:5001/api/v1/doc/

6. **Access the Frontend**
   - Open `part4/index.html` in a browser
   - Or serve with: `python -m http.server 8000` in part4 folder

## API Documentation

### Authentication

```bash
# Login
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Main Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /api/v1/auth/login | User login | No |
| GET | /api/v1/users | List users | No |
| POST | /api/v1/users | Create user | Admin |
| GET | /api/v1/places | List places | No |
| POST | /api/v1/places | Create place | Yes |
| GET | /api/v1/places/{id} | Get place details | No |
| PUT | /api/v1/places/{id} | Update place | Owner |
| GET | /api/v1/reviews | List reviews | No |
| POST | /api/v1/reviews | Create review | Yes |
| GET | /api/v1/amenities | List amenities | No |
| POST | /api/v1/amenities | Create amenity | Admin |

## Testing

### Run Tests

```bash
cd part3
pytest tests/ -v
```

### API Testing with Postman

1. Import the Postman collection from `docs/`
2. Set environment variable `base_url` to `http://localhost:5001`
3. Run the test collection

### Manual Testing

```bash
# Test login
curl -X POST http://localhost:5001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.io", "password": "admin1234"}'

# Test get places
curl http://localhost:5001/api/v1/places
```

## Project Structure

```
holbertonschool-hbnb/
├── part2/                    # In-memory implementation
│   ├── app/
│   │   ├── models/          # Business models
│   │   ├── api/v1/          # API endpoints
│   │   ├── services/        # Facade pattern
│   │   └── persistence/     # In-memory storage
│   └── run.py
│
├── part3/                    # Database implementation
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   │   ├── baseclass.py
│   │   │   ├── user.py
│   │   │   ├── place.py
│   │   │   ├── review.py
│   │   │   └── amenity.py
│   │   ├── api/
│   │   │   ├── auth.py      # Authentication
│   │   │   └── v1/          # API v1 endpoints
│   │   └── services/
│   │       └── facade.py    # Business logic
│   ├── config.py            # Configuration
│   ├── requirements.txt
│   └── run.py               # Entry point
│
├── part4/                    # Frontend
│   ├── index.html           # Main page
│   ├── login.html           # Login page
│   ├── place.html           # Place details
│   ├── add_review.html      # Review form
│   ├── scripts.js           # JavaScript logic
│   └── styles.css           # Styling
│
└── docs/                     # Documentation
    ├── stage2-planning/
    ├── stage3-technical/
    └── stage4-development/
```

## Authors

- Holberton School Students

## License

This project is part of the Holberton School curriculum.
