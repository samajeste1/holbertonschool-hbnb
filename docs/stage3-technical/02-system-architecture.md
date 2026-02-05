# HBnB - System Architecture (Stage 3)

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     Web Browser (Frontend)                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │   │
│  │  │  HTML5   │  │  CSS3    │  │JavaScript│  │  Fetch API       │ │   │
│  │  │  Pages   │  │  Styles  │  │  Logic   │  │  (HTTP Requests) │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/HTTPS (REST API)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              API LAYER                                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Flask REST API (Flask-RESTx)                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │   │
│  │  │ /api/v1/auth │  │/api/v1/users │  │  /api/v1/places      │  │   │
│  │  │   - login    │  │   - CRUD     │  │    - CRUD            │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │   │
│  │  │/api/v1/reviews│ │/api/v1/      │  │  JWT Middleware      │  │   │
│  │  │   - CRUD     │  │  amenities   │  │  (Authentication)    │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           SERVICE LAYER                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    HBnBFacade (Facade Pattern)                   │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │   │
│  │  │ User Service │  │Place Service │  │  Review Service      │  │   │
│  │  │  - create    │  │  - create    │  │    - create          │  │   │
│  │  │  - get       │  │  - get       │  │    - get             │  │   │
│  │  │  - update    │  │  - update    │  │    - update          │  │   │
│  │  │  - auth      │  │  - list      │  │    - delete          │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘  │   │
│  │  ┌──────────────┐                                               │   │
│  │  │Amenity Svc   │                                               │   │
│  │  │  - CRUD      │                                               │   │
│  │  └──────────────┘                                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           MODEL LAYER                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                  SQLAlchemy ORM Models                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │   │
│  │  │   User   │  │  Place   │  │  Review  │  │    Amenity       │ │   │
│  │  │  Model   │  │  Model   │  │  Model   │  │    Model         │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │   │
│  │                     │                                            │   │
│  │              ┌──────────────┐                                    │   │
│  │              │  BaseClass   │                                    │   │
│  │              │  (id, dates) │                                    │   │
│  │              └──────────────┘                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        PERSISTENCE LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     SQLAlchemy + Database                        │   │
│  │  ┌──────────────────────────────────────────────────────────┐   │   │
│  │  │                    SQLite (Development)                   │   │   │
│  │  │                    PostgreSQL (Production)                │   │   │
│  │  └──────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | User interface |
| **API Framework** | Flask + Flask-RESTx | REST API endpoints |
| **Authentication** | Flask-JWT-Extended | JWT token management |
| **Password Hashing** | Bcrypt | Secure password storage |
| **ORM** | SQLAlchemy | Database abstraction |
| **Database** | SQLite / PostgreSQL | Data persistence |
| **Documentation** | Swagger/OpenAPI | API documentation |

## Data Flow

```
User Action → Frontend (JS) → HTTP Request → Flask API → Service Layer → Model → Database
                                                  ↑
                                            JWT Validation
```

### Authentication Flow

```
1. Login Request
   Client ──POST /api/v1/auth/login──▶ API
                                        │
                                        ▼
                               Verify credentials
                                        │
                                        ▼
                               Generate JWT token
                                        │
                                        ▼
   Client ◀──────JWT Token─────────────┘

2. Protected Request
   Client ──GET /api/v1/places (+ JWT)──▶ API
                                           │
                                           ▼
                                    Validate JWT
                                           │
                                           ▼
                                    Process request
                                           │
                                           ▼
   Client ◀──────Response─────────────────┘
```

## Design Patterns Used

| Pattern | Implementation | Purpose |
|---------|---------------|---------|
| **Facade** | HBnBFacade class | Single interface to complex subsystems |
| **Repository** | SQLAlchemy models | Data access abstraction |
| **Factory** | create_app() | Application instance creation |
| **Singleton** | Facade instance | Shared service instance |

## Technical Justifications

### Why Flask?
- Lightweight and flexible
- Easy to learn and implement
- Large ecosystem of extensions
- Suitable for REST API development

### Why SQLAlchemy?
- Powerful ORM with database abstraction
- Support for multiple database backends
- Easy migration between SQLite (dev) and PostgreSQL (prod)

### Why JWT?
- Stateless authentication
- Scalable (no server-side sessions)
- Industry standard for REST APIs
- Easy to implement with Flask-JWT-Extended

### Why Bcrypt?
- Industry standard for password hashing
- Built-in salting
- Resistant to rainbow table attacks
- Configurable work factor
