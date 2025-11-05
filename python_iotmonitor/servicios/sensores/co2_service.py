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
