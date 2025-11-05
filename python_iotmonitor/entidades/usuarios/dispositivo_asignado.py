from python_iotmonitor.entidades.sensores.sensor import Serializable


class DispositivoAsignado(Serializable):
    """
    Entidad que representa un dispositivo o módulo asignado a un usuario.
    
    Asegura que solo se puedan usar dispositivos verificados y certificados
    por el sistema IoTMonitor (US-009, US-010).
    """

    def __init__(self, id_dispositivo: int, nombre: str, verificado: bool):
        """
        Inicializa un nuevo dispositivo asignado.

        Args:
            id_dispositivo: Identificador único del dispositivo.
            nombre: Nombre o modelo del dispositivo (e.g., "Sensor DHT11", "Módulo ESP32").
            verificado: Booleano que indica si el dispositivo pasó la verificación técnica.
        
        Raises:
            ValueError: Si el dispositivo no está verificado por el sistema.
        """
        if not verificado:
            raise ValueError(
                f"El dispositivo '{nombre}' (ID: {id_dispositivo}) debe estar verificado "
                "técnicamente para ser registrado en el sistema."
            )

        self._id = id_dispositivo
        self._nombre = nombre
        self._verificado = verificado

    def get_id(self) -> int:
        """Devuelve el identificador único del dispositivo."""
        return self._id

    def get_nombre(self) -> str:
        """Devuelve el nombre o modelo del dispositivo."""
        return self._nombre

    def esta_verificado(self) -> bool:
        """Indica si el dispositivo está verificado técnicamente."""
        return self._verificado
