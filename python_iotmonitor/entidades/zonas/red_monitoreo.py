from typing import Optional, TYPE_CHECKING
from python_iotmonitor.entidades.sensores.sensor import Serializable

if TYPE_CHECKING:
    from python_iotmonitor.entidades.zonas.zona import Zona


class RedMonitoreo(Serializable):
    """
    Representa una red de monitoreo ambiental compuesta por una o más zonas (US-001).
    Gestiona información general sobre ubicación, cobertura y sensores activos.
    """

    def __init__(self, id_red: int, ubicacion: str, descripcion: str):
        """
        Inicializa una nueva Red de Monitoreo.

        Args:
            id_red: Identificador único de la red.
            ubicacion: Descripción geográfica o física (ej. “Campus Central”).
            descripcion: Información general o propósito de la red.
        """
        self._id_red = id_red
        self._ubicacion = ubicacion
        self._descripcion = descripcion
        self._zona_principal: Optional['Zona'] = None  # Relación 0..1 con Zona
        self._total_sensores = 0
        self._total_zonas = 0

    # --- Getters básicos ---
    def get_id(self) -> int:
        """Devuelve el ID único de la red de monitoreo."""
        return self._id_red

    def get_ubicacion(self) -> str:
        """Devuelve la ubicación física o geográfica de la red."""
        return self._ubicacion

    def get_descripcion(self) -> str:
        """Devuelve la descripción general de la red."""
        return self._descripcion

    def get_zona_principal(self) -> Optional['Zona']:
        """Devuelve la zona principal de esta red."""
        return self._zona_principal

    def set_zona_principal(self, zona: 'Zona') -> None:
        """Asigna una zona principal a la red."""
        self._zona_principal = zona

    # --- Estadísticas de monitoreo ---
    def get_total_sensores(self) -> int:
        """Devuelve el número total de sensores registrados en la red."""
        return self._total_sensores

    def get_total_zonas(self) -> int:
        """Devuelve la cantidad total de zonas monitoreadas."""
        return self._total_zonas

    def incrementar_sensores(self, cantidad: int) -> None:
        """Incrementa el conteo total de sensores en la red."""
        self._total_sensores += max(0, cantidad)

    def decrementar_sensores(self, cantidad: int) -> None:
        """Decrementa el conteo total de sensores (sin permitir valores negativos)."""
        self._total_sensores = max(0, self._total_sensores - cantidad)

    def incrementar_zonas(self, cantidad: int = 1) -> None:
        """Aumenta el número total de zonas registradas."""
        self._total_zonas += max(0, cantidad)

    def decrementar_zonas(self, cantidad: int = 1) -> None:
        """Disminuye el número total de zonas registradas."""
        self._total_zonas = max(0, self._total_zonas - cantidad)
