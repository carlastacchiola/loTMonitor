from datetime import datetime
from python_iotmonitor.entidades.sensores.sensor import Serializable


class CredencialAcceso(Serializable):
    """
    Representa la credencial de acceso digital de un usuario (US-009, US-010).
    Indica si el usuario tiene permiso activo para operar en el sistema IoTMonitor.
    """

    def __init__(self, activa: bool, fecha_emision: datetime, observaciones: str):
        """
        Inicializa una nueva credencial de acceso.

        Args:
            activa: True si el usuario tiene acceso habilitado.
            fecha_emision: Fecha y hora de emisión o activación.
            observaciones: Detalles o notas adicionales (motivo de alta, caducidad, etc.).
        """
        self._activa = activa
        self._fecha_emision = fecha_emision
        self._observaciones = observaciones

    def esta_activa(self) -> bool:
        """Devuelve True si la credencial está activa."""
        return self._activa

    def get_fecha_emision(self) -> datetime:
        """Devuelve la fecha de emisión de la credencial."""
        return self._fecha_emision

    def get_observaciones(self) -> str:
        """Devuelve las observaciones registradas en la credencial."""
        return self._observaciones
