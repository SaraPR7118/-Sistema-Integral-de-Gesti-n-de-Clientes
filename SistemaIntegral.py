import logging
from abc import ABC, abstractmethod
from datetime import datetime

#Phase 1: Exceptions, Logging, and Base Abstractions
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
    
    #Phase 2: The Cliente Class
class Cliente(Entity):
    """
    Represents a client with robust data validation and encapsulation.
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
    
    #Phase 3: Specialized Services (Polymorphism)
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base
    
    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass
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
    
    #Phase 4: The Reserva Class
    
class Reserva:
    """
    Integrates Cliente and Servicio. Manages duration and status.
    Demonstrates advanced exception handling (else/finally/chaining).
    """
    def __init__(self, id_reserva, cliente, servicio, duracion):
        # Validation: Duration must be positive
        if duracion <= 0:
            raise ValidationError("Duration must be a positive number.")
            
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"
        self.costo_total = 0

    def procesar_confirmacion(self, **kwargs):
        """
        Confirms the reservation and calculates costs.
        Uses try/except/else/finally and exception chaining.
        """
        print(f"\n--- Procesando Reserva #{self.id_reserva} ---")
        try:
            # We attempt to calculate the cost based on the specific service type
            # Requirement: Polymorphism in action [cite: 24]
            self.costo_total = self.servicio.calcular_costo(self.duracion, **kwargs)
            
        except ValidationError as ve:
            # Exception Chaining: Raising a new exception while preserving context [cite: 17]
            logging.error(f"Error en validación de Reserva {self.id_reserva}: {ve}")
            raise ReservationError("No se pudo confirmar la reserva por datos inválidos.") from ve
            
        except Exception as e:
            # Catch-all for unexpected errors to maintain system stability [cite: 11, 19]
            logging.critical(f"Error inesperado en Reserva {self.id_reserva}: {e}")
            raise SoftwareFJError("Error crítico interno del sistema.") from e
            
        else:
            # Executes only if no exception was raised [cite: 17]
            self.estado = "CONFIRMADA"
            print(f"Éxito: Reserva confirmada para {self.cliente.nombre}.")
            print(f"Servicio: {self.servicio.obtener_descripcion()}")
            print(f"Total a pagar: ${self.costo_total}")
            
        finally:
            # Always executes, regardless of success or failure [cite: 17]
            print(f"Finalización del proceso de registro para ID: {self.id_reserva}")

    def __str__(self):
        return f"Reserva {self.id_reserva} - {self.estado} - Cliente: {self.cliente.nombre}"
    
# Ohase 5: Controlador de Simulaciones 

def ejecutar_simulaciones():
    """
    Ejecuta al menos 10 operaciones para demostrar estabilidad y manejo de errores.
    Requisito: Simulación sin base de datos (uso de listas volátiles).
    """
    
    # Listas internas que actúan como almacenamiento volátil
    listado_clientes = []
    listado_reservas = []
    
    print("\n" + "="*50)
    print("=== INICIANDO SIMULACIÓN SISTEMA SOFTWARE FJ ===")
    print("="*50)

    # 1. Registro Válido de Cliente
    try:
        c1 = Cliente(101, "Juan Perez", "juan@unad.edu.co")
        listado_clientes.append(c1)
        print("Operación 1 (OK): Cliente registrado.")
    except Exception as e:
        print(f"Operación 1 (Error): {e}")

    # 2. Registro Inválido de Cliente (Nombre corto - Provoca ValidationError)
    try:
        c2 = Cliente(102, "Jo", "error@test.com") # Esto fallará intencionalmente
    except ValidationError as e:
        logging.warning(f"Simulación 2 detectó error esperado: {e}")
        print(f"Operación 2 (OK - Error capturado): {e}")

    # 3. Creación de Servicio de Sala
    # Importante: La clase ServicioSala debe estar definida arriba en el archivo
    sala_conferencias = ServicioSala("Sala Magna", 50) 
    print("Operación 3 (OK): Servicio de sala creado.")

    # 4. Reserva Exitosa (Sala)
    try:
        # Requiere que listado_clientes[0] exista (creado en Operación 1)
        r1 = Reserva("R-001", listado_clientes[0], sala_conferencias, 4)
        r1.procesar_confirmacion(descuento=10) # Parámetro opcional (sobrecarga)
        listado_reservas.append(r1)
    except Exception as e:
        print(f"Operación 4 (Error): {e}")

    # 5. Reserva Fallida (Duración negativa - Provoca ValidationError)
    try:
        r2 = Reserva("R-002", listado_clientes[0], sala_conferencias, -2)
        r2.procesar_confirmacion()
    except ValidationError as e:
        print(f"Operación 5 (OK - Error capturado): {e}")
    except NameError:
        print("Operación 5 (Error): La clase 'Reserva' no está definida antes de esta función.")

    # 6. Creación de Servicio de Asesoría
    asesoria_it = ServicioAsesoria("Consultoría Python", 100)
    print("Operación 6 (OK): Servicio de asesoría creado.")

    # 7. Reserva Exitosa (Asesoría)
    try:
        r3 = Reserva("R-003", listado_clientes[0], asesoria_it, 2)
        r3.procesar_confirmacion()
        listado_reservas.append(r3)
    except Exception as e:
        print(f"Operación 7 (Error): {e}")

    # 8. Registro de Cliente con Email Inválido (Falta @)
    try:
        c3 = Cliente(103, "Ana Garcia", "anagarcia_at_provider.com") 
    except ValidationError as e:
        print(f"Operación 8 (OK - Error capturado): {e}")

    # 9. Creación de Servicio de Equipo
    laptop = ServicioEquipo("Laptop Gamer", 30)
    print("Operación 9 (OK): Servicio de equipo creado.")

    # 10. Reserva con error de tipo (Simulando error crítico)
    try:
        r4 = Reserva("R-004", listado_clientes[0], laptop, 3)
        # Pasamos un string donde se espera un número para forzar el catch de Exception
        r4.procesar_confirmacion(seguro="Texto no numérico") 
    except Exception as e:
        print(f"Operación 10 (OK - Error crítico manejado y registrado): {e}")

    print("\n" + "="*50)
    print("=== RESUMEN DE RESERVAS PROCESADAS ===")
    print("="*50)
    if not listado_reservas:
        print("No se confirmaron reservas.")
    for res in listado_reservas:
        print(res)
    #Phase 6: Final Simulation Execution and Entry Point
    
    # --- MAIN EXECUTION POINT ---
# Requirement: A single functional project capable of executing without interruptions[cite: 33].

if __name__ == "__main__":
    try:
        # We trigger the 10-operation simulation defined in Phase 5
        ejecutar_simulaciones()
        
    except Exception as fatal_error:
        # This is the last line of defense
        # Every error must be logged 
        logging.critical(f"CRITICAL SYSTEM FAILURE: {fatal_error}")
        print(f"El sistema ha encontrado un error fatal inesperado: {fatal_error}")
        
    else:
        print("\n" + "="*40)
        print("SIMULACIÓN FINALIZADA CON ÉXITO")
        print(f"Revise 'system_errors.log' para ver el registro de eventos.")
        print("="*40)
        
    finally:
        # Ensures the program gracefully notifies the user it is closing
        print("Cerrando el sistema Software FJ...")