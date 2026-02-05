"""
Application Factory for HBnB Part 3
Usine a application avec SQLAlchemy, JWT et CORS
Ce fichier initialise toutes les extensions Flask necessaires
"""

# Importe Flask et redirect pour les redirections
from flask import Flask, redirect

# Importe Bcrypt pour le hachage securise des mots de passe
from flask_bcrypt import Bcrypt

# Importe JWTManager pour l'authentification par tokens JWT
from flask_jwt_extended import JWTManager

# Importe SQLAlchemy pour l'ORM (mapping objet-relationnel)
from flask_sqlalchemy import SQLAlchemy

# Importe CORS pour autoriser les requetes cross-origin (frontend different)
from flask_cors import CORS

# Cree les instances globales des extensions
# Elles seront initialisees avec l'app dans create_app()
jwt = JWTManager()      # Gestionnaire de tokens JWT
bcrypt = Bcrypt()       # Utilitaire de hachage de mots de passe
db = SQLAlchemy()       # ORM pour la base de donnees

# Importe le blueprint de l'API v1
# Fait ici pour eviter les imports circulaires
from app.api.v1 import api_bp


def create_app(config_name="development"):
    """
    Cree l'application Flask avec la configuration specifiee.
    Factory pattern permettant de creer plusieurs instances

    Args:
        config_name (str): Nom de la configuration
                          ('development', 'testing', 'production')
    """
    # Cree l'instance Flask
    app = Flask(__name__)

    # Dictionnaire mappant les noms aux classes de configuration
    # Permet de charger facilement differentes configs
    config_map = {
        'development': 'config.DevelopmentConfig',   # Dev local avec debug
        'testing': 'config.TestingConfig',           # Tests avec DB en memoire
        'production': 'config.ProductionConfig'      # Production securisee
    }

    # Selectionne la classe de config, defaut sur development
    config_class = config_map.get(config_name.lower(), 'config.DevelopmentConfig')
    # Charge la configuration dans l'app
    app.config.from_object(config_class)

    # Configure JWT avec la meme cle secrete que l'app
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    # Les tokens expirent apres 1 heure (3600 secondes)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

    # Initialise Bcrypt avec l'application
    # Permet d'utiliser bcrypt.generate_password_hash() etc.
    bcrypt.init_app(app)

    # Initialise JWT avec l'application
    # Active les decorateurs @jwt_required() etc.
    jwt.init_app(app)

    # Initialise SQLAlchemy avec l'application
    # Connecte a la base de donnees configuree
    db.init_app(app)

    # Active CORS pour toutes les routes /api/*
    # origins="*" autorise toutes les origines (a restreindre en prod)
    # supports_credentials=True permet les cookies/auth headers
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Configure les callbacks JWT (gestion des erreurs, claims, etc.)
    from app.api import configure_jwt
    configure_jwt(jwt)

    # Enregistre le blueprint de l'API
    app.register_blueprint(api_bp)

    # Route racine qui redirige vers la documentation Swagger
    @app.route('/')
    def root():
        # redirect() retourne une reponse HTTP 302
        return redirect('/api/v1/doc/')

    # Endpoint de verification de sante
    # Utile pour les load balancers et le monitoring
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    # Retourne l'application configuree
    return app
