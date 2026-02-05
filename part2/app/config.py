"""
Configuration module for HBnB Part 2
Module de configuration pour HBnB Part 2
Contient les differentes classes de configuration selon l'environnement
"""

# Importe le module os pour acceder aux variables d'environnement systeme
import os


class Config:
    """
    Base configuration class
    Classe de configuration de base dont heritent toutes les autres
    Contient les parametres communs a tous les environnements
    """
    # Cle secrete pour signer les sessions et tokens
    # os.environ.get() essaie d'abord de lire la variable d'env 'SECRET_KEY'
    # Si elle n'existe pas, utilise la valeur par defaut
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Mode debug desactive par defaut (securite en production)
    DEBUG = False

    # Mode test desactive par defaut
    TESTING = False


class DevelopmentConfig(Config):
    """
    Development configuration
    Configuration pour l'environnement de developpement
    Herite de Config et surcharge certains parametres
    """
    # Active le mode debug pour voir les erreurs detaillees
    # et activer le rechargement automatique du code
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configuration
    Configuration pour les tests automatises
    """
    # Active le mode test de Flask
    TESTING = True

    # Active aussi le debug pour voir les erreurs pendant les tests
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configuration
    Configuration pour l'environnement de production (serveur live)
    """
    # Desactive le debug en production pour la securite
    # Ne jamais exposer les erreurs detaillees aux utilisateurs
    DEBUG = False


# Dictionnaire qui mappe les noms d'environnement aux classes de configuration
# Permet de charger facilement la bonne config avec config['development']
config = {
    'development': DevelopmentConfig,   # Pour le developpement local
    'testing': TestingConfig,           # Pour les tests automatises
    'production': ProductionConfig,     # Pour le serveur de production
    'default': DevelopmentConfig        # Configuration par defaut
}
