import threading
import time
from typing import TYPE_CHECKING
from python_iotmonitor.patrones.observer.observer import Observer
from python_iotmonitor.patrones.observer.eventos.evento_sensor_ambiental import EventoSensorAmbiental
from python_iotmonitor.constantes import (CONTROL_AMBIENTAL_CICLO_SEGUNDOS)

if TYPE_CHECKING:
    from python_iotmonitor.servicios.sensores.sensor_service_registry import SensorServiceRegistry
    from python_iotmonitor.entidades.zonas.zona import Zona


class ControlAmbientalTask(threading.Thread, Observer[EventoSensorAmbiental]):
    """
    Controlador Ambiental principal del sistema IoTMonitor.
    Actúa como hilo concurrente y observador de eventos de sensores.

    Se encarga de mantener condiciones ambientales estables reaccionando
    a los cambios en temperatura, humedad, CO₂ y luz.
    """

    def __init__(self, zona: "Zona", sensor_registry: "SensorServiceRegistry"):
        super().__init__()
        self.zona = zona
        self.sensor_registry = sensor_registry
        self._parar = threading.Event()
        self.name = f"ControlAmbientalThread-{zona.get_id_zona()}"
        self._lock = threading.Lock()

        # Últimos valores registrados
        self._ultima_temperatura = 0.0
        self._ultima_humedad = 50.0
        self._ultimo_co2 = 400.0
        self._ultima_luz = 250.0

    # -----------------------------------------------------------------------
    # Ciclo principal
    # -----------------------------------------------------------------------
    def run(self):
        """Inicia el ciclo continuo de monitoreo ambiental."""
        print(f"[{self.name}] Control ambiental iniciado.")
        while not self._parar.is_set():
            try:
                self._aplicar_control_ambiental()
            except Exception as e:
                print(f"[{self.name}]  Error en control ambiental: {e}")

            self._parar.wait(CONTROL_AMBIENTAL_CICLO_SEGUNDOS)

        print(f"[{self.name}] Control ambiental detenido.")

    # -----------------------------------------------------------------------
    # Observador de sensores
    # -----------------------------------------------------------------------
    def actualizar(self, evento: EventoSensorAmbiental) -> None:
        """Recibe notificaciones de los sensores y actualiza sus últimas lecturas."""
        with self._lock:
            if evento.tipo_sensor == "Temperatura":
                self._ultima_temperatura = evento.valor
            elif evento.tipo_sensor == "Humedad":
                self._ultima_humedad = evento.valor
            elif evento.tipo_sensor == "CO2":
                self._ultimo_co2 = evento.valor
            elif evento.tipo_sensor == "Luz":
                self._ultima_luz = evento.valor

    # -----------------------------------------------------------------------
    # Lógica de control ambiental
    # -----------------------------------------------------------------------
    def _aplicar_control_ambiental(self):
        """
        Evalúa las condiciones actuales y ejecuta acciones automáticas.
        Aplica estrategias de enfriamiento, ventilación, humidificación y ajuste de luz.
        """
        with self._lock:
            T = self._ultima_temperatura
            H = self._ultima_humedad
            C = self._ultimo_co2
            L = self._ultima_luz

        print(
            f"[{self.name}] Estado actual → T:{T}°C | H:{H}% | CO₂:{C}ppm | L:{L}lux"
        )

        # --- Temperatura (Strategy Enfriar / Calentar) ---
        if T < 8:
            print(" Activando calefacción ambiental...")
        elif T > 28:
            print(" Activando ventilación y enfriamiento...")

        # --- Humedad (Strategy Humidificar) ---
        if H < 40:
            print(" Activando humidificador...")
        elif H > 80:
            print(" Deshumidificando ambiente...")

        # --- CO₂ (Strategy Ventilar) ---
        if C > 900:
            print(" Nivel crítico de CO₂ — ventilación forzada activada.")
        elif C > 600:
            print(" Nivel alto de CO₂ — ventilación moderada.")

        # --- Luz (Strategy AjustarLuz) ---
        if L < 200:
            print(" Encendiendo luces automáticas.")
        elif L > 700:
            print(" Ambiente sobreiluminado — reduciendo luz artificial.")

    def parar(self):
        """Detiene el hilo de control ambiental de forma segura."""
        self._parar.set()
