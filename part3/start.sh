#!/bin/bash

echo "================================================"
echo "      HBnB Part 3 - Démarrage du projet"
echo "================================================"
echo

# Vérification de l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
    echo "Environnement virtuel créé."
fi

# Activation de l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate

# Installation des dépendances
echo
echo "Installation des dépendances..."
pip install -q -r requirements.txt

# Vérification de la base de données
if [ ! -f "development.db" ]; then
    echo
    echo "Initialisation de la base de données..."
    python init_db.py
else
    echo
    echo "Base de données existante détectée."
    read -p "Voulez-vous réinitialiser la base de données ? (o/N): " reinit
    if [ "$reinit" = "o" ] || [ "$reinit" = "O" ]; then
        python init_db.py --drop
    fi
fi

# Démarrage du serveur
echo
echo "================================================"
echo "Démarrage du serveur Flask..."
echo "================================================"
python run.py
