"""
Script pour créer des données initiales dans la base de données.
"""
from app import create_app, db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
import uuid

def seed_database():
    """Crée les données initiales dans la base de données."""
    app = create_app('development')

    with app.app_context():
        print("\n" + "="*50)
        print("Création des données initiales...")
        print("="*50 + "\n")

        # Vérifier si des utilisateurs existent déjà
        existing_users = User.query.all()
        if existing_users:
            print("⚠️  Des utilisateurs existent déjà dans la base de données.")
            response = input("Voulez-vous continuer et ajouter de nouvelles données ? (o/N): ")
            if response.lower() != 'o':
                print("Opération annulée.")
                return

        # Créer un utilisateur administrateur
        print("1. Création de l'utilisateur administrateur...")
        admin = User.query.filter_by(email='admin@hbnb.io').first()
        if not admin:
            admin = User(
                first_name='Admin',
                last_name='HBnB',
                email='admin@hbnb.io',
                password='admin1234',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print(f"   ✅ Admin créé : {admin.email}")
            print(f"      ID: {admin.id}")
            print(f"      Mot de passe: admin1234")
        else:
            print(f"   ℹ️  Admin existe déjà : {admin.email}")

        # Créer un utilisateur normal pour les tests
        print("\n2. Création d'utilisateurs de test...")
        test_user = User.query.filter_by(email='john.doe@example.com').first()
        if not test_user:
            test_user = User(
                first_name='John',
                last_name='Doe',
                email='john.doe@example.com',
                password='password123',
                is_admin=False
            )
            db.session.add(test_user)
            db.session.commit()
            print(f"   ✅ Utilisateur créé : {test_user.email}")
            print(f"      ID: {test_user.id}")
            print(f"      Mot de passe: password123")
        else:
            print(f"   ℹ️  Utilisateur existe déjà : {test_user.email}")

        # Créer un deuxième utilisateur de test
        test_user2 = User.query.filter_by(email='jane.smith@example.com').first()
        if not test_user2:
            test_user2 = User(
                first_name='Jane',
                last_name='Smith',
                email='jane.smith@example.com',
                password='password123',
                is_admin=False
            )
            db.session.add(test_user2)
            db.session.commit()
            print(f"   ✅ Utilisateur créé : {test_user2.email}")
            print(f"      ID: {test_user2.id}")
            print(f"      Mot de passe: password123")
        else:
            print(f"   ℹ️  Utilisateur existe déjà : {test_user2.email}")

        # Créer des amenities
        print("\n3. Création des équipements (amenities)...")
        amenities_data = ['WiFi', 'Swimming Pool', 'Air Conditioning', 'Parking', 'Kitchen']
        amenities = []

        for amenity_name in amenities_data:
            amenity = Amenity.query.filter_by(name=amenity_name).first()
            if not amenity:
                amenity = Amenity(name=amenity_name)
                db.session.add(amenity)
                db.session.commit()
                print(f"   ✅ Amenity créé : {amenity.name} (ID: {amenity.id})")
            else:
                print(f"   ℹ️  Amenity existe déjà : {amenity.name}")
            amenities.append(amenity)

        # Créer des places de test
        print("\n4. Création de lieux de test (places)...")
        place1 = Place.query.filter_by(title='Cozy Apartment').first()
        if not place1:
            place1 = Place(
                title='Cozy Apartment',
                description='A comfortable and affordable apartment in the city center',
                price=75.50,
                latitude=37.7749,
                longitude=-122.4194,
                owner_id=test_user.id
            )
            db.session.add(place1)
            db.session.commit()
            # Ajouter quelques amenities
            place1.amenities.extend([amenities[0], amenities[2], amenities[4]])  # WiFi, AC, Kitchen
            db.session.commit()
            print(f"   ✅ Place créé : {place1.title} (ID: {place1.id})")
            print(f"      Propriétaire: {test_user.email}")
        else:
            print(f"   ℹ️  Place existe déjà : {place1.title}")

        place2 = Place.query.filter_by(title='Luxury Villa').first()
        if not place2:
            place2 = Place(
                title='Luxury Villa',
                description='Beautiful villa with ocean view and private pool',
                price=250.00,
                latitude=34.0522,
                longitude=-118.2437,
                owner_id=test_user2.id
            )
            db.session.add(place2)
            db.session.commit()
            # Ajouter plusieurs amenities
            place2.amenities.extend([amenities[0], amenities[1], amenities[2], amenities[3]])
            db.session.commit()
            print(f"   ✅ Place créé : {place2.title} (ID: {place2.id})")
            print(f"      Propriétaire: {test_user2.email}")
        else:
            print(f"   ℹ️  Place existe déjà : {place2.title}")

        print("\n" + "="*50)
        print("✅ Données initiales créées avec succès !")
        print("="*50)

        print("\n📝 Récapitulatif des comptes créés :")
        print("-" * 50)
        print("ADMIN:")
        print(f"  Email: admin@hbnb.io")
        print(f"  Mot de passe: admin1234")
        print(f"  ID: {admin.id}")
        print("\nUTILISATEURS DE TEST:")
        print(f"  1. Email: john.doe@example.com")
        print(f"     Mot de passe: password123")
        print(f"     ID: {test_user.id}")
        print(f"  2. Email: jane.smith@example.com")
        print(f"     Mot de passe: password123")
        print(f"     ID: {test_user2.id}")
        print("-" * 50)
        print("\n💡 Utilisez ces identifiants pour tester l'API\n")

if __name__ == '__main__':
    seed_database()
