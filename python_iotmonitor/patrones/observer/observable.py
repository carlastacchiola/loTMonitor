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
