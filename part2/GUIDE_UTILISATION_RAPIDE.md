# 🚀 Guide d'Utilisation Rapide - HBnB Part 2

## ⚡ Démarrage Rapide

### 1️⃣ Démarrer le serveur

**Windows:**
```batch
cd holbertonschool-hbnb\part2
start_server.bat
```

**Linux/Mac:**
```bash
cd holbertonschool-hbnb/part2
python run.py
```

### 2️⃣ Accéder à l'API

- **Documentation Swagger:** http://localhost:5000/api/v1/doc/
- **Base API:** http://localhost:5000/api/v1/

---

## 📖 Tests Rapides (Sans JWT!)

### ✅ Test 1: Créer un utilisateur

```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Allan",
    "last_name": "Bony",
    "email": "allan@example.com"
  }'
```

**Réponse attendue (201):**
```json
{
  "id": "uuid-here",
  "first_name": "Allan",
  "last_name": "Bony",
  "email": "allan@example.com",
  "is_admin": false,
  "created_at": "...",
  "updated_at": "..."
}
```

### ✅ Test 2: Lister les utilisateurs

```bash
curl http://localhost:5000/api/v1/users/
```

### ✅ Test 3: Créer une amenity

```bash
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

### ✅ Test 4: Créer un place avec relations

```bash
# Remplacez <USER_ID> et <AMENITY_ID> par vos IDs
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cozy Apartment",
    "description": "Nice place",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "<USER_ID>",
    "amenities": ["<AMENITY_ID>"]
  }'
```

### ✅ Test 5: Voir place avec owner et amenities

```bash
# Remplacez <PLACE_ID>
curl http://localhost:5000/api/v1/places/<PLACE_ID>
```

**Réponse inclut:**
- ✅ Détails du owner (first_name, last_name, email)
- ✅ Liste complète des amenities

### ✅ Test 6: Créer une review

```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place!",
    "rating": 5,
    "user_id": "<USER_ID>",
    "place_id": "<PLACE_ID>"
  }'
```

### ✅ Test 7: Supprimer une review (SEUL DELETE)

```bash
curl -X DELETE http://localhost:5000/api/v1/reviews/<REVIEW_ID>
```

---

## 🎯 Endpoints Disponibles

### Users
- `POST   /api/v1/users/` - Créer
- `GET    /api/v1/users/` - Lister tous
- `GET    /api/v1/users/<id>` - Détails
- `PUT    /api/v1/users/<id>` - Modifier

### Amenities
- `POST   /api/v1/amenities/` - Créer
- `GET    /api/v1/amenities/` - Lister tous
- `GET    /api/v1/amenities/<id>` - Détails
- `PUT    /api/v1/amenities/<id>` - Modifier

### Places
- `POST   /api/v1/places/` - Créer
- `GET    /api/v1/places/` - Lister tous
- `GET    /api/v1/places/<id>` - Détails + owner + amenities
- `PUT    /api/v1/places/<id>` - Modifier
- `GET    /api/v1/places/<id>/reviews` - Reviews du place

### Reviews
- `POST   /api/v1/reviews/` - Créer
- `GET    /api/v1/reviews/` - Lister tous
- `GET    /api/v1/reviews/<id>` - Détails
- `PUT    /api/v1/reviews/<id>` - Modifier
- `DELETE /api/v1/reviews/<id>` - **Supprimer** ⚠️ Seul DELETE

---

## 🧪 Script de Test Complet

```bash
# Exécuter tous les tests d'un coup
bash test_all_endpoints.sh
```

Ce script teste:
- ✅ Création de 2 users
- ✅ Création de 2 amenities
- ✅ Création d'un place avec relations
- ✅ Création, modification et suppression de review
- ✅ Tous les endpoints GET

---

## 🔍 Vérifications Importantes

### ❌ Si vous voyez "Missing Authorization Header"

**Problème:** Vous avez démarré Part 3 au lieu de Part 2!

**Solution:**
```bash
# Arrêter tous les serveurs
taskkill //F //IM python3.11.exe  # Windows
pkill -f python                    # Linux/Mac

# Redémarrer Part 2
cd holbertonschool-hbnb/part2
python run.py
```

### ✅ Comment savoir si c'est le bon serveur?

**Vérifiez Swagger:** http://localhost:5000/api/v1/doc/

**Modèle User Part 2 (correct):**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "is_admin": false
}
```

**Modèle User Part 3 (mauvais serveur!):**
```json
{
  "first_name": "string",
  "password": "string",      ← NE DOIT PAS ÊTRE LÀ
  "place_list": ["string"]   ← NE DOIT PAS ÊTRE LÀ
}
```

---

## 📊 Validations Automatiques

Ces validations sont appliquées automatiquement:

### User
- ✅ Email format valide
- ✅ Email unique
- ✅ first_name/last_name max 50 chars

### Place
- ✅ Price > 0
- ✅ Latitude: -90.0 à 90.0
- ✅ Longitude: -180.0 à 180.0
- ✅ owner_id doit exister

### Review
- ✅ Rating: 1 à 5
- ✅ user_id doit exister
- ✅ place_id doit exister

---

## 🎨 Exemples d'Erreurs

### Email déjà utilisé
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -d '{"first_name":"Test", "last_name":"User", "email":"allan@example.com"}'
```
**Réponse (400):**
```json
{"error": "Email already registered"}
```

### Latitude invalide
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -d '{"latitude": 100.0, ...}'  # > 90
```
**Réponse (400):**
```json
{"error": "Latitude must be between -90.0 and 90.0"}
```

### Rating invalide
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -d '{"rating": 6, ...}'  # > 5
```
**Réponse (400):**
```json
{"error": "Rating must be an integer between 1 and 5"}
```

---

## 📁 Fichiers Utiles

- `RAPPORT_CONFORMITE_PART2.md` - Rapport complet de conformité
- `RESOLUTION_PROBLEME_JWT.md` - Guide résolution problème JWT
- `test_all_endpoints.sh` - Script de test complet
- `test_review_crud.sh` - Test CRUD reviews
- `start_server.bat` - Démarrage automatique (Windows)

---

## 💡 Astuces

### Formater les réponses JSON

```bash
# Ajouter | python -m json.tool
curl http://localhost:5000/api/v1/users/ | python -m json.tool
```

### Voir le code HTTP

```bash
# Ajouter -w "\nHTTP: %{http_code}\n"
curl -w "\nHTTP: %{http_code}\n" http://localhost:5000/api/v1/users/
```

### Mode verbose (debug)

```bash
curl -v http://localhost:5000/api/v1/users/
```

---

## 🎯 Checklist Avant Review

- [ ] Serveur Part 2 démarre sans erreur
- [ ] Swagger accessible à `/api/v1/doc/`
- [ ] Aucun JWT requis
- [ ] Création User fonctionne
- [ ] Création Place avec relations fonctionne
- [ ] GET Place retourne owner et amenities
- [ ] Review DELETE fonctionne
- [ ] Script `test_all_endpoints.sh` passe à 100%

---

**Dernière mise à jour:** 13 janvier 2026
**Version:** 1.0
