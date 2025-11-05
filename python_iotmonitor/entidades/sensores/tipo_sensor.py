from enum import Enum

class TipoSensor(Enum):
    """
    Define los tipos de sensores disponibles en el sistema IoTMonitor.
    Este enum se utiliza por la fábrica de sensores (Factory Method).
    """

    TEMPERATURA = "Temperatura"
    HUMEDAD = "Humedad"
    CO2 = "CO2"
    LUZ = "Luz"
