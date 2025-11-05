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
