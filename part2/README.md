# HBnB Part 2 - Business Logic and API Endpoints

## 📋 Description

Implémentation complète de la couche Business Logic et des endpoints API pour l'application HBnB (Holberton AirBnB clone). Ce projet utilise Flask et flask-restx pour créer une API RESTful complète avec pattern Facade et repository in-memory.

## ✅ Status: 100% CONFORME

Tous les tests passent, tous les endpoints fonctionnent correctement. Voir `RAPPORT_CONFORMITE_PART2.md` pour les détails complets.

## 🚀 Démarrage Rapide

### Windows
```batch
start_server.bat
```

### Linux/Mac
```bash
python run.py
```

### Accès
- **Documentation Swagger:** http://localhost:5000/api/v1/doc/
- **Base API:** http://localhost:5000/api/v1/

**IMPORTANT:** Cette API Part 2 ne nécessite **AUCUNE authentification JWT**. Si vous obtenez "Missing Authorization Header", vous avez démarré Part 3 par erreur. Voir `RESOLUTION_PROBLEME_JWT.md`.

## 📚 Documentation

- **`RAPPORT_CONFORMITE_PART2.md`** - Rapport complet de conformité (100%)
- **`GUIDE_UTILISATION_RAPIDE.md`** - Guide d'utilisation avec exemples
- **`RESOLUTION_PROBLEME_JWT.md`** - Résolution du problème JWT
- **`test_all_endpoints.sh`** - Script de test automatique
- **`test_review_crud.sh`** - Tests CRUD reviews

## 🏗️ Architecture

```
part2/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration
│   ├── models/                  # Business Logic Layer
│   │   ├── base_model.py        # Classe de base
│   │   ├── user.py              # Modèle User
│   │   ├── place.py             # Modèle Place
│   │   ├── review.py            # Modèle Review
│   │   └── amenity.py           # Modèle Amenity
│   ├── services/                # Services Layer (Facade)
│   │   ├── __init__.py          # Instance unique facade
│   │   └── facade.py            # Facade pattern
│   ├── persistence/             # Persistence Layer
│   │   ├── __init__.py
│   │   └── repository.py        # In-memory repository
│   └── api/
│       └── v1/                  # Presentation Layer (API v1)
│           ├── __init__.py      # Blueprint et namespaces
│           ├── users.py         # Endpoints User
│           ├── places.py        # Endpoints Place
│           ├── reviews.py       # Endpoints Review
│           └── amenities.py     # Endpoints Amenity
├── run.py                       # Point d'entrée
├── test_api.sh                  # Script de test Bash
├── test_api.py                  # Script de test Python
├── VERIFICATION_CONFORMITE.md   # Document de vérification
└── README.md                    # Ce fichier
```

## ✨ Fonctionnalités

### Modèles Implémentés

- **User** : Gestion des utilisateurs
  - Attributs : `first_name`, `last_name`, `email`, `is_admin`
  - Validations : longueur, format email

- **Place** : Gestion des lieux de location
  - Attributs : `title`, `description`, `price`, `latitude`, `longitude`, `owner`
  - Relations : amenities (many-to-many), reviews (one-to-many)
  - Validations : coordonnées GPS, prix positif

- **Review** : Gestion des avis
  - Attributs : `text`, `rating`, `place_id`, `user_id`
  - Validations : rating entre 1 et 5

- **Amenity** : Gestion des équipements
  - Attributs : `name`
  - Validations : longueur max 50 caractères

### API Endpoints

#### Users
- `POST /api/v1/users/` - Créer un utilisateur
- `GET /api/v1/users/` - Lister tous les utilisateurs
- `GET /api/v1/users/<user_id>` - Récupérer un utilisateur
- `PUT /api/v1/users/<user_id>` - Mettre à jour un utilisateur

#### Amenities
- `POST /api/v1/amenities/` - Créer un amenity
- `GET /api/v1/amenities/` - Lister tous les amenities
- `GET /api/v1/amenities/<amenity_id>` - Récupérer un amenity
- `PUT /api/v1/amenities/<amenity_id>` - Mettre à jour un amenity

#### Places
- `POST /api/v1/places/` - Créer un place
- `GET /api/v1/places/` - Lister tous les places
- `GET /api/v1/places/<place_id>` - Récupérer un place
- `PUT /api/v1/places/<place_id>` - Mettre à jour un place

#### Reviews
- `POST /api/v1/reviews/` - Créer un review
- `GET /api/v1/reviews/` - Lister tous les reviews
- `GET /api/v1/reviews/<review_id>` - Récupérer un review
- `PUT /api/v1/reviews/<review_id>` - Mettre à jour un review
- `DELETE /api/v1/reviews/<review_id>` - Supprimer un review
- `GET /api/v1/reviews/places/<place_id>` - Reviews par place
- `GET /api/v1/reviews/users/<user_id>` - Reviews par utilisateur

