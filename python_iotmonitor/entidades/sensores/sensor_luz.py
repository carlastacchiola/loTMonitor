from python_iotmonitor.entidades.sensores.sensor_ambiental import SensorAmbiental
from python_iotmonitor.constantes import LUZ_MIN_LECTURA, LUZ_MAX_LECTURA


class SensorLuz(SensorAmbiental):
    """
    Representa un sensor de luminosidad (lux) dentro del sistema IoTMonitor.
    Puede instalarse en interior o exterior.
    """

    def __init__(self, es_interior: bool = True):
        """
        Inicializa un sensor de luz.

        Args:
            es_interior: True si el sensor está instalado en interior, False si está al aire libre.
        """
        super().__init__(tipo="Luz", unidad="lux", requiere_calibracion=False)
        self._es_interior = es_interior
        self._rango_min = LUZ_MIN_LECTURA
        self._rango_max = LUZ_MAX_LECTURA

    def es_interior(self) -> bool:
        """Devuelve True si el sensor está instalado en interior."""
        return self._es_interior

    def set_es_interior(self, interior: bool) -> None:
        """Establece si el sensor está instalado en interior o exterior."""
        self._es_interior = interior
