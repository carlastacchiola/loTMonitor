from enum import Enum
from python_iotmonitor.excepciones.iot_exception import IoTMonitorException
from python_iotmonitor.excepciones.mensajes_exception import MensajesException


class TipoOperacion(Enum):
    """Define los tipos de operaciones de persistencia."""
    LECTURA = "LECTURA"
    ESCRITURA = "ESCRITURA"


class PersistenciaException(IoTMonitorException):
    """
    Excepción lanzada durante operaciones de persistencia del sistema (serialización / deserialización).
    Puede generarse al guardar o leer archivos de datos (.dat).
    """

    def __init__(self, tipo_operacion: TipoOperacion, nombre_archivo: str, causa_raiz: Exception, error_code: str):
        self._tipo_operacion = tipo_operacion
        self._nombre_archivo = nombre_archivo

        # Mensaje técnico para logs
        msg = (
            f"Error de {tipo_operacion.value} en archivo '{nombre_archivo}'. "
            f"Causa: {causa_raiz.__class__.__name__}: {str(causa_raiz)}"
        )

        # Mensaje amigable para usuario
        user_msg = MensajesException.MSG_PERSISTENCIA_USER.format(error_code)

        super().__init__(error_code, msg, user_msg)

    # --- Métodos de fábrica ---
    @classmethod
    def from_io_exception(cls, tipo_operacion: TipoOperacion, nombre_archivo: str, causa: Exception):
        """Crea una excepción a partir de un error de E/S (FileNotFound, PermissionDenied, etc.)."""
        return cls(tipo_operacion, nombre_archivo, causa, MensajesException.E_05_PERSISTENCIA)

    @classmethod
    def from_class_not_found(cls, tipo_operacion: TipoOperacion, nombre_archivo: str, causa: Exception):
        """Crea una excepción a partir de un error de clase faltante al deserializar."""
        return cls(tipo_operacion, nombre_archivo, causa, MensajesException.E_07_DESERIALIZACION)

    # --- Getter ---
    def get_tipo_operacion(self) -> TipoOperacion:
        """Devuelve el tipo de operación (LECTURA o ESCRITURA)."""
        return self._tipo_operacion
