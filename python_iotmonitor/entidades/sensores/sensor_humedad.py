from python_iotmonitor.entidades.sensores.sensor_ambiental import SensorAmbiental
from python_iotmonitor.constantes import HUMEDAD_MIN_LECTURA, HUMEDAD_MAX_LECTURA


class SensorHumedad(SensorAmbiental):
    """
    Representa un sensor de humedad relativa del aire (%).
    Hereda de SensorAmbiental e incluye información adicional como modelo o marca.
    """

    def __init__(self, modelo: str, requiere_calibracion: bool = True):
        """
        Inicializa un sensor de humedad.

        Args:
            modelo: Modelo o nombre comercial del sensor.
            requiere_calibracion: Indica si el sensor necesita calibración.
        """
        super().__init__(tipo="Humedad", unidad="%", requiere_calibracion=requiere_calibracion)
        self._modelo = modelo
        self._rango_min = HUMEDAD_MIN_LECTURA
        self._rango_max = HUMEDAD_MAX_LECTURA

    def get_modelo(self) -> str:
        """Devuelve el modelo del sensor."""
        return self._modelo

    def requiere_calibracion(self) -> bool:
        """Devuelve True si el sensor necesita calibración."""
        return super().requiere_calibracion()
