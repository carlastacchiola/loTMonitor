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
