"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/singleton
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/singleton/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: sensor_registry.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/singleton/sensor_registry.py
# ================================================================================

from threading import Lock
from typing import Dict


class SensorRegistry:
    """
    Singleton que mantiene un registro global de sensores activos.
    (US-008)

    Permite registrar, obtener y listar sensores del sistema IoTMonitor.
    Garantiza que solo exista una única instancia de registro.
    """

    _instance = None
    _lock = Lock()

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._sensors: Dict[int, object] = {}
        self._initialized = True

    # -------------------------------------------------------------------------
    # Método Singleton
    # -------------------------------------------------------------------------
    @classmethod
    def get_instance(cls) -> "SensorRegistry":
        """Devuelve la única instancia del registro de sensores."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # doble chequeo
                    cls._instance = cls()
        return cls._instance

    # -------------------------------------------------------------------------
    # Métodos de gestión
    # -------------------------------------------------------------------------
    def registrar_sensor(self, id_sensor: int, sensor: object) -> None:
        """Registra un nuevo sensor en el sistema."""
        if id_sensor in self._sensors:
            print(f"[SensorRegistry] Sensor #{id_sensor} ya registrado.")
        else:
            self._sensors[id_sensor] = sensor
            print(f"[SensorRegistry] Sensor #{id_sensor} agregado correctamente.")

    def obtener_sensor(self, id_sensor: int) -> object:
        """Devuelve el sensor correspondiente al ID."""
        return self._sensors.get(id_sensor)

    def listar_sensores(self) -> Dict[int, object]:
        """Devuelve un diccionario con todos los sensores registrados."""
        return dict(self._sensors)


