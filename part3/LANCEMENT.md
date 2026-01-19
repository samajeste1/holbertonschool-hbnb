# 🚀 Guide de lancement - HBnB Part 3

## 📋 Prérequis

- Python 3.8 ou supérieur installé
- pip (gestionnaire de packages Python)
- Terminal/Invite de commandes

## 🎯 Méthode rapide (RECOMMANDÉ)

### Pour Windows :
```bash
cd C:\Users\Bonya\holbertonschool-higher_level_programming-1\holbertonschool-hbnb\part3
start.bat
```

### Pour Linux/Mac :
```bash
cd /chemin/vers/holbertonschool-hbnb/part3
chmod +x start.sh
./start.sh
```

Le script automatique va :
1. ✅ Créer l'environnement virtuel
2. ✅ Installer les dépendances
3. ✅ Initialiser la base de données
4. ✅ Démarrer le serveur

---

## 📝 Méthode manuelle (étape par étape)

### Étape 1 : Naviguer vers le dossier
```bash
cd C:\Users\Bonya\holbertonschool-higher_level_programming-1\holbertonschool-hbnb\part3
```

### Étape 2 : Créer l'environnement virtuel
**Windows :**
```bash
python -m venv venv
```

**Linux/Mac :**
```bash
python3 -m venv venv
```

### Étape 3 : Activer l'environnement virtuel
**Windows (CMD) :**
```bash
venv\Scripts\activate
```

**Windows (PowerShell) :**
```bash
venv\Scripts\Activate.ps1
```

**Linux/Mac :**
```bash
source venv/bin/activate
```

Vous devriez voir `(venv)` apparaître au début de votre ligne de commande.

### Étape 4 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 5 : Initialiser la base de données
```bash
python init_db.py
```

### Étape 6 : Créer les données de test (OPTIONNEL mais recommandé)
```bash
python seed_data.py
```

Cela créera :
- Un compte administrateur
- Deux utilisateurs de test
- Des amenities (WiFi, Pool, etc.)
- Des places de test

### Étape 7 : Lancer le serveur
```bash
python run.py
```

---

## 🔑 Comptes créés par défaut

Si vous avez exécuté `seed_data.py`, ces comptes sont disponibles :

### Administrateur :
- **Email :** admin@hbnb.io
- **Mot de passe :** admin1234
- **Rôle :** Admin (peut tout faire)

### Utilisateurs de test :
1. **Email :** john.doe@example.com
   - **Mot de passe :** password123

2. **Email :** jane.smith@example.com
   - **Mot de passe :** password123

---

## 🌐 URLs importantes

Une fois le serveur démarré, accédez à :

- **Documentation Swagger UI :** http://127.0.0.1:5000/
- **Health Check :** http://127.0.0.1:5000/health
- **API Users :** http://127.0.0.1:5000/api/v1/users
- **API Places :** http://127.0.0.1:5000/api/v1/places
- **API Reviews :** http://127.0.0.1:5000/api/v1/reviews
- **API Amenities :** http://127.0.0.1:5000/api/v1/amenities
- **Login :** http://127.0.0.1:5000/api/v1/auth/login

---

## 🧪 Tester l'API

### 1. Via Swagger UI (Interface graphique)
Ouvrez http://127.0.0.1:5000/ dans votre navigateur.

### 2. Via cURL (ligne de commande)

**Health Check :**
```bash
curl http://127.0.0.1:5000/health
```

**Login (obtenir un token JWT) :**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@hbnb.io\",\"password\":\"admin1234\"}"
```

**Obtenir tous les utilisateurs (avec token) :**
```bash
curl http://127.0.0.1:5000/api/v1/users ^
  -H "Authorization: Bearer VOTRE_TOKEN_ICI"
```

### 3. Via Postman
Importez la collection d'API et testez les endpoints.

---

## 🛠️ Commandes utiles

### Réinitialiser complètement la base de données :
```bash
python init_db.py --drop
python seed_data.py
```

### Vérifier les tables créées :
```bash
python
>>> from app import create_app, db
>>> app = create_app('development')
>>> with app.app_context():
...     print(db.metadata.tables.keys())
```

### Désactiver l'environnement virtuel :
```bash
deactivate
```

### Arrêter le serveur :
Appuyez sur `Ctrl + C` dans le terminal

---

## ❌ Résolution des problèmes courants

### Erreur : "Module not found"
```bash
# Vérifiez que le venv est activé (vous devez voir (venv))
# Réinstallez les dépendances
pip install -r requirements.txt
```

### Erreur : "Port 5000 already in use"
```bash
# Changez le port dans run.py (ligne 10)
port = 5001  # Au lieu de 5000
```

### Base de données corrompue
```bash
# Supprimez le fichier de base de données et recréez
del development.db  # Windows
rm development.db   # Linux/Mac
python init_db.py
python seed_data.py
```

### Erreur d'activation du venv sur Windows PowerShell
```bash
# Exécutez cette commande une fois en tant qu'administrateur
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📚 Structure du projet

```
part3/
├── app/
│   ├── __init__.py          # Factory de l'application
│   ├── api/                 # Endpoints REST
│   ├── models/              # Modèles SQLAlchemy
│   ├── persistence/         # Repositories
│   └── services/            # Facade pattern
├── config.py                # Configuration
├── run.py                   # Point d'entrée
├── init_db.py              # Initialisation DB
├── seed_data.py            # Données de test
├── requirements.txt        # Dépendances
├── start.bat               # Script Windows
├── start.sh                # Script Linux/Mac
└── development.db          # Base de données SQLite (créée automatiquement)
```

---

## 🎓 Prochaines étapes

1. ✅ Lancer le serveur
2. ✅ Tester le Health Check
3. ✅ Se connecter via l'endpoint /auth/login
4. ✅ Tester les endpoints protégés avec le token JWT
5. ✅ Explorer l'API via Swagger UI
6. ✅ Créer des places, reviews, etc.

---

## 📞 Support

En cas de problème, vérifiez :
1. Que Python est bien installé : `python --version`
2. Que le venv est activé (vous voyez `(venv)`)
3. Que toutes les dépendances sont installées
4. Que la base de données est initialisée
5. Les logs d'erreur dans le terminal

Bon développement ! 🚀
