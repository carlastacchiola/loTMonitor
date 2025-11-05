from python_iotmonitor.excepciones.iot_exception import IoTMonitorException
from python_iotmonitor.excepciones.mensajes_exception import MensajesException


class SensorFueraDeRangoException(IoTMonitorException):
    """
    Excepción lanzada cuando un sensor registra un valor fuera del rango permitido.
    Por ejemplo: temperatura excesiva, humedad negativa, o CO₂ fuera de umbral crítico.
    """

    def __init__(self, tipo_sensor: str, valor: float, rango_min: float, rango_max: float):
        """
        Inicializa la excepción.

        Args:
            tipo_sensor: Tipo de sensor (Temperatura, CO2, Humedad, etc.).
            valor: Valor medido que causó el error.
            rango_min: Límite inferior permitido.
            rango_max: Límite superior permitido.
        """
        self._tipo_sensor = tipo_sensor
        self._valor = valor
        self._rango_min = rango_min
        self._rango_max = rango_max

        # Mensaje detallado para logs
        msg = (
            f"Lectura fuera de rango en sensor {tipo_sensor}. "
            f"Valor leído: {valor}, Rango permitido: [{rango_min}, {rango_max}]."
        )

        super().__init__(
            MensajesException.E_02_SENSOR,
            msg,
            MensajesException.MSG_SENSOR_USER
        )

    def get_tipo_sensor(self) -> str:
        """Devuelve el tipo de sensor que causó la excepción."""
        return self._tipo_sensor

    def get_valor(self) -> float:
        """Devuelve el valor leído fuera de rango."""
        return self._valor

    def get_rango_min(self) -> float:
        """Devuelve el límite inferior del rango permitido."""
        return self._rango_min

    def get_rango_max(self) -> float:
        """Devuelve el límite superior del rango permitido."""
        return self._rango_max
