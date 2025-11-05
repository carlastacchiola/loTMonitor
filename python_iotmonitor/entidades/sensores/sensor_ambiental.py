from abc import ABC
import threading
from python_iotmonitor.entidades.sensores.sensor import Sensor


class SensorAmbiental(Sensor, ABC):
    """
    Clase base abstracta para sensores ambientales del sistema IoTMonitor.
    Provee control thread-safe sobre los valores leídos y define si requieren calibración ambiental.
    """

    def __init__(self, tipo: str, unidad: str, requiere_calibracion: bool = True):
        """
        Inicializa un sensor ambiental.

        Args:
            tipo: Tipo de sensor (Temperatura, Humedad, CO2, Luz, etc.).
            unidad: Unidad de medida del sensor.
            requiere_calibracion: Indica si el sensor necesita calibración inicial.
        """
        super().__init__(tipo)
        self._unidad = unidad
        self._requiere_calibracion = requiere_calibracion
        self._valor_actual = 0.0
        self._lock = threading.Lock()

    # --- Métodos thread-safe ---
    def get_valor_actual(self) -> float:
        """Devuelve el valor actual leído por el sensor (Thread-safe)."""
        with self._lock:
            return self._valor_actual

    def set_valor_actual(self, valor: float) -> None:
        """
        Actualiza el valor del sensor (Thread-safe).
        Asegura que no se asignen valores negativos o nulos inesperados.
        """
        with self._lock:
            self._valor_actual = max(0.0, valor)

    # --- Métodos de persistencia ---
    def __getstate__(self):
        """Devuelve el estado del sensor a serializar, excluyendo el lock."""
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state):
        """Restaura el estado del sensor al deserializar e inicializa un nuevo lock."""
        self.__dict__.update(state)
        self._lock = threading.Lock()

    # --- Métodos adicionales ---
    def requiere_calibracion(self) -> bool:
        """
        Devuelve True si el sensor requiere calibración ambiental.
        """
        return self._requiere_calibracion
