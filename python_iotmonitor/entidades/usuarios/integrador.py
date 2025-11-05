"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/5: credencial_acceso.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios/credencial_acceso.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/5: dispositivo_asignado.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios/dispositivo_asignado.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/5: tarea_usuario.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios/tarea_usuario.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 5/5: usuario.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios/usuario.py
# ================================================================================

from typing import List
from datetime import datetime
from python_iotmonitor.entidades.sensores.sensor import Serializable
from python_iotmonitor.entidades.usuarios.credencial_acceso import CredencialAcceso
from python_iotmonitor.entidades.usuarios.tarea_usuario import TareaUsuario


class Usuario(Serializable):
    """
    Representa un usuario del sistema IoTMonitor.
    Puede ser un administrador, técnico o observador (US-009).
    """

    def __init__(self, id_usuario: int, nombre: str, rol: str, tareas: List[TareaUsuario]):
        """
        Inicializa un nuevo usuario.

        Args:
            id_usuario: Identificador único del usuario.
            nombre: Nombre completo.
            rol: Rol del usuario ('admin', 'tecnico', 'observador').
            tareas: Lista inicial de tareas asignadas.
        """
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._rol = rol.lower()
        # La credencial se crea por defecto con acceso activo
        self._credencial = CredencialAcceso(
            activa=True,
            fecha_emision=datetime.now(),
            observaciones="Acceso válido por defecto"
        )
        self._tareas: List[TareaUsuario] = tareas  # Lista mutable interna

    # --- Getters básicos ---
    def get_id(self) -> int:
        """Devuelve el identificador único del usuario."""
        return self._id_usuario

    def get_nombre(self) -> str:
        """Devuelve el nombre completo del usuario."""
        return self._nombre

    def get_rol(self) -> str:
        """Devuelve el rol del usuario."""
        return self._rol

    # --- Credencial de acceso ---
    def get_credencial(self) -> CredencialAcceso:
        """Devuelve la credencial digital asociada al usuario."""
        return self._credencial

    def asignar_credencial(self, activa: bool, fecha_emision: datetime, observaciones: str) -> None:
        """
        Asigna una nueva credencial o actualiza la existente.

        Args:
            activa: Estado del acceso.
            fecha_emision: Fecha de emisión de la credencial.
            observaciones: Notas o motivos del cambio.
        """
        self._credencial = CredencialAcceso(activa, fecha_emision, observaciones)

    # --- Tareas ---
    def get_tareas(self) -> List[TareaUsuario]:
        """Devuelve una copia inmutable de la lista de tareas asignadas."""
        return list(self._tareas)

    def get_tareas_internal(self) -> List[TareaUsuario]:
        """Devuelve la lista interna mutable de tareas (uso interno de servicios)."""
        return self._tareas

    def agregar_tarea(self, tarea: TareaUsuario) -> None:
        """Agrega una nueva tarea al usuario."""
        self._tareas.append(tarea)


