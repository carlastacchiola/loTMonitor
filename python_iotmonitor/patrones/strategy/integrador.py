"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: lectura_sensor_strategy.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/lectura_sensor_strategy.py
# ================================================================================

from abc import ABC, abstractmethod

class LecturaSensorStrategy(ABC):
    """
    Interfaz base del patrón Strategy para generar lecturas de sensores.
    (US-010)
    """

    @abstractmethod
    def generar_valor(self) -> float:
        """
        Genera un valor de lectura simulado o calculado para un sensor,
        dependiendo de su tipo (temperatura, humedad, CO₂, luz, etc.).
        """
        pass


