"""
Main application entry point for the HBnB API server.
Point d'entree principal du serveur API HBnB Part 3
Ce fichier lance le serveur Flask avec SQLAlchemy et authentification JWT
"""

# Importe la fonction create_app depuis le package app
# Cette fonction cree et configure l'application Flask complete
from app import create_app

# Cree l'instance de l'application Flask
# create_app() configure SQLAlchemy, JWT, CORS et toutes les routes
app = create_app()

# Bloc conditionnel: s'execute uniquement quand ce fichier est lance directement
if __name__ == '__main__':
    # Configuration du serveur de developpement
    host = '0.0.0.0'  # Ecoute sur toutes les interfaces (accessible depuis le reseau)
    port = 5001       # Port du serveur HBnB Part 3
    debug = True      # Mode debug pour le developpement (recharge auto)

    # Affiche un en-tete informatif au demarrage
    print("\n" + "="*50)
    print("HBnB API Server")
    print("="*50)

    # Affiche toutes les routes disponibles
    # url_map contient toutes les regles de routage de Flask
    print("\nAvailable routes:")
    # Trie les routes par leur URL pour un affichage plus lisible
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        # Filtre les methodes OPTIONS et HEAD (automatiques)
        methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
        # Affiche: URL -> nom_endpoint [METHODES]
        print(f"  {rule.rule} -> {rule.endpoint} [{methods}]")

    # Affiche les URLs importantes pour le developpeur
    # Utilise 127.0.0.1 pour que les liens soient cliquables dans le terminal
    display_url = f"http://127.0.0.1:{port}"
    print("\nImportant URLs (clickable in terminal):")
    print(f"  Swagger UI:    {display_url}/ (redirige vers /api/v1/doc/")
    print(f"  Users API:     {display_url}/api/v1/users")
    print(f"  Amenities API: {display_url}/api/v1/amenities")
    print(f"  Health check:  {display_url}/health")

    # Affiche la configuration actuelle
    print("\nConfiguration:")
    print(f"  Debug mode: {debug}")
    print(f"  Host: 0.0.0.0 (accessible from network)")
    print(f"  Port: {port}")

    # Message de demarrage final
    print("\n" + "="*50)
    print("Starting server... (Press Ctrl+C to stop)")
    print("="*50 + "\n")

    # Lance le serveur de developpement Flask
    # host, port, debug: configuration du serveur
    app.run(host=host, port=port, debug=debug)
