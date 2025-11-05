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
