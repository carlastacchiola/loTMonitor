"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: observable.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/observable.py
# ================================================================================

from typing import TypeVar, Generic, List, TYPE_CHECKING
import threading

T = TypeVar("T")

if TYPE_CHECKING:
    from python_iotmonitor.patrones.observer.observer import Observer


class Observable(Generic[T]):
    """
    Clase base genérica para objetos que emiten notificaciones (patrón Observer).

    En el sistema PythonIoTMonitor, los observables suelen ser:
      - Sensores (TemperaturaReaderTask, HumedadReaderTask)
      - Módulos que generan eventos ambientales (CO₂, luz, etc.)

    Los observadores pueden ser:
      - ControlAmbientalTask
      - Sistemas de registro o alarmas
    """

    def __init__(self):
        self._observers: List["Observer[T]"] = []
        self._lock = threading.Lock()  # Asegura la concurrencia

    # -----------------------------------------------------------------------
    # Registro / eliminación de observadores
    # -----------------------------------------------------------------------
    def agregar_observer(self, observer: "Observer[T]") -> None:
        """Agrega un nuevo observador si aún no está registrado."""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def remover_observer(self, observer: "Observer[T]") -> None:
        """Elimina un observador del registro."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    # -----------------------------------------------------------------------
    # Notificación de eventos
    # -----------------------------------------------------------------------
    def notificar_observers(self, evento: T) -> None:
        """
        Notifica a todos los observadores registrados con un evento específico.

        Args:
            evento: Instancia del evento generado (por ejemplo, EventoSensorAmbiental).
        """
        # Se notifica sin lock para evitar deadlocks si el observador hace tareas pesadas
        for observer in list(self._observers):
            observer.actualizar(evento)


# ================================================================================
# ARCHIVO 3/3: observer.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/observer.py
# ================================================================================

from typing import Protocol, TypeVar, Generic

T = TypeVar("T")

class Observer(Generic[T], Protocol):
    """
    Interfaz genérica del patrón Observer.
    Define el contrato que deben cumplir todos los observadores de eventos.

    En el contexto de PythonIoTMonitor, los observadores pueden ser:
    - ControlAmbientalTask (observador principal)
    - Servicios automáticos de monitoreo
    - Sistemas de alerta
    """

    def actualizar(self, evento: T) -> None:
        """
        Método llamado por el Observable para notificar un nuevo evento.

        Args:
            evento: Instancia del evento emitido (por ejemplo, EventoSensorAmbiental).
        """
        ...


