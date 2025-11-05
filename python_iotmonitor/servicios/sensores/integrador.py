"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 8
"""

# ================================================================================
# ARCHIVO 1/8: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/8: co2_service.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/co2_service.py
# ================================================================================

from typing import TYPE_CHECKING
import random
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.entidades.sensores.sensor import Sensor

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class CO2Service(SensorService):
    """Servicio con lógica específica para sensores de CO₂."""

    def procesar_lectura(self, sensor: "Sensor") -> None:
        """
        Procesa la lectura actual de CO₂ y simula la activación
        de mecanismos de ventilación o alertas (US-008, US-010).
        """
        if sensor.get_tipo().lower() not in ["co2", "dioxido de carbono"]:
            raise TypeError("CO2Service solo puede operar con sensores de tipo 'CO₂'.")

        valor_actual = sensor.get_valor_actual()

        # --- Lógica de reacción ante niveles de CO₂ ---
        if valor_actual > 1000:
            accion = " Nivel crítico — activando ventilación forzada"
        elif valor_actual > 700:
            accion = " Nivel alto — aumentando ventilación"
        else:
            accion = " Nivel normal de CO₂"

        print(f"[CO2Service] Sensor {sensor.get_tipo()} #{sensor.get_id()} → {valor_actual:.1f} ppm ({accion})")

        # --- Simulación adicional ---
        # Cada cierto ciclo, el sensor puede generar una lectura aleatoria de calibración
        if random.random() < 0.1:
            print(f"[CO2Service] Sensor {sensor.get_id()} ejecutó calibración automática.")


# ================================================================================
# ARCHIVO 3/8: humedad_service.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/humedad_service.py
# ================================================================================

from typing import TYPE_CHECKING
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.constantes import HUMEDAD_MAX_RIEGO
from python_iotmonitor.entidades.sensores.sensor import Sensor

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class HumedadService(SensorService):
    """Servicio con lógica específica para sensores de humedad."""

    def procesar_lectura(self, sensor: "Sensor") -> None:
        """
        Procesa la lectura actual del sensor de humedad e identifica
        si deben activarse mecanismos de humidificación o alertas (US-008).
        """
        if sensor.get_tipo().lower() != "humedad":
            raise TypeError("HumedadService solo puede operar con sensores de tipo 'Humedad'.")

        valor_actual = sensor.get_valor_actual()

        # --- Lógica de control ambiental específica ---
        if valor_actual < 20:
            accion = " Activando humidificador (nivel crítico)"
        elif valor_actual < HUMEDAD_MAX_RIEGO:
            accion = " Activando humidificación moderada"
        else:
            accion = " Humedad adecuada"

        print(f"[HumedadService] Sensor {sensor.get_tipo()} #{sensor.get_id()} → {valor_actual:.1f}% ({accion})")


# ================================================================================
# ARCHIVO 4/8: luz_service.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/luz_service.py
# ================================================================================

from typing import TYPE_CHECKING
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.entidades.sensores.sensor import Sensor

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class LuzService(SensorService):
    """Servicio con lógica específica para sensores de luz."""

    def procesar_lectura(self, sensor: "Sensor") -> None:
        """
        Procesa la lectura actual de luz y aplica decisiones automáticas
        sobre iluminación ambiental (US-008, US-010).
        """
        if sensor.get_tipo().lower() not in ["luz", "luminosidad"]:
            raise TypeError("LuzService solo puede operar con sensores de tipo 'Luz'.")

        valor_actual = sensor.get_valor_actual()

        # --- Lógica específica de control lumínico ---
        if valor_actual < 200:
            accion = " Intensificando iluminación (ambiente oscuro)"
        elif valor_actual < 500:
            accion = " Iluminación adecuada"
        else:
            accion = " Ambiente sobreiluminado — reduciendo luz artificial"

        print(f"[LuzService] Sensor {sensor.get_tipo()} #{sensor.get_id()} → {valor_actual:.1f} lux ({accion})")


# ================================================================================
# ARCHIVO 5/8: presion_service.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/presion_service.py
# ================================================================================

from typing import TYPE_CHECKING
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.entidades.sensores.sensor import Sensor

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class PresionService(SensorService):
    """Servicio con lógica específica para sensores de presión atmosférica."""

    def procesar_lectura(self, sensor: "Sensor") -> None:
        """
        Procesa la lectura actual del sensor de presión y aplica
        ajustes o alertas según los valores registrados (US-008).
        """
        if sensor.get_tipo().lower() not in ["presion", "presión"]:
            raise TypeError("PresionService solo puede operar con sensores de tipo 'Presión'.")

        valor_actual = sensor.get_valor_actual()

        # --- Lógica específica: fluctuaciones de presión ---
        if valor_actual < 950:
            estado = " Presión baja — posible tormenta"
        elif valor_actual > 1030:
            estado = " Presión alta — clima estable"
        else:
            estado = " Presión normal"

        print(f"[PresionService] Sensor {sensor.get_tipo()} #{sensor.get_id()} → {valor_actual:.1f} hPa ({estado})")

        # --- Simula “madurez” o recalibración periódica ---
        if hasattr(sensor, "necesita_recalibracion") and sensor.necesita_recalibracion():
            sensor.calibrar()
            print(f"[PresionService] Sensor #{sensor.get_id()} recalibrado automáticamente.")


# ================================================================================
# ARCHIVO 6/8: sensor_service.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/sensor_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 7/8: sensor_service_registry.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/sensor_service_registry.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 8/8: temperatura_service.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/temperatura_service.py
# ================================================================================

from typing import TYPE_CHECKING
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.entidades.sensores.sensor import Sensor

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class TemperaturaService(SensorService):
    """
    Servicio para sensores de temperatura.
    Implementa la lógica de procesamiento y control térmico básico (US-008, US-010).
    """

    def procesar_lectura(self, sensor: "Sensor") -> None:
        """
        Lógica de procesamiento para lecturas de temperatura.
        Aplica ajustes de tendencia térmica según el rango medido.
        """
        if sensor.get_tipo().lower() != "temperatura":
            raise TypeError("TemperaturaService solo puede operar con sensores de tipo 'Temperatura'.")

        valor_actual = sensor.get_valor_actual()

        # Simula un ajuste basado en tendencias térmicas
        if valor_actual < 10:
            accion = "Activando calefacción"
        elif valor_actual > 30:
            accion = "Activando ventilación"
        else:
            accion = "Temperatura estable"

        print(f"[TemperaturaService] {sensor.get_tipo()} #{sensor.get_id()} → {valor_actual:.2f}°C ({accion})")


