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
