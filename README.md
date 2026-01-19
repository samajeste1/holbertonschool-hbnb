# HBnB - AirBnB Clone

Projet complet de clone d'AirBnB développé en équipe, comprenant le backend (API, Business Logic, Database) et le frontend (Web Client).

## Équipe

- Allan
- Bony
- Rattler

## Structure du projet

Le projet est divisé en 4 parties principales :

### Part 1: Technical Documentation
Documentation technique complète de l'architecture et du design de l'application.

**Dossier:** `part1/`

**Contenu:**
- Diagramme de packages (architecture 3 couches)
- Diagramme de classes détaillé (Business Logic)
- Diagrammes de séquence (4 flux API)
- Documentation UML complète avec Mermaid.js
- Principes SOLID appliqués
- Règles métier et validation

**Fichiers clés:**
- [README.md](part1/README.md) - Vue d'ensemble complète
- [QUICK_START.md](part1/QUICK_START.md) - Guide de navigation
- [task_00_package_diagram.md](part1/task_00_package_diagram.md) - Architecture
- [task_01_class_diagram.md](part1/task_01_class_diagram.md) - Modèles
- [task_02_sequence_diagrams.md](part1/task_02_sequence_diagrams.md) - Flux API

### Part 2: Business Logic and API
Implémentation de la couche Business Logic et des endpoints API RESTful avec Flask et flask-restx.

**Dossier:** `part2/`

**Fonctionnalités:**
- Architecture modulaire (Presentation, Business Logic, Persistence)
- Pattern Facade pour la communication entre couches
- Repository en mémoire pour la persistance
- Endpoints CRUD pour User, Place, Review, Amenity
- Documentation Swagger automatique

### Part 3: Authentication and Database Integration
Extension du backend avec authentification JWT, contrôle d'accès basé sur les rôles, et intégration de base de données.

**Dossier:** `part3/`

**Fonctionnalités:**
- Authentification JWT avec Flask-JWT-Extended
- Contrôle d'accès basé sur les rôles (RBAC)
- Hachage de mots de passe avec bcrypt
- Intégration SQLAlchemy (SQLite pour dev, MySQL pour prod)
- Mapping des entités et relations
- Scripts SQL pour la génération de schéma
- Diagrammes ER avec Mermaid.js

### Part 4: Simple Web Client
Client web frontend interactif utilisant HTML5, CSS3 et JavaScript ES6.

**Dossier:** `part4/`

**Fonctionnalités:**
- Interface utilisateur responsive
- Authentification côté client
- Gestion de sessions avec cookies JWT
- Liste des places avec filtrage
- Détails des places
- Ajout de reviews
- Communication avec l'API via Fetch API

## Technologies utilisées

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **Flask-RESTx** - Extension pour APIs RESTful
- **Flask-JWT-Extended** - Authentification JWT
- **Flask-Bcrypt** - Hachage de mots de passe
- **SQLAlchemy** - ORM pour base de données
- **SQLite** - Base de données de développement
- **MySQL** - Base de données de production

### Frontend
- **HTML5** - Structure
- **CSS3** - Styles
- **JavaScript ES6** - Logique client
- **Fetch API** - Requêtes HTTP

## Installation

### Part 2 (Backend - API)
```bash
cd part2
pip install -r requirements.txt
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

### Part 3 (Backend - Auth & DB)
```bash
cd part3
pip install -r requirements.txt
export FLASK_APP=app
export FLASK_ENV=development
export JWT_SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///hbnb.db
python scripts/init_db.py
flask run
```

### Part 4 (Frontend)
```bash
cd part4
# Ouvrir index.html dans un navigateur
# Ou utiliser un serveur local :
python -m http.server 8000
```

## Architecture

### Backend (Part 2 & 3)

```
Presentation Layer (API)
    ↓
Business Logic Layer (Models)
    ↓
Facade Pattern
    ↓
Persistence Layer (Repository)
    ↓
Database (SQLite/MySQL)
```

### Frontend (Part 4)

```
HTML Pages
    ↓
JavaScript (ES6)
    ↓
Fetch API
    ↓
Backend API
```

## Endpoints API

### Authentication
- `POST /api/v1/auth/login` - Connexion utilisateur

### Users
- `POST /api/v1/users/` - Créer un utilisateur
- `GET /api/v1/users/` - Lister les utilisateurs
- `GET /api/v1/users/<id>` - Obtenir un utilisateur
- `PUT /api/v1/users/<id>` - Mettre à jour un utilisateur

### Places
- `POST /api/v1/places/` - Créer un place (authentifié)
- `GET /api/v1/places/` - Lister les places
- `GET /api/v1/places/<id>` - Obtenir un place
- `PUT /api/v1/places/<id>` - Mettre à jour un place (propriétaire/admin)

### Reviews
- `POST /api/v1/reviews/` - Créer un review (authentifié)
- `GET /api/v1/reviews/` - Lister les reviews
- `GET /api/v1/reviews/<id>` - Obtenir un review
- `PUT /api/v1/reviews/<id>` - Mettre à jour un review (auteur/admin)
- `DELETE /api/v1/reviews/<id>` - Supprimer un review (auteur/admin)

### Amenities
- `POST /api/v1/amenities/` - Créer une amenity (admin)
- `GET /api/v1/amenities/` - Lister les amenities
- `GET /api/v1/amenities/<id>` - Obtenir une amenity
- `PUT /api/v1/amenities/<id>` - Mettre à jour une amenity (admin)

## Sécurité

- **JWT Authentication** - Tokens pour l'authentification
- **Password Hashing** - Bcrypt pour le hachage des mots de passe
- **Role-Based Access Control** - Contrôle d'accès basé sur les rôles
- **Ownership Validation** - Validation de la propriété des ressources
- **CORS Configuration** - Configuration CORS pour le frontend

## Base de données

### Entités principales
- **User** - Utilisateurs (avec is_admin pour les administrateurs)
- **Place** - Places à louer
- **Review** - Avis des utilisateurs
- **Amenity** - Commodités/équipements

### Relations
- User → Place (one-to-many) - Un utilisateur peut posséder plusieurs places
- Place → Review (one-to-many) - Un place peut avoir plusieurs reviews
- User → Review (one-to-many) - Un utilisateur peut écrire plusieurs reviews
- Place ↔ Amenity (many-to-many) - Un place peut avoir plusieurs amenities

## Documentation

Chaque partie contient son propre README avec des instructions détaillées :
- [Part 1 README](part1/README.md) - Documentation technique UML
- [Part 2 README](part2/README.md) - Business Logic et API
- [Part 3 README](part3/README.md) - Authentication et Database
- [Part 4 README](part4/README.md) - Web Client

## Tests

### Backend
```bash
# Tests unitaires
python -m pytest tests/

# Tests avec cURL
curl -X GET http://localhost:5000/api/v1/places/
```

### Frontend
- Ouvrir les pages HTML dans un navigateur
- Tester l'authentification
- Vérifier les interactions avec l'API

## Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Mermaid.js](https://mermaid.js.org/)
- [MDN Web Docs](https://developer.mozilla.org/)

## Auteur

Holberton School - Team: Allan, Bony, Rattler



