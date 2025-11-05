"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/zonas
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/zonas/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/4: red_monitoreo.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/zonas/red_monitoreo.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/4: registro_ambiental.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/zonas/registro_ambiental.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/4: zona.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/zonas/zona.py
# ================================================================================

import threading
from typing import List, TYPE_CHECKING
from python_iotmonitor.entidades.sensores.sensor import Sensor, Serializable
from python_iotmonitor.constantes import CO2_CRITICO_ALTO, HUMEDAD_CRITICA_BAJA, TEMP_CRITICA_ALTA

if TYPE_CHECKING:
    from python_iotmonitor.entidades.zonas.red_monitoreo import RedMonitoreo
    from python_iotmonitor.entidades.usuarios.usuario import Usuario


class Zona(Serializable):
    """
    Representa una zona ambiental dentro de una red de monitoreo IoT.
    Cada zona contiene múltiples sensores y puede tener usuarios asignados.
    """

    def __init__(self, id_zona: int, nombre: str, ubicada_en: 'RedMonitoreo', tipo: str):
        """
        Inicializa una nueva zona de monitoreo.

        Args:
            id_zona: ID único de la zona.
            nombre: Nombre identificador de la zona (ej. “Laboratorio A”).
            ubicada_en: Referencia a la red de monitoreo a la que pertenece.
        """
        self._id = id_zona
        self._nombre = nombre
        self._ubicada_en = ubicada_en
        self._sensores: List[Sensor] = []
        self._usuarios: List['Usuario'] = []
        self._lock = threading.Lock()
        self._alertas_activas = 0
        self._tipo = tipo 

    # --- Métodos de Persistencia (Serialización Thread-Safe) ---
    def __getstate__(self):
        """Devuelve el estado serializable de la zona (excluye el lock)."""
        state = self.__dict__.copy()
        del state['_lock']
        return state

    def __setstate__(self, state):
        """Restaura el estado al deserializar e inicializa un nuevo lock."""
        self.__dict__.update(state)
        self._lock = threading.Lock()

    # --- Métodos básicos ---
    def get_id_zona(self) -> int:
        """Devuelve el ID único de la zona."""
        return self._id

    def get_nombre(self) -> str:
        """Devuelve el nombre de la zona."""
        return self._nombre
    
    def get_tipo(self) -> str:
        return self._tipo

    def get_sensores_internal(self) -> List[Sensor]:
        """Acceso interno a la lista mutable de sensores (uso en servicios)."""
        return self._sensores

    def set_sensores_internal(self, nuevos_sensores: List[Sensor]) -> None:
        """Reemplaza completamente la lista de sensores (thread-safe)."""
        with self._lock:
            self._sensores = nuevos_sensores

    def get_sensores(self) -> List[Sensor]:
        """Devuelve una copia inmutable de los sensores registrados."""
        return list(self._sensores)

    def get_usuarios(self) -> List['Usuario']:
        """Devuelve una copia inmutable de los usuarios asignados."""
        return list(self._usuarios)

    def set_usuarios(self, usuarios: List['Usuario']) -> None:
        """Reemplaza la lista de usuarios asignados (thread-safe)."""
        with self._lock:
            self._usuarios = usuarios

    # --- Operaciones sobre sensores ---
    def agregar_sensor(self, sensor: Sensor) -> None:
        """Agrega un sensor a la zona (thread-safe)."""
        with self._lock:
            self._sensores.append(sensor)

    def remover_sensor(self, sensor: Sensor) -> None:
        """Remueve un sensor de la zona si existe."""
        with self._lock:
            if sensor in self._sensores:
                self._sensores.remove(sensor)

    # --- Gestión de alertas ---
    def registrar_alerta(self) -> None:
        """Incrementa el contador de alertas activas en la zona."""
        with self._lock:
            self._alertas_activas += 1

    def get_alertas_activas(self) -> int:
        """Devuelve la cantidad de alertas activas registradas."""
        return self._alertas_activas

    def evaluar_condiciones(self) -> str:
        """
        Evalúa las condiciones generales de la zona según los sensores registrados.

        Returns:
            Una descripción textual del estado ambiental de la zona.
        """
        alertas = []
        for s in self._sensores:
            if s.get_tipo() == "Temperatura" and s.get_valor_actual() > TEMP_CRITICA_ALTA:
                alertas.append("Alta temperatura")
            elif s.get_tipo() == "Humedad" and s.get_valor_actual() < HUMEDAD_CRITICA_BAJA:
                alertas.append("Baja humedad")
            elif s.get_tipo() == "CO2" and s.get_valor_actual() > CO2_CRITICO_ALTO:
                alertas.append("CO₂ elevado")

        return ", ".join(alertas) if alertas else "Condiciones normales"


