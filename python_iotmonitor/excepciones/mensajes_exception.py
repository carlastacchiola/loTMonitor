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