## 🚀 Installation

### Prérequis

```bash
Python 3.8+
pip
```

### Installation des dépendances

```bash
cd part2
pip install -r requirements.txt
```

Si le fichier `requirements.txt` n'existe pas, créez-le avec :

```txt
Flask==2.3.0
flask-restx==1.1.0
colorama==0.4.6
requests==2.31.0
```

## 💻 Utilisation

### Lancer l'application

```bash
cd part2
python run.py
```

L'API sera accessible sur `http://localhost:5000`

### Documentation Swagger

Une fois l'application lancée, accédez à la documentation interactive :

```
http://localhost:5000/api/v1/
```

## 🧪 Tests

### Option 1 : Script Bash

```bash
cd part2
./test_api.sh
```

### Option 2 : Script Python (recommandé)

```bash
cd part2
python test_api.py
```

Le script Python offre :
- Tests colorés et formatés
- Validation automatique
- Rapport détaillé
- Tests de validation (email unique, rating, etc.)

### Option 3 : Tests manuels avec cURL

#### Créer un utilisateur
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}'
```

#### Créer un amenity
```bash
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

#### Lister tous les utilisateurs
```bash
curl -X GET http://localhost:5000/api/v1/users/
```

## 📊 Exemples de Réponses

### POST /api/v1/users/
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "is_admin": false,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### PUT /api/v1/amenities/<amenity_id>
```json
{
  "message": "Amenity updated successfully"
}
```

### GET /api/v1/places/<place_id>
```json
{
  "id": "...",
  "title": "Cozy Apartment",
  "description": "A nice place",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner": {
    "id": "...",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
  },
  "amenities": [
    {"id": "...", "name": "Wi-Fi"},
    {"id": "...", "name": "Air Conditioning"}
  ],
  "reviews": [
    {
      "id": "...",
      "text": "Great place!",
      "rating": 5,
      "user_id": "..."
    }
  ]
}
```

## 🔍 Validations Implémentées

### User
- ✅ `first_name` : max 50 caractères, requis
- ✅ `last_name` : max 50 caractères, requis
- ✅ `email` : format valide, unique, requis

### Place
- ✅ `title` : max 100 caractères, requis
- ✅ `price` : doit être positif
- ✅ `latitude` : entre -90.0 et 90.0
- ✅ `longitude` : entre -180.0 et 180.0
- ✅ `owner` : doit exister

### Review
- ✅ `text` : requis, non vide
- ✅ `rating` : entier entre 1 et 5
- ✅ `place_id` et `user_id` : doivent exister

### Amenity
- ✅ `name` : max 50 caractères, requis

## 🎯 Status Codes

| Code | Signification | Utilisation |
|------|---------------|-------------|
| 200 | OK | Récupération/mise à jour réussie |
| 201 | Created | Création réussie |
| 204 | No Content | Suppression réussie |
| 400 | Bad Request | Données invalides |
| 404 | Not Found | Ressource non trouvée |

## 📝 Patterns Utilisés

### Facade Pattern
Simplifie l'accès à la Business Logic depuis l'API :

```python
from app.services import facade

# Dans les endpoints API
user = facade.create_user(user_data)
place = facade.get_place(place_id)
```

### Repository Pattern
Abstraction de la persistence (in-memory pour Part 2) :

```python
class InMemoryRepository:
    def add(self, obj)
    def get(self, obj_id)
    def get_all()
    def update(obj_id, data)
    def delete(obj_id)
    def get_by_attribute(attr_name, attr_value)
```

## 🔧 Développement

### Structure des couches

1. **Presentation Layer** (`api/v1/`)
   - Définition des endpoints REST
   - Validation des entrées avec flask-restx
   - Sérialisation des réponses

2. **Business Logic Layer** (`models/`)
   - Logique métier
   - Validations
   - Relations entre entités

3. **Services Layer** (`services/`)
   - Facade pattern
   - Coordination entre couches

4. **Persistence Layer** (`persistence/`)
   - Repository pattern
   - In-memory storage (Part 2)
   - Sera remplacé par SQL Alchemy (Part 3)

## 📚 Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/)
- [REST API Best Practices](https://restfulapi.net/)
- [Facade Pattern](https://refactoring.guru/design-patterns/facade)

## 👥 Auteurs

**Team Allan Bony Rattler**
- Projet Holberton School
- HBnB v2 - Part 2

## 📄 Licence

Ce projet fait partie du curriculum Holberton School.

## 🔜 Prochaines Étapes (Part 3)

- Authentification JWT
- Contrôle d'accès basé sur les rôles (RBAC)
- Persistence avec SQL Alchemy
- Base de données PostgreSQL/MySQL
