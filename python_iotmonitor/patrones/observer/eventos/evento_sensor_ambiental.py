from datetime import datetime


class EventoSensorAmbiental:
    """
    Clase que encapsula la información emitida por un sensor ambiental.
    Representa un evento dentro del sistema IoTMonitor.
    """

    def __init__(self, tipo: str, valor: float, unidad: str, id_sensor: int):
        """
        Inicializa un nuevo evento ambiental.

        Args:
            tipo: Tipo de sensor (Temperatura, Humedad, CO₂, Luz, etc.).
            valor: Valor leído por el sensor.
            unidad: Unidad de medida (°C, %, ppm, lux, etc.).
            id_sensor: Identificador único del sensor emisor.
        """
        self.timestamp = datetime.now()
        self.tipo_sensor = tipo
        self.valor = valor
        self.unidad = unidad
        self.id_sensor = id_sensor

    def __str__(self):
        """Devuelve una representación legible del evento."""
        return (
            f"[{self.tipo_sensor} #{self.id_sensor} @ "
            f"{self.timestamp.strftime('%H:%M:%S')}] → {self.valor}{self.unidad}"
        )
