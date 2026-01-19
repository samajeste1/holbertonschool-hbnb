# HBnB - Simple Web Client (Part 4)

Ce projet implémente le client web frontend pour l'application HBnB en utilisant HTML5, CSS3 et JavaScript ES6.

## Objectifs

- Créer une interface utilisateur interactive
- Implémenter l'authentification côté client
- Interagir avec l'API backend via Fetch API
- Gérer les sessions avec des cookies JWT
- Implémenter le filtrage côté client

## Structure du projet

```
part4/
├── index.html           # Page principale (liste des places)
├── login.html           # Page de connexion
├── place.html           # Détails d'un place
├── add_review.html      # Formulaire d'ajout de review
├── css/
│   └── styles.css       # Styles CSS
├── js/
│   └── scripts.js       # Logique JavaScript
├── images/
│   ├── logo.png         # Logo de l'application
│   └── icon.png         # Favicon
└── README.md
```

## Tâches

### Task 0: Design
- Compléter les fichiers HTML et CSS
- Créer les pages : Login, List of Places, Place Details, Add Review
- Respecter les spécifications de design
- Validation W3C

### Task 1: Login
- Implémenter la fonctionnalité de login
- Faire une requête AJAX à l'API
- Stocker le JWT token dans un cookie
- Rediriger vers index.html après login

### Task 2: Index
- Afficher la liste de tous les places
- Fetch des données depuis l'API
- Implémenter le filtrage par prix côté client
- Afficher/masquer le lien de login selon l'authentification

### Task 3: Place Details
- Afficher les détails d'un place
- Fetch des détails depuis l'API avec l'ID
- Afficher les informations : nom, description, prix, amenities, reviews
- Afficher le formulaire d'ajout de review si authentifié

### Task 4: Add Review Form
- Implémenter le formulaire d'ajout de review
- Vérifier l'authentification (rediriger si non authentifié)
- Envoyer les données à l'API
- Gérer les réponses (succès/erreur)

## Spécifications de design

### Structure requise

**Header:**
- Logo avec classe `logo`
- Bouton/lien de login avec classe `login-button`

**Footer:**
- Texte "All rights reserved"

**Navigation:**
- Liens vers index.html et login.html

### Classes CSS requises

- `.place-card` - Carte pour chaque place
- `.details-button` - Bouton "View Details"
- `.place-details` - Section détails du place
- `.place-info` - Informations du place
- `.review-card` - Carte pour chaque review
- `.add-review` - Section formulaire d'ajout
- `.form` - Formulaire

### Paramètres fixes

- Margin: 20px pour les cartes
- Padding: 10px dans les cartes
- Border: 1px solid #ddd
- Border-radius: 10px

### Paramètres flexibles

- Palette de couleurs (choix libre)
- Police (choix libre)
- Images (choix libre)

## Configuration CORS

Pour permettre au client de communiquer avec l'API, il faut configurer CORS dans le backend Flask :

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

## Utilisation

1. Ouvrir `index.html` dans un navigateur
2. Se connecter via `login.html`
3. Naviguer vers les détails d'un place
4. Ajouter des reviews (si authentifié)

## Ressources

- [HTML5 Documentation](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS3 Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript ES6](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

## Auteur

Holberton School - Team: Allan, Bony, Rattler



