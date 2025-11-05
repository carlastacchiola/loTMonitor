"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/usuarios
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/usuarios/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: usuario_service.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/usuarios/usuario_service.py
# ================================================================================

from typing import List
from datetime import datetime
from python_iotmonitor.entidades.usuarios.usuario import Usuario
from python_iotmonitor.entidades.usuarios.tarea_usuario import TareaUsuario
from python_iotmonitor.excepciones.iot_exception import CredencialInvalidaException


class UsuarioService:
    """
    Servicio para gestionar las tareas y credenciales de los usuarios del sistema (US-009, US-010).
    """

    def asignar_tarea(self, usuario: Usuario, tarea: TareaUsuario) -> None:
        """
        Asigna una nueva tarea a un usuario.

        Args:
            usuario: Usuario al que se le asigna la tarea.
            tarea: Instancia de TareaUsuario a asignar.
        """
        usuario.agregar_tarea(tarea)
        print(f"[UsuarioService] Tarea {tarea.get_id()} asignada a {usuario.get_nombre()}.")

    def completar_tarea(self, usuario: Usuario, id_tarea: int) -> bool:
        """
        Busca una tarea por ID y la marca como completada.

        Args:
            usuario: Usuario que completa la tarea.
            id_tarea: ID de la tarea a marcar como completada.

        Returns:
            True si la tarea fue encontrada y marcada; False si no se encontró.
        """
        for tarea in usuario.get_tareas_internal():
            if tarea.get_id() == id_tarea:
                tarea.set_completada(True)
                return True
        return False

    def get_usuarios_activos(self, usuarios: List[Usuario]) -> List[Usuario]:
        """
        Filtra y retorna solo los usuarios con credenciales activas (US-010).

        Args:
            usuarios: Lista completa de usuarios.

        Returns:
            Lista de usuarios con acceso activo.
        """
        return [u for u in usuarios if u.get_credencial().esta_activa()]

    def ejecutar_tareas(self, usuario: Usuario) -> None:
        """
        Ejecuta todas las tareas pendientes del usuario.
        Valida que la credencial esté activa antes de iniciar (US-009, US-010).

        Args:
            usuario: Usuario que ejecutará sus tareas pendientes.

        Raises:
            CredencialInvalidaException: Si el usuario no tiene credencial activa.
        """
        if not usuario.get_credencial().esta_activa():
            raise CredencialInvalidaException(usuario.get_nombre())

        print(f"\n[UsuarioService] Ejecutando tareas de {usuario.get_nombre()} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")

        tareas_pendientes = [t for t in usuario.get_tareas_internal() if not t.esta_completada()]
        if not tareas_pendientes:
            print(f"  {usuario.get_nombre()} no tiene tareas pendientes.")
            return

        # Orden descendente por ID
        tareas_pendientes.sort(key=lambda t: t.get_id(), reverse=True)

        for tarea in tareas_pendientes:
            self.completar_tarea(usuario, tarea.get_id())
            dispositivo = tarea.get_dispositivo()
            print(f"  Tarea #{tarea.get_id()}: {tarea.get_descripcion()}")
            print(f"  Usando dispositivo: {dispositivo.get_nombre()}")


