#!/bin/bash

# Script de test pour l'API HBnB Part 2
# Usage: ./test_api.sh

BASE_URL="http://localhost:5000/api/v1"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================"
echo "  Tests API HBnB Part 2"
echo "======================================"
echo ""

# Test 1: Créer un utilisateur
echo -e "${YELLOW}Test 1: Créer un utilisateur${NC}"
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}')

USER_ID=$(echo $USER_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

if [ -n "$USER_ID" ]; then
    echo -e "${GREEN}✓ Utilisateur créé avec succès${NC}"
    echo "  ID: $USER_ID"
else
    echo -e "${RED}✗ Échec de création utilisateur${NC}"
    echo "  Réponse: $USER_RESPONSE"
fi
echo ""

# Test 2: Récupérer tous les utilisateurs
echo -e "${YELLOW}Test 2: Récupérer tous les utilisateurs${NC}"
USERS_LIST=$(curl -s -X GET "$BASE_URL/users/")
USER_COUNT=$(echo $USERS_LIST | grep -o '"id"' | wc -l)

if [ "$USER_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ $USER_COUNT utilisateur(s) récupéré(s)${NC}"
else
    echo -e "${RED}✗ Aucun utilisateur trouvé${NC}"
fi
echo ""

# Test 3: Récupérer un utilisateur par ID
echo -e "${YELLOW}Test 3: Récupérer utilisateur par ID${NC}"
if [ -n "$USER_ID" ]; then
    USER_DETAIL=$(curl -s -X GET "$BASE_URL/users/$USER_ID")
    if echo $USER_DETAIL | grep -q "\"id\":\"$USER_ID\""; then
        echo -e "${GREEN}✓ Utilisateur récupéré avec succès${NC}"
    else
        echo -e "${RED}✗ Échec récupération utilisateur${NC}"
    fi
else
    echo -e "${RED}✗ Pas d'ID utilisateur disponible${NC}"
fi
echo ""

# Test 4: Mettre à jour un utilisateur
echo -e "${YELLOW}Test 4: Mettre à jour un utilisateur${NC}"
if [ -n "$USER_ID" ]; then
    UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/users/$USER_ID" \
      -H "Content-Type: application/json" \
      -d '{"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com"}')

    if echo $UPDATE_RESPONSE | grep -q "Jane"; then
        echo -e "${GREEN}✓ Utilisateur mis à jour avec succès${NC}"
    else
        echo -e "${RED}✗ Échec mise à jour utilisateur${NC}"
    fi
else
    echo -e "${RED}✗ Pas d'ID utilisateur disponible${NC}"
fi
echo ""

# Test 5: Créer un amenity
echo -e "${YELLOW}Test 5: Créer un amenity${NC}"
AMENITY_RESPONSE=$(curl -s -X POST "$BASE_URL/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}')

AMENITY_ID=$(echo $AMENITY_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

if [ -n "$AMENITY_ID" ]; then
    echo -e "${GREEN}✓ Amenity créé avec succès${NC}"
    echo "  ID: $AMENITY_ID"
else
    echo -e "${RED}✗ Échec création amenity${NC}"
    echo "  Réponse: $AMENITY_RESPONSE"
fi
echo ""

# Test 6: Récupérer tous les amenities
echo -e "${YELLOW}Test 6: Récupérer tous les amenities${NC}"
AMENITIES_LIST=$(curl -s -X GET "$BASE_URL/amenities/")
AMENITY_COUNT=$(echo $AMENITIES_LIST | grep -o '"id"' | wc -l)

if [ "$AMENITY_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ $AMENITY_COUNT amenity(ies) récupéré(s)${NC}"
else
    echo -e "${RED}✗ Aucun amenity trouvé${NC}"
fi
echo ""

# Test 7: Mettre à jour un amenity
echo -e "${YELLOW}Test 7: Mettre à jour un amenity${NC}"
if [ -n "$AMENITY_ID" ]; then
    AMENITY_UPDATE=$(curl -s -X PUT "$BASE_URL/amenities/$AMENITY_ID" \
      -H "Content-Type: application/json" \
      -d '{"name": "High-Speed Wi-Fi"}')

    if echo $AMENITY_UPDATE | grep -q "Amenity updated successfully"; then
        echo -e "${GREEN}✓ Amenity mis à jour avec succès${NC}"
    else
        echo -e "${RED}✗ Échec mise à jour amenity${NC}"
        echo "  Réponse: $AMENITY_UPDATE"
    fi
else
    echo -e "${RED}✗ Pas d'ID amenity disponible${NC}"
fi
echo ""

# Test 8: Créer un place
echo -e "${YELLOW}Test 8: Créer un place${NC}"
if [ -n "$USER_ID" ] && [ -n "$AMENITY_ID" ]; then
    PLACE_RESPONSE=$(curl -s -X POST "$BASE_URL/places/" \
      -H "Content-Type: application/json" \
      -d "{\"title\": \"Cozy Apartment\", \"description\": \"A nice place\", \"price\": 100, \"latitude\": 37.7749, \"longitude\": -122.4194, \"owner_id\": \"$USER_ID\", \"amenities\": [\"$AMENITY_ID\"]}")

    PLACE_ID=$(echo $PLACE_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

    if [ -n "$PLACE_ID" ]; then
        echo -e "${GREEN}✓ Place créé avec succès${NC}"
        echo "  ID: $PLACE_ID"
    else
        echo -e "${RED}✗ Échec création place${NC}"
        echo "  Réponse: $PLACE_RESPONSE"
    fi
else
    echo -e "${RED}✗ Pas d'ID utilisateur ou amenity disponible${NC}"
fi
echo ""

# Test 9: Créer un review
echo -e "${YELLOW}Test 9: Créer un review${NC}"
if [ -n "$USER_ID" ] && [ -n "$PLACE_ID" ]; then
    REVIEW_RESPONSE=$(curl -s -X POST "$BASE_URL/reviews/" \
      -H "Content-Type: application/json" \
      -d "{\"text\": \"Great place!\", \"rating\": 5, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}")

    REVIEW_ID=$(echo $REVIEW_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

    if [ -n "$REVIEW_ID" ]; then
        echo -e "${GREEN}✓ Review créé avec succès${NC}"
        echo "  ID: $REVIEW_ID"
    else
        echo -e "${RED}✗ Échec création review${NC}"
        echo "  Réponse: $REVIEW_RESPONSE"
    fi
else
    echo -e "${RED}✗ Pas d'ID utilisateur ou place disponible${NC}"
fi
echo ""

# Test 10: Supprimer un review
echo -e "${YELLOW}Test 10: Supprimer un review${NC}"
if [ -n "$REVIEW_ID" ]; then
    DELETE_RESPONSE=$(curl -s -w "%{http_code}" -X DELETE "$BASE_URL/reviews/$REVIEW_ID")

    if [ "$DELETE_RESPONSE" = "204" ]; then
        echo -e "${GREEN}✓ Review supprimé avec succès${NC}"
    else
        echo -e "${RED}✗ Échec suppression review${NC}"
        echo "  Code: $DELETE_RESPONSE"
    fi
else
    echo -e "${RED}✗ Pas d'ID review disponible${NC}"
fi
echo ""

echo "======================================"
echo "  Fin des tests"
echo "======================================"
