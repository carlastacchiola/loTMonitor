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
