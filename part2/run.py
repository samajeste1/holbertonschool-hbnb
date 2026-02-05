#!/usr/bin/env python3
# Ligne shebang : indique que ce script doit etre execute avec Python 3

"""
Entry point for the HBnB application Part 2
Point d'entree principal de l'application HBnB Part 2
Ce fichier lance le serveur Flask pour l'API REST
"""

# Importe la fonction create_app depuis le package app
# Cette fonction cree et configure l'application Flask
from app import create_app

# Appelle create_app() pour creer une instance de l'application Flask
# Cette instance est stockee dans la variable 'app'
app = create_app()

# Bloc conditionnel : s'execute uniquement si ce fichier est lance directement
# (pas importe comme module)
if __name__ == '__main__':
    # Lance le serveur de developpement Flask avec :
    # - debug=True : mode debug active (rechargement auto, messages d'erreur detailles)
    # - host='0.0.0.0' : ecoute sur toutes les interfaces reseau (accessible depuis le reseau)
    # - port=5000 : le serveur ecoute sur le port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
