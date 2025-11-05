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
