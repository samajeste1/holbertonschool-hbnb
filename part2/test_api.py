#!/usr/bin/env python3
"""
Script de test automatique pour l'API HBnB Part 2
Usage: python test_api.py
"""

import requests
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

BASE_URL = "http://localhost:5000/api/v1"

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.user_id = None
        self.amenity_id = None
        self.place_id = None
        self.review_id = None
        self.passed = 0
        self.failed = 0

    def print_header(self, title):
        print(f"\n{Fore.YELLOW}{'=' * 50}")
        print(f"{title}")
        print(f"{'=' * 50}{Style.RESET_ALL}\n")

    def print_test(self, test_name):
        print(f"{Fore.CYAN}▶ {test_name}{Style.RESET_ALL}")

    def print_success(self, message):
        print(f"{Fore.GREEN}  ✓ {message}{Style.RESET_ALL}")
        self.passed += 1

    def print_error(self, message):
        print(f"{Fore.RED}  ✗ {message}{Style.RESET_ALL}")
        self.failed += 1

    def print_info(self, message):
        print(f"  {Fore.WHITE}{message}{Style.RESET_ALL}")

    def test_create_user(self):
        self.print_test("Test 1: Créer un utilisateur")

        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@test.com"
        }

        try:
            response = requests.post(f"{self.base_url}/users/", json=data)

            if response.status_code == 201:
                result = response.json()
                self.user_id = result.get('id')
                self.print_success(f"Utilisateur créé (ID: {self.user_id})")
                self.print_info(f"Réponse: {json.dumps(result, indent=2)}")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
                self.print_info(f"Réponse: {response.text}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_get_all_users(self):
        self.print_test("Test 2: Récupérer tous les utilisateurs")

        try:
            response = requests.get(f"{self.base_url}/users/")

            if response.status_code == 200:
                users = response.json()
                self.print_success(f"{len(users)} utilisateur(s) trouvé(s)")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_get_user_by_id(self):
        self.print_test("Test 3: Récupérer un utilisateur par ID")

        if not self.user_id:
            self.print_error("Pas d'ID utilisateur disponible")
            return

        try:
            response = requests.get(f"{self.base_url}/users/{self.user_id}")

            if response.status_code == 200:
                user = response.json()
                if user.get('id') == self.user_id:
                    self.print_success("Utilisateur récupéré avec succès")
                else:
                    self.print_error("ID incorrect dans la réponse")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_update_user(self):
        self.print_test("Test 4: Mettre à jour un utilisateur")

        if not self.user_id:
            self.print_error("Pas d'ID utilisateur disponible")
            return

        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@test.com"
        }

        try:
            response = requests.put(f"{self.base_url}/users/{self.user_id}", json=data)

            if response.status_code == 200:
                user = response.json()
                if user.get('first_name') == "Jane":
                    self.print_success("Utilisateur mis à jour avec succès")
                else:
                    self.print_error("Données non mises à jour")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
                self.print_info(f"Réponse: {response.text}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_create_amenity(self):
        self.print_test("Test 5: Créer un amenity")

        data = {"name": "Wi-Fi"}

        try:
            response = requests.post(f"{self.base_url}/amenities/", json=data)

            if response.status_code == 201:
                result = response.json()
                self.amenity_id = result.get('id')
                self.print_success(f"Amenity créé (ID: {self.amenity_id})")
                self.print_info(f"Réponse: {json.dumps(result, indent=2)}")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
                self.print_info(f"Réponse: {response.text}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_get_all_amenities(self):
        self.print_test("Test 6: Récupérer tous les amenities")

        try:
            response = requests.get(f"{self.base_url}/amenities/")

            if response.status_code == 200:
                amenities = response.json()
                self.print_success(f"{len(amenities)} amenity(ies) trouvé(s)")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_update_amenity(self):
        self.print_test("Test 7: Mettre à jour un amenity")

        if not self.amenity_id:
            self.print_error("Pas d'ID amenity disponible")
            return

        data = {"name": "High-Speed Wi-Fi"}

        try:
            response = requests.put(f"{self.base_url}/amenities/{self.amenity_id}", json=data)

            if response.status_code == 200:
                result = response.json()
                if result.get('message') == "Amenity updated successfully":
                    self.print_success("Amenity mis à jour avec succès")
                    self.print_info(f"Réponse: {json.dumps(result, indent=2)}")
                else:
                    self.print_error(f"Message incorrect: {result}")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
                self.print_info(f"Réponse: {response.text}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_create_place(self):
        self.print_test("Test 8: Créer un place")

        if not self.user_id:
            self.print_error("Pas d'ID utilisateur disponible")
            return

        data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id,
            "amenities": [self.amenity_id] if self.amenity_id else []
        }

        try:
            response = requests.post(f"{self.base_url}/places/", json=data)

            if response.status_code == 201:
                result = response.json()
                self.place_id = result.get('id')
                self.print_success(f"Place créé (ID: {self.place_id})")
                self.print_info(f"Inclut owner: {'owner' in result}")
                self.print_info(f"Inclut amenities: {'amenities' in result}")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
                self.print_info(f"Réponse: {response.text}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_create_review(self):
        self.print_test("Test 9: Créer un review")

        if not self.user_id or not self.place_id:
            self.print_error("Pas d'ID utilisateur ou place disponible")
            return

        data = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }

        try:
            response = requests.post(f"{self.base_url}/reviews/", json=data)

            if response.status_code == 201:
                result = response.json()
                self.review_id = result.get('id')
                self.print_success(f"Review créé (ID: {self.review_id})")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
                self.print_info(f"Réponse: {response.text}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_delete_review(self):
        self.print_test("Test 10: Supprimer un review")

        if not self.review_id:
            self.print_error("Pas d'ID review disponible")
            return

        try:
            response = requests.delete(f"{self.base_url}/reviews/{self.review_id}")

            if response.status_code == 204:
                self.print_success("Review supprimé avec succès")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_email_uniqueness(self):
        self.print_test("Test 11: Validation email unique")

        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "jane.doe@test.com"  # Email déjà utilisé
        }

        try:
            response = requests.post(f"{self.base_url}/users/", json=data)

            if response.status_code == 400:
                result = response.json()
                if 'already registered' in result.get('error', '').lower():
                    self.print_success("Validation email unique fonctionne")
                else:
                    self.print_error("Message d'erreur incorrect")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def test_invalid_rating(self):
        self.print_test("Test 12: Validation rating (1-5)")

        if not self.user_id or not self.place_id:
            self.print_error("Pas d'ID utilisateur ou place disponible")
            return

        data = {
            "text": "Test review",
            "rating": 10,  # Rating invalide
            "user_id": self.user_id,
            "place_id": self.place_id
        }

        try:
            response = requests.post(f"{self.base_url}/reviews/", json=data)

            if response.status_code == 400:
                self.print_success("Validation rating fonctionne")
            else:
                self.print_error(f"Status code incorrect: {response.status_code}")
        except Exception as e:
            self.print_error(f"Exception: {str(e)}")

    def run_all_tests(self):
        self.print_header("Tests API HBnB Part 2")

        # Tests création
        self.test_create_user()
        self.test_create_amenity()
        self.test_create_place()
        self.test_create_review()

        # Tests récupération
        self.test_get_all_users()
        self.test_get_user_by_id()
        self.test_get_all_amenities()

        # Tests mise à jour
        self.test_update_user()
        self.test_update_amenity()

        # Tests suppression
        self.test_delete_review()

        # Tests validation
        self.test_email_uniqueness()
        self.test_invalid_rating()

        # Résumé
        self.print_header("Résumé des Tests")
        total = self.passed + self.failed
        print(f"{Fore.GREEN}Tests réussis: {self.passed}/{total}{Style.RESET_ALL}")
        print(f"{Fore.RED}Tests échoués: {self.failed}/{total}{Style.RESET_ALL}")

        if self.failed == 0:
            print(f"\n{Fore.GREEN}{'🎉 Tous les tests sont passés ! 🎉':^50}{Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.RED}{'⚠️  Certains tests ont échoué  ⚠️':^50}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    print(f"\n{Fore.CYAN}Assurez-vous que l'API est lancée sur {BASE_URL}{Style.RESET_ALL}\n")

    try:
        # Test de connexion
        response = requests.get(f"{BASE_URL}/amenities/", timeout=2)

        tester = APITester()
        tester.run_all_tests()

    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}❌ Erreur: Impossible de se connecter à l'API")
        print(f"Veuillez lancer l'application avec: python run.py{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}❌ Erreur: {str(e)}{Style.RESET_ALL}\n")
