import logging
from abc import ABC, abstractmethod
from datetime import datetime

# --- LOGGING CONFIGURATION ---
# Requirement: Each error must be recorded in a log file[cite: 18, 31].
logging.basicConfig(
    filename='system_errors.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- CUSTOM EXCEPTIONS ---
# Requirement: Use custom exceptions for robust error handling[cite: 17, 19].
class SoftwareFJError(Exception):
    """Base class for exceptions in this module."""
    pass

class ValidationError(SoftwareFJError):
    """Exception raised for errors in the input data."""
    pass

class ReservationError(SoftwareFJError):
    """Exception raised for logic errors during reservation processes."""
    pass

# --- ABSTRACT BASE CLASSES ---
# Requirement: A general abstract class for system entities[cite: 21].
class Entity(ABC):
    """
    Abstract base class to represent any entity within the Software FJ system.
    Ensures all entities have an identification and basic string representation.
    """
    def __init__(self, id_entity):
        self._id_entity = id_entity

    @property
    def id_entity(self):
        return self._id_entity

    @abstractmethod
    def __str__(self):
        pass

# Requirement: An abstract class 'Servicio'[cite: 23].
class Servicio(ABC):
    """
    Abstract class for services (Rooms, Equipment, Consultancy).
    Implements polymorphism through abstract methods for costs and descriptions[cite: 24].
    """
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        """Must be implemented by subclasses to calculate total price[cite: 24]."""
        pass

    @abstractmethod
    def obtener_descripcion(self):
        """Must be implemented to describe the specific service[cite: 24]."""
        pass
    
    class Cliente(Entity):
    """
    Represents a client with robust data validation and encapsulation[cite: 22].
    """
    def __init__(self, id_cliente, nombre, email):
        super().__init__(id_cliente)
        # We use setters to trigger validation during initialization
        self.nombre = nombre
        self.email = email

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        # Validation: Name cannot be empty or just numbers [cite: 19]
        if not valor or not isinstance(valor, str) or len(valor) < 3:
            raise ValidationError(f"Invalid name: {valor}. Must be a string of at least 3 characters.")
        self._nombre = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        # Basic validation: Must contain '@' and '.' [cite: 19]
        if "@" not in valor or "." not in valor:
            raise ValidationError(f"Invalid email format: {valor}.")
        self._email = valor

    def __str__(self):
        return f"Cliente [ID: {self.id_entity}, Nombre: {self.nombre}, Email: {self.email}]"