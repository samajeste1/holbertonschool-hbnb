"""
Repository pattern implementation for in-memory data storage
Implementation du pattern Repository pour le stockage en memoire
Le Repository agit comme une couche d'abstraction entre la logique metier et le stockage
"""

# Importe ABC (Abstract Base Class) et abstractmethod pour creer des classes abstraites
# Une classe abstraite ne peut pas etre instanciee directement
from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract base repository class
    Classe abstraite definissant l'interface que tous les repositories doivent implementer
    Utilise le pattern Repository pour separer la logique de stockage
    """

    @abstractmethod
    def add(self, obj):
        """
        Add an object to the repository
        Ajoute un objet au repository
        Methode abstraite: doit etre implementee par les classes filles
        """
        pass  # pass indique que la methode n'a pas d'implementation ici

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by ID
        Recupere un objet par son identifiant unique
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects
        Recupere tous les objets stockes
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an object
        Met a jour un objet existant avec de nouvelles donnees
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object
        Supprime un objet du repository
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute
        Recherche un objet par la valeur d'un attribut specifique
        Exemple: trouver un user par son email
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory implementation of the repository pattern
    Implementation du repository qui stocke les donnees en memoire (RAM)
    Les donnees sont perdues quand l'application s'arrete
    Utile pour le developpement et les tests
    """

    def __init__(self):
        """
        Initialize empty storage dictionary
        Initialise un dictionnaire vide pour stocker les objets
        Le dictionnaire utilise l'ID comme cle pour un acces rapide O(1)
        """
        # _storage est "prive" par convention (prefixe _)
        # C'est un dictionnaire: {id: objet, id2: objet2, ...}
        self._storage = {}

    def add(self, obj):
        """
        Add an object to the repository
        Ajoute un objet au stockage

        Args:
            obj: Objet avec un attribut 'id' a stocker
                L'objet doit avoir un attribut id unique
        """
        # Utilise l'ID de l'objet comme cle dans le dictionnaire
        # Permet un acces rapide par ID plus tard
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Retrieve an object by ID
        Recupere un objet par son identifiant

        Args:
            obj_id (str): Identifiant unique de l'objet

        Returns:
            Object if found, None otherwise
            L'objet si trouve, None sinon
        """
        # dict.get() retourne la valeur ou None si la cle n'existe pas
        # Plus sur que self._storage[obj_id] qui leverait une KeyError
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Retrieve all objects
        Recupere tous les objets stockes

        Returns:
            list: Liste de tous les objets (pas les cles)
        """
        # dict.values() retourne toutes les valeurs du dictionnaire
        # list() convertit en liste pour pouvoir iterer plusieurs fois
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update an object with new data
        Met a jour un objet avec de nouvelles donnees

        Args:
            obj_id (str): Identifiant de l'objet a mettre a jour
            data (dict): Dictionnaire des attributs a modifier

        Returns:
            Updated object if found, None otherwise
            L'objet mis a jour si trouve, None sinon
        """
        # Recupere d'abord l'objet existant
        obj = self.get(obj_id)

        # Si l'objet existe
        if obj:
            # Appelle la methode update de l'objet (definie dans BaseModel)
            # Cette methode met a jour les attributs et le timestamp
            obj.update(data)
            return obj

        # Retourne None si l'objet n'a pas ete trouve
        return None

    def delete(self, obj_id):
        """
        Delete an object by ID
        Supprime un objet par son identifiant

        Args:
            obj_id (str): Identifiant de l'objet a supprimer

        Returns:
            bool: True si supprime, False si non trouve
        """
        # Verifie si l'ID existe dans le dictionnaire
        if obj_id in self._storage:
            # del supprime la paire cle-valeur du dictionnaire
            del self._storage[obj_id]
            return True  # Suppression reussie

        # L'objet n'existait pas
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve first object matching attribute value
        Recherche le premier objet ayant un attribut avec une valeur specifique

        Args:
            attr_name (str): Nom de l'attribut a rechercher (ex: 'email')
            attr_value: Valeur a trouver (ex: 'john@example.com')

        Returns:
            Object if found, None otherwise
            Le premier objet trouve ou None
        """
        # Parcourt tous les objets stockes
        for obj in self._storage.values():
            # Verifie si l'objet a cet attribut ET si la valeur correspond
            # hasattr() verifie l'existence de l'attribut
            # getattr() recupere la valeur de l'attribut
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                # Retourne le premier objet trouve
                return obj

        # Aucun objet ne correspond
        return None
