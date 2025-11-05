from abc import ABC
import threading
from python_iotmonitor.entidades.sensores.sensor import Sensor
from python_iotmonitor.constantes import (
    TEMP_MIN_LECTURA, TEMP_MAX_LECTURA,
    HUMEDAD_MIN_LECTURA, HUMEDAD_MAX_LECTURA,
    CO2_MIN_LECTURA, CO2_MAX_LECTURA,
    LUZ_MIN_LECTURA, LUZ_MAX_LECTURA
)


class SensorBase(Sensor, ABC):
    """
    Clase base abstracta para todos los sensores del sistema IoTMonitor.
    Provee manejo común de ID, valor actual, unidad de medida y seguridad en hilos.
    """
    _id_counter = 0

    def __init__(self, tipo: str, unidad: str, rango_min: float, rango_max: float):
        """
        Inicializa un nuevo sensor base.

        Args:
            tipo: Tipo de sensor (Temperatura, Humedad, CO2, Luz).
            unidad: Unidad de medida (°C, %, ppm, lux).
            rango_min: Valor mínimo esperado de medición.
            rango_max: Valor máximo esperado de medición.
        """
        super().__init__(tipo)
        SensorBase._id_counter += 1
        self._id = SensorBase._id_counter
        self._unidad = unidad
        self._rango_min = rango_min
        self._rango_max = rango_max
        self._valor_actual = None
        self._lock = threading.Lock()

    # --- Getters básicos ---
    def get_id(self) -> int:
        """Devuelve el ID único del sensor."""
        return self._id

    def get_tipo(self) -> str:
        """Devuelve el tipo de sensor."""
        return self._tipo

    def get_unidad(self) -> str:
        """Devuelve la unidad de medida del sensor."""
        return self._unidad

    def get_rango(self) -> tuple:
        """Devuelve el rango de medición del sensor."""
        return self._rango_min, self._rango_max

    def get_valor_actual(self) -> float:
        """Devuelve el último valor leído del sensor."""
        return self._valor_actual

    # --- Setters seguros ---
    def set_valor_actual(self, valor: float) -> None:
        """
        Actualiza el valor actual del sensor (Thread-safe).
        Asegura que el valor quede dentro de su rango válido.
        """
        with self._lock:
            valor_limitado = max(self._rango_min, min(valor, self._rango_max))
            self._valor_actual = valor_limitado

    # --- Métodos de persistencia ---
    def __getstate__(self):
        """Devuelve el estado serializable del sensor, excluyendo el lock."""
        state = self.__dict__.copy()
        del state['_lock']
        return state

    def __setstate__(self, state):
        """Restaura el estado del sensor al deserializar e inicializa un nuevo lock."""
        self.__dict__.update(state)
        self._lock = threading.Lock()
