from datetime import datetime
from python_iotmonitor.entidades.sensores.sensor import Serializable
from python_iotmonitor.entidades.usuarios.dispositivo_asignado import DispositivoAsignado


class TareaUsuario(Serializable):
    """
    Representa una tarea asignada a un usuario del sistema (US-009, US-010).
    Cada tarea puede estar vinculada a un dispositivo o sensor específico.
    """

    def __init__(self, id_tarea: int, descripcion: str, fecha_asignada: datetime, dispositivo: DispositivoAsignado):
        """
        Inicializa una nueva tarea de usuario.

        Args:
            id_tarea: Identificador único de la tarea.
            descripcion: Descripción breve de la tarea asignada.
            fecha_asignada: Fecha en la que se asignó la tarea.
            dispositivo: Dispositivo o sensor vinculado a la tarea.
        """
        self._id = id_tarea
        self._descripcion = descripcion
        self._fecha_asignada = fecha_asignada
        self._completada = False
        self._dispositivo = dispositivo

    # --- Getters básicos ---
    def get_id(self) -> int:
        """Devuelve el ID único de la tarea."""
        return self._id

    def get_descripcion(self) -> str:
        """Devuelve la descripción de la tarea."""
        return self._descripcion

    def get_fecha_asignada(self) -> datetime:
        """Devuelve la fecha en la que se asignó la tarea."""
        return self._fecha_asignada

    def esta_completada(self) -> bool:
        """Indica si la tarea ya ha sido completada."""
        return self._completada

    def set_completada(self, estado: bool) -> None:
        """Marca la tarea como completada (o pendiente)."""
        self._completada = estado

    # --- Dispositivo asociado ---
    def get_dispositivo(self) -> DispositivoAsignado:
        """Devuelve el dispositivo vinculado a esta tarea."""
        return self._dispositivo
