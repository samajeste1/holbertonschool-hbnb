#!/bin/bash

# Script de test complet pour tous les endpoints de HBnB Part 2
# Ce script teste tous les endpoints CRUD sans authentification JWT

echo "=========================================="
echo "Tests des endpoints HBnB Part 2"
echo "=========================================="
echo ""

BASE_URL="http://localhost:5000/api/v1"

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables pour stocker les IDs
USER_ID=""
USER2_ID=""
AMENITY_ID=""
AMENITY2_ID=""
PLACE_ID=""
REVIEW_ID=""

echo -e "${YELLOW}=== TEST 1: Créer un utilisateur ===${NC}"
RESPONSE=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Allan",
    "last_name": "Bony",
    "email": "allan.bony@example.com"
  }')

echo "$RESPONSE" | python -m json.tool
USER_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")

if [ -n "$USER_ID" ]; then
    echo -e "${GREEN}✓ Utilisateur créé avec ID: $USER_ID${NC}"
else
    echo -e "${RED}✗ Échec de création de l'utilisateur${NC}"
fi
echo ""

echo -e "${YELLOW}=== TEST 2: Créer un second utilisateur ===${NC}"
RESPONSE=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }')

echo "$RESPONSE" | python -m json.tool
USER2_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo -e "${GREEN}✓ Second utilisateur créé avec ID: $USER2_ID${NC}"
echo ""

echo -e "${YELLOW}=== TEST 3: Récupérer la liste des utilisateurs ===${NC}"
curl -s -X GET "$BASE_URL/users/" | python -m json.tool
echo -e "${GREEN}✓ Liste des utilisateurs récupérée${NC}"
echo ""

echo -e "${YELLOW}=== TEST 4: Récupérer un utilisateur par ID ===${NC}"
curl -s -X GET "$BASE_URL/users/$USER_ID" | python -m json.tool
echo -e "${GREEN}✓ Utilisateur récupéré${NC}"
echo ""

echo -e "${YELLOW}=== TEST 5: Mettre à jour un utilisateur ===${NC}"
curl -s -X PUT "$BASE_URL/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Allan Updated",
    "last_name": "Bony Updated",
    "email": "allan.updated@example.com"
  }' | python -m json.tool
echo -e "${GREEN}✓ Utilisateur mis à jour${NC}"
echo ""

echo -e "${YELLOW}=== TEST 6: Créer une première amenity ===${NC}"
RESPONSE=$(curl -s -X POST "$BASE_URL/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}')

echo "$RESPONSE" | python -m json.tool
AMENITY_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo -e "${GREEN}✓ Amenity créée avec ID: $AMENITY_ID${NC}"
echo ""

echo -e "${YELLOW}=== TEST 7: Créer une seconde amenity ===${NC}"
RESPONSE=$(curl -s -X POST "$BASE_URL/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Air Conditioning"}')

echo "$RESPONSE" | python -m json.tool
AMENITY2_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo -e "${GREEN}✓ Amenity créée avec ID: $AMENITY2_ID${NC}"
echo ""

echo -e "${YELLOW}=== TEST 8: Récupérer la liste des amenities ===${NC}"
curl -s -X GET "$BASE_URL/amenities/" | python -m json.tool
echo -e "${GREEN}✓ Liste des amenities récupérée${NC}"
echo ""

echo -e "${YELLOW}=== TEST 9: Mettre à jour une amenity ===${NC}"
curl -s -X PUT "$BASE_URL/amenities/$AMENITY_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "High-Speed Wi-Fi"}' | python -m json.tool
echo -e "${GREEN}✓ Amenity mise à jour${NC}"
echo ""

echo -e "${YELLOW}=== TEST 10: Créer un place ===${NC}"
RESPONSE=$(curl -s -X POST "$BASE_URL/places/" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Cozy Apartment\",
    \"description\": \"A nice place to stay\",
    \"price\": 100.0,
    \"latitude\": 37.7749,
    \"longitude\": -122.4194,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$AMENITY_ID\", \"$AMENITY2_ID\"]
  }")

echo "$RESPONSE" | python -m json.tool
PLACE_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo -e "${GREEN}✓ Place créé avec ID: $PLACE_ID${NC}"
echo ""

echo -e "${YELLOW}=== TEST 11: Récupérer un place par ID (avec owner et amenities) ===${NC}"
curl -s -X GET "$BASE_URL/places/$PLACE_ID" | python -m json.tool
echo -e "${GREEN}✓ Place récupéré avec détails${NC}"
echo ""

echo -e "${YELLOW}=== TEST 12: Récupérer la liste des places ===${NC}"
curl -s -X GET "$BASE_URL/places/" | python -m json.tool
echo -e "${GREEN}✓ Liste des places récupérée${NC}"
echo ""

echo -e "${YELLOW}=== TEST 13: Mettre à jour un place ===${NC}"
curl -s -X PUT "$BASE_URL/places/$PLACE_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Luxury Condo\",
    \"description\": \"An upscale place to stay\",
    \"price\": 200.0,
    \"latitude\": 37.7749,
    \"longitude\": -122.4194,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$AMENITY_ID\"]
  }" | python -m json.tool
echo -e "${GREEN}✓ Place mis à jour${NC}"
echo ""

echo -e "${YELLOW}=== TEST 14: Créer une review ===${NC}"
RESPONSE=$(curl -s -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Great place to stay!\",
    \"rating\": 5,
    \"user_id\": \"$USER2_ID\",
    \"place_id\": \"$PLACE_ID\"
  }")

echo "$RESPONSE" | python -m json.tool
REVIEW_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
echo -e "${GREEN}✓ Review créée avec ID: $REVIEW_ID${NC}"
echo ""

echo -e "${YELLOW}=== TEST 15: Récupérer toutes les reviews ===${NC}"
curl -s -X GET "$BASE_URL/reviews/" | python -m json.tool
echo -e "${GREEN}✓ Liste des reviews récupérée${NC}"
echo ""

echo -e "${YELLOW}=== TEST 16: Récupérer une review par ID ===${NC}"
curl -s -X GET "$BASE_URL/reviews/$REVIEW_ID" | python -m json.tool
echo -e "${GREEN}✓ Review récupérée${NC}"
echo ""

echo -e "${YELLOW}=== TEST 17: Récupérer les reviews d'un place ===${NC}"
curl -s -X GET "$BASE_URL/places/$PLACE_ID/reviews" | python -m json.tool
echo -e "${GREEN}✓ Reviews du place récupérées${NC}"
echo ""

echo -e "${YELLOW}=== TEST 18: Mettre à jour une review ===${NC}"
curl -s -X PUT "$BASE_URL/reviews/$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Amazing stay!\",
    \"rating\": 4,
    \"user_id\": \"$USER2_ID\",
    \"place_id\": \"$PLACE_ID\"
  }" | python -m json.tool
echo -e "${GREEN}✓ Review mise à jour${NC}"
echo ""

echo -e "${YELLOW}=== TEST 19: Supprimer une review ===${NC}"
curl -s -X DELETE "$BASE_URL/reviews/$REVIEW_ID" | python -m json.tool
echo -e "${GREEN}✓ Review supprimée${NC}"
echo ""

echo -e "${YELLOW}=== TEST 20: Vérifier la suppression ===${NC}"
curl -s -X GET "$BASE_URL/reviews/$REVIEW_ID" | python -m json.tool
echo -e "${GREEN}✓ Vérification effectuée${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}TOUS LES TESTS SONT TERMINÉS${NC}"
echo "=========================================="
