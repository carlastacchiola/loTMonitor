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
