from typing import Dict
from python_iotmonitor.patrones.strategy.impl.lectura_variable_strategy import LecturaVariableStrategy
from python_iotmonitor.patrones.strategy.impl.lectura_constante_strategy import LecturaConstanteStrategy, TipoConstante
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.servicios.sensores.temperatura_service import TemperaturaService
from python_iotmonitor.servicios.sensores.humedad_service import HumedadService
from python_iotmonitor.servicios.sensores.co2_service import CO2Service
from python_iotmonitor.servicios.sensores.luz_service import LuzService


class SensorServiceRegistry:
    """
    Patrón Registry implementado como Singleton (US-TECH-005).
    Mapea el tipo de sensor a su Service correspondiente con la Strategy inyectada.
    """
    _instance: "SensorServiceRegistry" = None
    _registry: Dict[str, SensorService] = {}

    def __new__(cls):
        """Implementa Singleton simple (sin locks, suficiente en Python)."""
        if cls._instance is None:
            cls._instance = super(SensorServiceRegistry, cls).__new__(cls)
            cls._instance._inicializar_registro()
        return cls._instance

    # -----------------------------------------------------------------------
    # Inicialización de servicios con sus estrategias respectivas
    # -----------------------------------------------------------------------
    def _inicializar_registro(self):
        """Inicializa los servicios y asocia estrategias de lectura adecuadas."""

        # Strategy Variable para sensores dinámicos (temperatura, CO₂)
        variable_strategy = LecturaVariableStrategy()
        self._registry["Temperatura"] = TemperaturaService(lectura_strategy=variable_strategy)
        self._registry["CO2"] = CO2Service(lectura_strategy=variable_strategy)

        # Strategy Constante para sensores estables (humedad, luz)
        constante_humedad = LecturaConstanteStrategy(TipoConstante.HUMEDAD)
        constante_luz = LecturaConstanteStrategy(TipoConstante.LUZ)
        self._registry["Humedad"] = HumedadService(lectura_strategy=constante_humedad)
        self._registry["Luz"] = LuzService(lectura_strategy=constante_luz)

    # -----------------------------------------------------------------------
    # Acceso público
    # -----------------------------------------------------------------------
    def get_service(self, tipo_sensor: str) -> SensorService:
        """
        Obtiene el servicio de sensor según su tipo.
        
        Args:
            tipo_sensor: Tipo textual del sensor (Temperatura, CO2, etc.).

        Raises:
            ValueError: Si no existe un servicio para ese tipo de sensor.
        """
        tipo_normalizado = tipo_sensor.strip().capitalize()
        service = self._registry.get(tipo_normalizado)

        if service is None:
            raise ValueError(f"Servicio no encontrado para el tipo de sensor: {tipo_sensor}")

        return service
