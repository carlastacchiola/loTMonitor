from python_iotmonitor.excepciones.iot_exception import IoTMonitorException
from python_iotmonitor.excepciones.mensajes_exception import MensajesException


class ZonaNoEncontradaException(IoTMonitorException):
    """
    Excepción lanzada cuando no existe una zona disponible o activa
    para registrar sensores dentro de la red de monitoreo.
    """

    def __init__(self, nombre_zona: str, zonas_disponibles: int):
        """
        Inicializa la excepción.

        Args:
            nombre_zona: Nombre o identificador de la zona buscada.
            zonas_disponibles: Número de zonas actualmente registradas.
        """
        self._nombre_zona = nombre_zona
        self._zonas_disponibles = zonas_disponibles

        # Mensaje de detalle (para logs)
        msg = (
            f"No se encontró la zona '{nombre_zona}' o no hay zonas disponibles. "
            f"Zonas registradas actualmente: {zonas_disponibles}."
        )

        super().__init__(
            MensajesException.E_01_ZONA,
            msg,
            MensajesException.MSG_ZONA_USER
        )

    def get_nombre_zona(self) -> str:
        """Devuelve el nombre o identificador de la zona buscada."""
        return self._nombre_zona

    def get_zonas_disponibles(self) -> int:
        """Devuelve la cantidad de zonas registradas en el sistema."""
        return self._zonas_disponibles
