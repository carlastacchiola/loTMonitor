from typing import TYPE_CHECKING
from python_iotmonitor.entidades.sensores.sensor import Serializable

# Evitamos dependencias circulares entre Zona y RedMonitoreo
if TYPE_CHECKING:
    from python_iotmonitor.entidades.zonas.red_monitoreo import RedMonitoreo
    from python_iotmonitor.entidades.zonas.zona import Zona


class RegistroAmbiental(Serializable):
    """
    Clase que encapsula los datos administrativos y técnicos
    de una instalación de monitoreo ambiental (US-003, US-012).
    """

    def __init__(self, id_instalacion: int, red: 'RedMonitoreo', zona: 'Zona', responsable: str, prioridad: int):
        """
        Inicializa un nuevo registro ambiental.

        Args:
            id_instalacion: Identificador único del registro o instalación.
            red: Red de monitoreo asociada.
            zona: Zona incluida dentro de la red.
            responsable: Nombre del técnico o responsable de la instalación.
            prioridad: Nivel de prioridad de la zona (1 = alta, 2 = media, 3 = baja).
        """
        self._id_instalacion = id_instalacion
        self._red = red
        self._zona = zona
        self._responsable = responsable
        self._prioridad = prioridad

    def get_id(self) -> int:
        """Devuelve el ID único del registro ambiental."""
        return self._id_instalacion

    def get_red(self) -> 'RedMonitoreo':
        """Devuelve la red asociada al registro."""
        return self._red

    def get_zona(self) -> 'Zona':
        """Devuelve la zona asociada al registro."""
        return self._zona

    def get_responsable(self) -> str:
        """Devuelve el nombre del técnico responsable."""
        return self._responsable

    def get_prioridad(self) -> int:
        """Devuelve el nivel de prioridad de la zona."""
        return self._prioridad
