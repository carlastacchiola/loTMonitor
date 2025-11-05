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
