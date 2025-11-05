from python_iotmonitor.entidades.sensores.sensor_base import SensorBase
from python_iotmonitor.constantes import TEMP_MIN_LECTURA, TEMP_MAX_LECTURA


class SensorTemperatura(SensorBase):
    """
    Representa un sensor de temperatura ambiental (°C).
    Hereda de SensorBase e incluye información del modelo y control de lecturas acumuladas.
    """

    def __init__(self, modelo: str):
        """
        Inicializa un sensor de temperatura.

        Args:
            modelo: Modelo o tipo de sensor (ej. DHT11, LM35, DS18B20).
        """
        super().__init__(tipo="Temperatura", unidad="°C", rango_min=TEMP_MIN_LECTURA, rango_max=TEMP_MAX_LECTURA)
        self._modelo = modelo
        self._lecturas_acumuladas = 0.0
        self._cantidad_lecturas = 0

    def get_modelo(self) -> str:
        """Devuelve el modelo o tipo de sensor."""
        return self._modelo

    def registrar_lectura(self, valor: float) -> None:
        """
        Registra una nueva lectura de temperatura y actualiza el promedio acumulado.

        Args:
            valor: Valor medido en grados Celsius.
        """
        self.set_valor_actual(valor)
        self._lecturas_acumuladas += valor
        self._cantidad_lecturas += 1

    def get_promedio_lecturas(self) -> float:
        """Devuelve el promedio de todas las lecturas registradas."""
        if self._cantidad_lecturas == 0:
            return 0.0
        return round(self._lecturas_acumuladas / self._cantidad_lecturas, 2)
