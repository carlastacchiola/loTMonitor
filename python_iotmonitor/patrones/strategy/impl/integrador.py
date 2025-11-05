"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/impl
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/impl/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: lectura_constante_strategy.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/impl/lectura_constante_strategy.py
# ================================================================================

from enum import Enum
from python_iotmonitor.patrones.strategy.lectura_sensor_strategy import LecturaSensorStrategy


class TipoConstante(Enum):
    HUMEDAD = "Humedad"
    LUZ = "Luz"


class LecturaConstanteStrategy(LecturaSensorStrategy):
    """
    Implementación del patrón Strategy:
    La lectura es constante o dentro de un rango fijo,
    ideal para sensores con baja variación (Humedad, Luz).
    """

    def __init__(self, tipo: TipoConstante):
        self._tipo = tipo

    def generar_valor(self) -> float:
        """
        Genera una lectura constante basada en el tipo de sensor.
        """
        if self._tipo == TipoConstante.HUMEDAD:
            # Simula una humedad ambiente promedio (entre 45–55%)
            return 50.0
        elif self._tipo == TipoConstante.LUZ:
            # Simula una intensidad de luz promedio (entre 400–500 lux)
            return 450.0
        else:
            return 0.0


# ================================================================================
# ARCHIVO 3/3: lectura_variable_strategy.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/impl/lectura_variable_strategy.py
# ================================================================================

from datetime import datetime
from python_iotmonitor.patrones.strategy.lectura_sensor_strategy import LecturaSensorStrategy


class LecturaVariableStrategy(LecturaSensorStrategy):
    """
    Implementación del patrón Strategy:
    La lectura varía según la hora del día o la estación simulada.

    - De día → valores más altos (temperatura, luz, CO₂)
    - De noche → valores más bajos
    """

    def generar_valor(self) -> float:
        """
        Genera un valor de lectura variable basado en la hora actual.
        """
        hora_actual = datetime.now().hour

        # --- Simulación de variación diurna ---
        if 6 <= hora_actual < 18:
            # Día: temperatura/luz altas, CO₂ activo
            return round(20 + (hora_actual - 6) * 0.8, 1)  # Ej. entre 20°C y 30°C
        else:
            # Noche: valores más bajos y estables
            return round(10 + (hora_actual % 6) * 0.5, 1)  # Ej. entre 10°C y 13°C


