from python_iotmonitor.entidades.sensores.sensor_base import SensorBase
from python_iotmonitor.constantes import CO2_MIN_LECTURA, CO2_MAX_LECTURA


class SensorCO2(SensorBase):
    """
    Representa un sensor de dióxido de carbono (CO₂) en ppm.
    Hereda de SensorBase y añade atributos específicos de control de calidad del aire.
    """

    def __init__(self, modelo: str, nivel_alarma: float = 1200.0):
        """
        Inicializa un sensor de CO₂.

        Args:
            modelo: Modelo o nombre comercial del sensor.
            nivel_alarma: Nivel de concentración en ppm a partir del cual se activa una alerta.
        """
        super().__init__(tipo="CO2", unidad="ppm", rango_min=CO2_MIN_LECTURA, rango_max=CO2_MAX_LECTURA)
        self._modelo = modelo
        self._nivel_alarma = nivel_alarma
        self._alertas_activadas = 0

    def get_modelo(self) -> str:
        """Devuelve el modelo del sensor."""
        return self._modelo

    def get_nivel_alarma(self) -> float:
        """Devuelve el nivel de alarma configurado para el sensor."""
        return self._nivel_alarma

    def set_nivel_alarma(self, valor: float) -> None:
        """Actualiza el nivel de alarma para este sensor."""
        self._nivel_alarma = max(self._rango_min, min(valor, self._rango_max))

    def registrar_alerta(self) -> None:
        """Incrementa el contador de alertas activadas."""
        self._alertas_activadas += 1

    def get_alertas_activadas(self) -> int:
        """Devuelve la cantidad de veces que se activó una alerta por exceso de CO₂."""
        return self._alertas_activadas
