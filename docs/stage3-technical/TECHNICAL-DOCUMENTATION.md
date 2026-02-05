# HBnB - Technical Documentation (Stage 3)

## Table of Contents

1. [User Stories and Mockups](#1-user-stories-and-mockups)
2. [System Architecture](#2-system-architecture)
3. [Database Design](#3-database-design)
4. [Sequence Diagrams](#4-sequence-diagrams)
5. [API Specifications](#5-api-specifications)
6. [SCM and QA Plans](#6-scm-and-qa-plans)
7. [Technical Justifications](#7-technical-justifications)

---

## 1. User Stories and Mockups

See: [01-user-stories.md](./01-user-stories.md)

### Summary of Prioritized User Stories

| Priority | ID | User Story |
|----------|-----|-----------|
| **Must Have** | US-01 | User registration |
| **Must Have** | US-02 | User login with JWT |
| **Must Have** | US-03 | View all places |
| **Must Have** | US-04 | View place details |
| **Must Have** | US-05 | Create place listing |
| **Must Have** | US-06 | Leave review |
| **Must Have** | US-07 | Admin user management |
| **Should Have** | US-08 | Update place listing |
| **Should Have** | US-09 | Filter places by price |
| **Should Have** | US-10 | View place amenities |

### Mockups

The frontend consists of 4 main pages:
- **Login Page** (`login.html`) - User authentication
- **Places Listing** (`index.html`) - Browse all places with price filter
- **Place Details** (`place.html`) - Full place information with reviews
- **Add Review** (`add_review.html`) - Submit review form

---

## 2. System Architecture

See: [02-system-architecture.md](./02-system-architecture.md)

### High-Level Architecture

```
Frontend (HTML/CSS/JS) → REST API (Flask) → Service Layer → ORM → Database
```

### Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, JavaScript |
| API | Flask + Flask-RESTx |
| Authentication | JWT (Flask-JWT-Extended) |
| ORM | SQLAlchemy |
| Database | SQLite / PostgreSQL |

---

## 3. Database Design

See: [03-database-design.md](./03-database-design.md)

### Tables

| Table | Description |
|-------|-------------|
| users | User accounts with authentication |
| places | Rental property listings |
| reviews | User reviews for places |
| amenities | Available amenities |
| place_amenity | Place-amenity relationships |

### Key Relationships

- User owns multiple Places (1:N)
- Place has multiple Reviews (1:N)
- Place has multiple Amenities (M:N)

---

## 4. Sequence Diagrams

See: [04-sequence-diagrams.md](./04-sequence-diagrams.md)

### Key Interactions Documented

1. **User Login** - Authentication flow with JWT generation
2. **Create Place** - Authenticated place creation
3. **Get Place Details** - Fetching place with reviews and amenities
4. **Create Review** - Authenticated review submission

---

## 5. API Specifications

See: [05-api-specifications.md](./05-api-specifications.md)

### Endpoint Summary

| Resource | Endpoints |
|----------|-----------|
| Authentication | POST /auth/login |
| Users | GET, POST /users, GET, PUT /users/{id} |
| Places | GET, POST /places, GET, PUT /places/{id} |
| Reviews | GET, POST, PUT, DELETE /reviews |
| Amenities | GET, POST /amenities |

### Authentication

All protected endpoints require:
```
Authorization: Bearer <JWT_TOKEN>
```

---

## 6. SCM and QA Plans

See: [06-scm-qa-plans.md](./06-scm-qa-plans.md)

### SCM Strategy

- **Tool**: Git + GitHub
- **Branching**: main → develop → feature/*
- **Code Reviews**: Required before merge

### QA Strategy

- **Unit Tests**: pytest
- **API Tests**: Postman
- **E2E Tests**: Manual browser testing

---

## 7. Technical Justifications

### Why Flask?
- Lightweight and flexible for REST APIs
- Large ecosystem of extensions
- Easy learning curve
- Suitable for MVP development

### Why SQLAlchemy?
- Powerful ORM with database abstraction
- Supports multiple database backends
- Easy switch from SQLite (dev) to PostgreSQL (prod)

### Why JWT Authentication?
- Stateless authentication (scalable)
- Industry standard for REST APIs
- No server-side session storage needed

### Why Bcrypt for Passwords?
- Industry standard hashing algorithm
- Built-in salting
- Resistant to rainbow table attacks

### Why Layered Architecture?
- Separation of concerns
- Easy testing and maintenance
- Scalable and extensible

### Why Facade Pattern?
- Single entry point for business logic
- Simplifies API layer code
- Encapsulates complex operations

---

## Document Index

| Document | Description |
|----------|-------------|
| [01-user-stories.md](./01-user-stories.md) | User stories with MoSCoW prioritization |
| [02-system-architecture.md](./02-system-architecture.md) | Architecture diagram and tech stack |
| [03-database-design.md](./03-database-design.md) | ERD and database schema |
| [04-sequence-diagrams.md](./04-sequence-diagrams.md) | Interaction diagrams |
| [05-api-specifications.md](./05-api-specifications.md) | API endpoint documentation |
| [06-scm-qa-plans.md](./06-scm-qa-plans.md) | Source control and testing plans |
