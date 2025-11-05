"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 6
"""

# ================================================================================
# ARCHIVO 1/6: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/6: iot_exception.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/iot_exception.py
# ================================================================================

class IoTMonitorException(Exception):
    """Clase base para todas las excepciones del sistema IoTMonitor."""
    def __init__(self, error_code: str, message: str, user_message: str):
        # Mensaje técnico para el log del sistema
        super().__init__(f"[{error_code}] - {message}")
        self._error_code = error_code
        self._user_message = user_message

    def get_error_code(self) -> str:
        """Devuelve el código de error estandarizado."""
        return self._error_code

    def get_user_message(self) -> str:
        """Devuelve el mensaje de error amigable para el usuario."""
        return self._user_message

    def get_full_message(self) -> str:
        """Devuelve el mensaje completo con código, detalle y mensaje de usuario."""
        return f"Error ({self._error_code}): {self._user_message} (Detalle: {super().__str__()})"


# ==============================================================
# Excepciones específicas del dominio de usuarios
# ==============================================================

class UsuarioException(IoTMonitorException):
    """Excepción base para errores en la gestión de usuarios."""


class CredencialInvalidaException(UsuarioException):
    """
    Se lanza cuando un usuario intenta acceder al sistema con credenciales inactivas
    o vencidas (US-009, US-010).
    """

    def __init__(self, nombre_usuario: str):
        error_code = "ERR-USR-001"
        internal_msg = f"Validación de credencial fallida para usuario: {nombre_usuario}. La credencial está inactiva o expirada."
        user_msg = f"El usuario '{nombre_usuario}' no tiene acceso activo al sistema."
        super().__init__(error_code, internal_msg, user_msg)
        self._nombre_usuario = nombre_usuario


# ================================================================================
# ARCHIVO 3/6: mensajes_exception.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/mensajes_exception.py
# ================================================================================

class MensajesException:
    # ==============================================================
    # Códigos de error (usados en IoTMonitorException)
    # ==============================================================

    E_01_ZONA = "ERROR 01"
    E_02_SENSOR = "ERROR 02"
    E_03_CREDENCIAL = "ERROR 03"
    E_05_PERSISTENCIA = "ERROR 05"
    E_07_DESERIALIZACION = "ERROR 07"

    # ==============================================================
    # Mensajes de usuario (para mostrar en interfaz o logs)
    # ==============================================================

    # --- Zonas ---
    MSG_ZONA_USER = (
        "No se encontró la zona especificada o no hay zonas disponibles. "
        "Verifique la red de monitoreo e intente nuevamente."
    )

    # --- Sensores ---
    MSG_SENSOR_USER = (
        "¡Alerta! Un sensor ha registrado valores fuera del rango permitido. "
        "Revise las condiciones ambientales o recalibre el dispositivo."
    )

    # --- Credenciales / Usuarios ---
    MSG_CREDENCIAL_USER = (
        "El usuario no posee credenciales válidas o su acceso ha expirado. "
        "Contacte a un administrador para restablecer el acceso."
    )

    # --- Persistencia ---
    MSG_PERSISTENCIA_USER = (
        "Error al guardar o recuperar los datos del sistema. "
        "Informe este incidente al soporte con el código {}."
    )


# ================================================================================
# ARCHIVO 4/6: persistencia_exception.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/persistencia_exception.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 5/6: sensor_exception.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/sensor_exception.py
# ================================================================================

from python_iotmonitor.excepciones.iot_exception import IoTMonitorException
from python_iotmonitor.excepciones.mensajes_exception import MensajesException


class SensorFueraDeRangoException(IoTMonitorException):
    """
    Excepción lanzada cuando un sensor registra un valor fuera del rango permitido.
    Por ejemplo: temperatura excesiva, humedad negativa, o CO₂ fuera de umbral crítico.
    """

    def __init__(self, tipo_sensor: str, valor: float, rango_min: float, rango_max: float):
        """
        Inicializa la excepción.

        Args:
            tipo_sensor: Tipo de sensor (Temperatura, CO2, Humedad, etc.).
            valor: Valor medido que causó el error.
            rango_min: Límite inferior permitido.
            rango_max: Límite superior permitido.
        """
        self._tipo_sensor = tipo_sensor
        self._valor = valor
        self._rango_min = rango_min
        self._rango_max = rango_max

        # Mensaje detallado para logs
        msg = (
            f"Lectura fuera de rango en sensor {tipo_sensor}. "
            f"Valor leído: {valor}, Rango permitido: [{rango_min}, {rango_max}]."
        )

        super().__init__(
            MensajesException.E_02_SENSOR,
            msg,
            MensajesException.MSG_SENSOR_USER
        )

    def get_tipo_sensor(self) -> str:
        """Devuelve el tipo de sensor que causó la excepción."""
        return self._tipo_sensor

    def get_valor(self) -> float:
        """Devuelve el valor leído fuera de rango."""
        return self._valor

    def get_rango_min(self) -> float:
        """Devuelve el límite inferior del rango permitido."""
        return self._rango_min

    def get_rango_max(self) -> float:
        """Devuelve el límite superior del rango permitido."""
        return self._rango_max


# ================================================================================
# ARCHIVO 6/6: zona_exception.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/zona_exception.py
# ================================================================================

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


