from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from python_iotmonitor.patrones.strategy.lectura_sensor_strategy import LecturaSensorStrategy

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class SensorService(ABC):
    """
    Clase abstracta base para los servicios de sensores.
    Contiene la inyección del patrón Strategy (US-008, US-010),
    utilizado para calcular lecturas y calibraciones.
    """

    def __init__(self, lectura_strategy: LecturaSensorStrategy):
        self._lectura_strategy = lectura_strategy

    # -----------------------------------------------------------------------
    # Lógica específica de cada sensor
    # -----------------------------------------------------------------------
    @abstractmethod
    def procesar_lectura(self, sensor: "Sensor") -> None:
        """Lógica específica de procesamiento o transformación de lectura."""
        pass

    # -----------------------------------------------------------------------
    # Estrategia de lectura común (Strategy)
    # -----------------------------------------------------------------------
    def aplicar_lectura(self, sensor: "Sensor") -> float:
        """
        Aplica la estrategia de lectura al sensor inyectado.
        Devuelve el valor leído y actualiza el sensor.
        """
        valor_leido = self._lectura_strategy.generar_valor()
        sensor.set_valor_actual(valor_leido)
        return valor_leido

    # -----------------------------------------------------------------------
    # Calibración genérica
    # -----------------------------------------------------------------------
    def calibrar_sensor(self, sensor: "Sensor") -> None:
        """
        Simula la calibración del sensor.
        Este método puede ser sobreescrito por clases concretas.
        """
        print(f"[SensorService] Calibrando sensor {sensor.get_tipo()}...")
        sensor.calibrar()
