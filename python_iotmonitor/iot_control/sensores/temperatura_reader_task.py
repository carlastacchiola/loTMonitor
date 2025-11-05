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