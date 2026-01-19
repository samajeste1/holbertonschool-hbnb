# 🔧 Résolution du Problème JWT

## 🔴 Problème Initial

Lors du test de l'API Part 2, vous receviez cette erreur:

```json
{
  "msg": "Missing Authorization Header"
}
```

## 🔍 Diagnostic

### Cause Racine

Le serveur **Part 3** (qui utilise JWT) tournait sur le port 5000 au lieu du serveur **Part 2** (sans JWT).

### Indices

1. **Swagger UI montrait des champs inexistants en Part 2:**
   - `password` dans le modèle User
   - `place_list` dans le modèle User

   → Ces champs n'existent QUE dans Part 3

2. **Erreur JWT sur tous les endpoints**
   → Le serveur Part 3 a JWT activé globalement

## ✅ Solution

### Étape 1: Arrêter tous les serveurs Python

```bash
# Windows
taskkill //F //IM python3.11.exe

# Linux/Mac
pkill -f python
```

### Étape 2: Démarrer UNIQUEMENT Part 2

**Option A - Script fourni (Windows):**
```batch
cd holbertonschool-hbnb\part2
start_server.bat
```

**Option B - Ligne de commande:**
```bash
cd holbertonschool-hbnb/part2
python run.py
```

### Étape 3: Vérifier le bon serveur

**Test rapide:**
```bash
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

**Si c'est Part 2 (correct):**
```json
{
  "id": "uuid-here",
  "name": "Wi-Fi",
  "created_at": "2026-01-13T...",
  "updated_at": "2026-01-13T..."
}
```
✅ Status: 201 Created

**Si c'est Part 3 (incorrect):**
```json
{
  "msg": "Missing Authorization Header"
}
```
❌ Status: 401 Unauthorized

## 🎯 Différences Part 2 vs Part 3

| Caractéristique | Part 2 | Part 3 |
|-----------------|--------|--------|
| **Authentification** | ❌ Aucune | ✅ JWT Required |
| **Modèle User** | first_name, last_name, email, is_admin | + password, + place_list |
| **Endpoints protégés** | ❌ Aucun | ✅ Tous (sauf /auth/login) |
| **Base de données** | In-Memory | SQLAlchemy |
| **Fichier __init__.py** | Simple Factory | + JWTManager + Bcrypt |

## 📊 Vérification Visuelle

### Part 2 - Swagger UI (Correct)

Modèle User:
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "is_admin": false
}
```

### Part 3 - Swagger UI (Si vous voyez ça, mauvais serveur!)

Modèle User:
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "password": "string",        ← UNIQUEMENT Part 3
  "place_list": ["string"],    ← UNIQUEMENT Part 3
  "is_admin": false
}
```

## 🛡️ Prévention Future

### 1. Script de démarrage dédié

Utilisez le script `start_server.bat` fourni qui:
- ✅ Arrête tous les serveurs Python existants
- ✅ Démarre UNIQUEMENT Part 2
- ✅ Affiche les routes disponibles

### 2. Vérifier le répertoire de travail

```bash
pwd  # Linux/Mac
cd   # Windows

# Doit afficher:
# .../holbertonschool-hbnb/part2
```

### 3. Vérifier les processus actifs

```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

## 📝 Checklist de Démarrage

- [ ] Tous les serveurs Python sont arrêtés
- [ ] Répertoire de travail = `part2/`
- [ ] Aucun autre processus sur port 5000
- [ ] Lancer `python run.py` depuis `part2/`
- [ ] Vérifier Swagger à http://localhost:5000/api/v1/doc/
- [ ] Tester un endpoint sans JWT

## ✅ Résultat Final

Après résolution:
- ✅ Serveur Part 2 démarre correctement
- ✅ Aucun JWT requis
- ✅ Tous les endpoints accessibles
- ✅ Tests passent à 100%

---

**Problème résolu:** 13 janvier 2026
**Solution:** Arrêt Part 3, démarrage Part 2 uniquement
