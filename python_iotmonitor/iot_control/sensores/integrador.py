"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/iot_control/sensores
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/iot_control/sensores/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: humedad_reader_task.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/iot_control/sensores/humedad_reader_task.py
# ================================================================================

import threading
import time
import random
from typing import TYPE_CHECKING
from python_iotmonitor.patrones.observer.observable import Observable
from python_iotmonitor.patrones.observer.eventos.evento_sensor_ambiental import EventoSensorAmbiental
from python_iotmonitor.constantes import (
    INTERVALO_SENSOR_TEMPERATURA, TEMP_MIN_LECTURA, TEMP_MAX_LECTURA,
    INTERVALO_SENSOR_HUMEDAD, HUMEDAD_MIN_LECTURA, HUMEDAD_MAX_LECTURA,
)

if TYPE_CHECKING:
    from python_iotmonitor.patrones.observer.observer import Observer

class HumedadReaderTask(Observable[EventoSensorAmbiental], threading.Thread):
    """Simula lecturas periódicas de humedad ambiental (US-008, US-010)."""

    def __init__(self, id_sensor: int):
        Observable.__init__(self)
        threading.Thread.__init__(self)
        self.id_sensor: int = id_sensor
        self._parar = threading.Event()
        self.name = f"HumedadReaderTask-{self.id_sensor}"
        self._observers: list["Observer[EventoSensorAmbiental]"] = []

    def run(self):
        print(f"[{self.name}] Sensor iniciado. Lectura cada {INTERVALO_SENSOR_HUMEDAD}s.")
        while not self._parar.is_set():
            humedad = round(random.uniform(HUMEDAD_MIN_LECTURA, HUMEDAD_MAX_LECTURA), 1)
            evento = EventoSensorAmbiental("Humedad", humedad, "%", self.id_sensor)
            self.notificar_observers(evento)
            self._parar.wait(INTERVALO_SENSOR_HUMEDAD)

    def parar(self):
        self._parar.set()
        print(f"[{self.name}] Sensor detenido correctamente.")


# ================================================================================
# ARCHIVO 3/3: temperatura_reader_task.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/iot_control/sensores/temperatura_reader_task.py
# ================================================================================

import threading
import time
import random
from typing import TYPE_CHECKING
from python_iotmonitor.patrones.observer.observable import Observable
from python_iotmonitor.patrones.observer.eventos.evento_sensor_ambiental import EventoSensorAmbiental
from python_iotmonitor.constantes import (
    INTERVALO_SENSOR_TEMPERATURA, TEMP_MIN_LECTURA, TEMP_MAX_LECTURA,
    INTERVALO_SENSOR_HUMEDAD, HUMEDAD_MIN_LECTURA, HUMEDAD_MAX_LECTURA,
)

if TYPE_CHECKING:
    from python_iotmonitor.patrones.observer.observer import Observer


class TemperaturaReaderTask(Observable[EventoSensorAmbiental], threading.Thread):
    """Simula lecturas periódicas de temperatura ambiental (US-008, US-010)."""

    def __init__(self, id_sensor: int):
        Observable.__init__(self)
        threading.Thread.__init__(self)
        self.id_sensor: int = id_sensor
        self._parar = threading.Event()
        self.name = f"TempReaderTask-{self.id_sensor}"
        self._observers: list["Observer[EventoSensorAmbiental]"] = []  # para que VS Code lo reconozca

    def run(self):
        print(f"[{self.name}] Sensor iniciado. Lectura cada {INTERVALO_SENSOR_TEMPERATURA}s.")
        while not self._parar.is_set():
            temperatura = round(random.uniform(TEMP_MIN_LECTURA, TEMP_MAX_LECTURA), 1)
            evento = EventoSensorAmbiental("Temperatura", temperatura, "°C", self.id_sensor)
            self.notificar_observers(evento)
            self._parar.wait(INTERVALO_SENSOR_TEMPERATURA)

    def parar(self):
        self._parar.set()
        print(f"[{self.name}] Sensor detenido correctamente.")

