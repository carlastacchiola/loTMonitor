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
