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
    
    class ServicioSala(Servicio):
    """Specialized service for Room Reservations[cite: 10, 24]."""
    
    def calcular_costo(self, horas, descuento=0):
        """
        Implementation of cost calculation with optional parameter (overloading simulation)[cite: 26].
        """
        if horas <= 0:
            raise ValidationError("Hours must be greater than zero.")
        total = (self.precio_base * horas) - descuento
        return max(total, 0)

    def obtener_descripcion(self):
        return f"Servicio de Sala: {self.nombre} (Precio/Hr: {self.precio_base})"

class ServicioEquipo(Servicio):
    """Specialized service for Equipment Rental[cite: 10, 24]."""
    
    def calcular_costo(self, dias, seguro=10):
        """Calculates cost based on days plus a mandatory insurance fee[cite: 26]."""
        if dias <= 0:
            raise ValidationError("Days must be greater than zero.")
        return (self.precio_base * dias) + seguro

    def obtener_descripcion(self):
        return f"Alquiler de Equipo: {self.nombre} (Precio/Día: {self.precio_base})"

class ServicioAsesoria(Servicio):
    """Specialized service for Specialized Consultancy[cite: 10, 24]."""
    
    def calcular_costo(self, sesiones):
        """Calculates cost based on flat session fees[cite: 24]."""
        if sesiones <= 0:
            raise ValidationError("Sessions must be greater than zero.")
        return self.precio_base * sesiones

    def obtener_descripcion(self):
        return f"Asesoría: {self.nombre} (Precio/Sesión: {self.precio_base})"