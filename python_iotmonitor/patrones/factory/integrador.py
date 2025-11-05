"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/factory
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/factory/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: sensor_factory.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/factory/sensor_factory.py
# ================================================================================

from typing import Union
from python_iotmonitor.iot_control.sensores.temperatura_reader_task import TemperaturaReaderTask
from python_iotmonitor.iot_control.sensores.humedad_reader_task import HumedadReaderTask

# Alias de tipo: puede expandirse con más sensores en el futuro
TipoSensor = Union[TemperaturaReaderTask, HumedadReaderTask]


class SensorFactory:
    """
    Implementación del patrón Factory Method (US-004).

    Permite crear sensores sin conocer sus clases concretas.
    Mejora la extensibilidad y evita condicionales repetitivos.
    """

    _factories = {
        "Temperatura": TemperaturaReaderTask,
        "Humedad": HumedadReaderTask,
    }

    @staticmethod
    def crear_sensor(tipo: str, id_sensor: int) -> TipoSensor:
        """
        Crea una instancia de sensor según su tipo.

        Args:
            tipo: Tipo del sensor ("Temperatura", "Humedad", etc.)
            id_sensor: Identificador único del sensor.

        Returns:
            Instancia del sensor correspondiente.

        Raises:
            ValueError: Si el tipo no está registrado.
        """
        tipo_normalizado = tipo.strip().capitalize()
        if tipo_normalizado not in SensorFactory._factories:
            raise ValueError(f"Tipo de sensor desconocido: {tipo}")

        clase_sensor = SensorFactory._factories[tipo_normalizado]
        return clase_sensor(id_sensor)


