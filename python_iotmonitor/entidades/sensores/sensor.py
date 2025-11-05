from abc import ABC, abstractmethod
from typing import Protocol

# Contador simple para IDs únicos de Sensor
_SENSOR_ID_COUNTER = 0


class Serializable(Protocol):
    """Protocolo para indicar que una clase es serializable (Pickle)."""
    pass


class Sensor(ABC, Serializable):
    """
    Clase abstracta base para todos los sensores del sistema IoTMonitor.
    Actúa como interfaz común y garantiza compatibilidad con serialización.
    """

    def __init__(self, tipo: str):
        """
        Inicializa la clase base de Sensor.

        Args:
            tipo: Tipo de sensor (e.g., "Temperatura", "Humedad", "CO2", "Luz").
        """
        global _SENSOR_ID_COUNTER
        _SENSOR_ID_COUNTER += 1

        self._id = _SENSOR_ID_COUNTER
        self._tipo = tipo
        self._valor_actual = None
        self._unidad = ""
        self._activo = True
        self._calibrado = False

    # --- Métodos abstractos para implementación concreta ---
    @abstractmethod
    def get_valor_actual(self) -> float:
        """Devuelve el valor actual leído por el sensor."""
        pass

    @abstractmethod
    def set_valor_actual(self, valor: float) -> None:
        """Actualiza el valor actual leído por el sensor."""
        pass

    # --- Getters y setters comunes ---
    def get_id(self) -> int:
        """Devuelve el ID único del sensor."""
        return self._id

    def get_tipo(self) -> str:
        """Devuelve el tipo del sensor."""
        return self._tipo

    def get_unidad(self) -> str:
        """Devuelve la unidad de medida del sensor."""
        return self._unidad

    def set_unidad(self, unidad: str) -> None:
        """Establece la unidad de medida del sensor (°C, %, ppm, lux, etc.)."""
        self._unidad = unidad

    def esta_activo(self) -> bool:
        """Indica si el sensor está activo."""
        return self._activo

    def activar(self) -> None:
        """Activa el sensor."""
        self._activo = True

    def desactivar(self) -> None:
        """Desactiva el sensor."""
        self._activo = False

    def esta_calibrado(self) -> bool:
        """Devuelve True si el sensor fue calibrado correctamente."""
        return self._calibrado

    def calibrar(self) -> None:
        """Marca el sensor como calibrado."""
        self._calibrado = True
