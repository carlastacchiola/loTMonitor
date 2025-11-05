"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 9
"""

# ================================================================================
# ARCHIVO 1/9: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/9: sensor.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor.py
# ================================================================================

from abc import ABC, abstractmethod
from typing import Protocol

# Contador simple para IDs únicos de Sensor
_SENSOR_ID_COUNTER = 0


class Serializable(Protocol):
    """Protocolo para indicar que una clase es serializable (Pickle)."""
    pass


class Sensor(ABC, Serializable):
    """
    Clase abstracta base para todos los sensores del sistema IoTMonitor.
    Actúa como interfaz común y garantiza compatibilidad con serialización.
    """

    def __init__(self, tipo: str):
        """
        Inicializa la clase base de Sensor.

        Args:
            tipo: Tipo de sensor (e.g., "Temperatura", "Humedad", "CO2", "Luz").
        """
        global _SENSOR_ID_COUNTER
        _SENSOR_ID_COUNTER += 1

        self._id = _SENSOR_ID_COUNTER
        self._tipo = tipo
        self._valor_actual = None
        self._unidad = ""
        self._activo = True
        self._calibrado = False

    # --- Métodos abstractos para implementación concreta ---
    @abstractmethod
    def get_valor_actual(self) -> float:
        """Devuelve el valor actual leído por el sensor."""
        pass

    @abstractmethod
    def set_valor_actual(self, valor: float) -> None:
        """Actualiza el valor actual leído por el sensor."""
        pass

    # --- Getters y setters comunes ---
    def get_id(self) -> int:
        """Devuelve el ID único del sensor."""
        return self._id

    def get_tipo(self) -> str:
        """Devuelve el tipo del sensor."""
        return self._tipo

    def get_unidad(self) -> str:
        """Devuelve la unidad de medida del sensor."""
        return self._unidad

    def set_unidad(self, unidad: str) -> None:
        """Establece la unidad de medida del sensor (°C, %, ppm, lux, etc.)."""
        self._unidad = unidad

    def esta_activo(self) -> bool:
        """Indica si el sensor está activo."""
        return self._activo

    def activar(self) -> None:
        """Activa el sensor."""
        self._activo = True

    def desactivar(self) -> None:
        """Desactiva el sensor."""
        self._activo = False

    def esta_calibrado(self) -> bool:
        """Devuelve True si el sensor fue calibrado correctamente."""
        return self._calibrado

    def calibrar(self) -> None:
        """Marca el sensor como calibrado."""
        self._calibrado = True


# ================================================================================
# ARCHIVO 3/9: sensor_ambiental.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_ambiental.py
# ================================================================================

from abc import ABC
import threading
from python_iotmonitor.entidades.sensores.sensor import Sensor


class SensorAmbiental(Sensor, ABC):
    """
    Clase base abstracta para sensores ambientales del sistema IoTMonitor.
    Provee control thread-safe sobre los valores leídos y define si requieren calibración ambiental.
    """

    def __init__(self, tipo: str, unidad: str, requiere_calibracion: bool = True):
        """
        Inicializa un sensor ambiental.

        Args:
            tipo: Tipo de sensor (Temperatura, Humedad, CO2, Luz, etc.).
            unidad: Unidad de medida del sensor.
            requiere_calibracion: Indica si el sensor necesita calibración inicial.
        """
        super().__init__(tipo)
        self._unidad = unidad
        self._requiere_calibracion = requiere_calibracion
        self._valor_actual = 0.0
        self._lock = threading.Lock()

    # --- Métodos thread-safe ---
    def get_valor_actual(self) -> float:
        """Devuelve el valor actual leído por el sensor (Thread-safe)."""
        with self._lock:
            return self._valor_actual

    def set_valor_actual(self, valor: float) -> None:
        """
        Actualiza el valor del sensor (Thread-safe).
        Asegura que no se asignen valores negativos o nulos inesperados.
        """
        with self._lock:
            self._valor_actual = max(0.0, valor)

    # --- Métodos de persistencia ---
    def __getstate__(self):
        """Devuelve el estado del sensor a serializar, excluyendo el lock."""
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state):
        """Restaura el estado del sensor al deserializar e inicializa un nuevo lock."""
        self.__dict__.update(state)
        self._lock = threading.Lock()

    # --- Métodos adicionales ---
    def requiere_calibracion(self) -> bool:
        """
        Devuelve True si el sensor requiere calibración ambiental.
        """
        return self._requiere_calibracion


# ================================================================================
# ARCHIVO 4/9: sensor_base.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_base.py
# ================================================================================

from abc import ABC
import threading
from python_iotmonitor.entidades.sensores.sensor import Sensor
from python_iotmonitor.constantes import (
    TEMP_MIN_LECTURA, TEMP_MAX_LECTURA,
    HUMEDAD_MIN_LECTURA, HUMEDAD_MAX_LECTURA,
    CO2_MIN_LECTURA, CO2_MAX_LECTURA,
    LUZ_MIN_LECTURA, LUZ_MAX_LECTURA
)


class SensorBase(Sensor, ABC):
    """
    Clase base abstracta para todos los sensores del sistema IoTMonitor.
    Provee manejo común de ID, valor actual, unidad de medida y seguridad en hilos.
    """
    _id_counter = 0

    def __init__(self, tipo: str, unidad: str, rango_min: float, rango_max: float):
        """
        Inicializa un nuevo sensor base.

        Args:
            tipo: Tipo de sensor (Temperatura, Humedad, CO2, Luz).
            unidad: Unidad de medida (°C, %, ppm, lux).
            rango_min: Valor mínimo esperado de medición.
            rango_max: Valor máximo esperado de medición.
        """
        super().__init__(tipo)
        SensorBase._id_counter += 1
        self._id = SensorBase._id_counter
        self._unidad = unidad
        self._rango_min = rango_min
        self._rango_max = rango_max
        self._valor_actual = None
        self._lock = threading.Lock()

    # --- Getters básicos ---
    def get_id(self) -> int:
        """Devuelve el ID único del sensor."""
        return self._id

    def get_tipo(self) -> str:
        """Devuelve el tipo de sensor."""
        return self._tipo

    def get_unidad(self) -> str:
        """Devuelve la unidad de medida del sensor."""
        return self._unidad

    def get_rango(self) -> tuple:
        """Devuelve el rango de medición del sensor."""
        return self._rango_min, self._rango_max

    def get_valor_actual(self) -> float:
        """Devuelve el último valor leído del sensor."""
        return self._valor_actual

    # --- Setters seguros ---
    def set_valor_actual(self, valor: float) -> None:
        """
        Actualiza el valor actual del sensor (Thread-safe).
        Asegura que el valor quede dentro de su rango válido.
        """
        with self._lock:
            valor_limitado = max(self._rango_min, min(valor, self._rango_max))
            self._valor_actual = valor_limitado

    # --- Métodos de persistencia ---
    def __getstate__(self):
        """Devuelve el estado serializable del sensor, excluyendo el lock."""
        state = self.__dict__.copy()
        del state['_lock']
        return state

    def __setstate__(self, state):
        """Restaura el estado del sensor al deserializar e inicializa un nuevo lock."""
        self.__dict__.update(state)
        self._lock = threading.Lock()


# ================================================================================
# ARCHIVO 5/9: sensor_co2.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_co2.py
# ================================================================================

from python_iotmonitor.entidades.sensores.sensor_base import SensorBase
from python_iotmonitor.constantes import CO2_MIN_LECTURA, CO2_MAX_LECTURA


class SensorCO2(SensorBase):
    """
    Representa un sensor de dióxido de carbono (CO₂) en ppm.
    Hereda de SensorBase y añade atributos específicos de control de calidad del aire.
    """

    def __init__(self, modelo: str, nivel_alarma: float = 1200.0):
        """
        Inicializa un sensor de CO₂.

        Args:
            modelo: Modelo o nombre comercial del sensor.
            nivel_alarma: Nivel de concentración en ppm a partir del cual se activa una alerta.
        """
        super().__init__(tipo="CO2", unidad="ppm", rango_min=CO2_MIN_LECTURA, rango_max=CO2_MAX_LECTURA)
        self._modelo = modelo
        self._nivel_alarma = nivel_alarma
        self._alertas_activadas = 0

    def get_modelo(self) -> str:
        """Devuelve el modelo del sensor."""
        return self._modelo

    def get_nivel_alarma(self) -> float:
        """Devuelve el nivel de alarma configurado para el sensor."""
        return self._nivel_alarma

    def set_nivel_alarma(self, valor: float) -> None:
        """Actualiza el nivel de alarma para este sensor."""
        self._nivel_alarma = max(self._rango_min, min(valor, self._rango_max))

    def registrar_alerta(self) -> None:
        """Incrementa el contador de alertas activadas."""
        self._alertas_activadas += 1

    def get_alertas_activadas(self) -> int:
        """Devuelve la cantidad de veces que se activó una alerta por exceso de CO₂."""
        return self._alertas_activadas


# ================================================================================
# ARCHIVO 6/9: sensor_humedad.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_humedad.py
# ================================================================================

from python_iotmonitor.entidades.sensores.sensor_ambiental import SensorAmbiental
from python_iotmonitor.constantes import HUMEDAD_MIN_LECTURA, HUMEDAD_MAX_LECTURA


class SensorHumedad(SensorAmbiental):
    """
    Representa un sensor de humedad relativa del aire (%).
    Hereda de SensorAmbiental e incluye información adicional como modelo o marca.
    """

    def __init__(self, modelo: str, requiere_calibracion: bool = True):
        """
        Inicializa un sensor de humedad.

        Args:
            modelo: Modelo o nombre comercial del sensor.
            requiere_calibracion: Indica si el sensor necesita calibración.
        """
        super().__init__(tipo="Humedad", unidad="%", requiere_calibracion=requiere_calibracion)
        self._modelo = modelo
        self._rango_min = HUMEDAD_MIN_LECTURA
        self._rango_max = HUMEDAD_MAX_LECTURA

    def get_modelo(self) -> str:
        """Devuelve el modelo del sensor."""
        return self._modelo

    def requiere_calibracion(self) -> bool:
        """Devuelve True si el sensor necesita calibración."""
        return super().requiere_calibracion()


# ================================================================================
# ARCHIVO 7/9: sensor_luz.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_luz.py
# ================================================================================

from python_iotmonitor.entidades.sensores.sensor_ambiental import SensorAmbiental
from python_iotmonitor.constantes import LUZ_MIN_LECTURA, LUZ_MAX_LECTURA


class SensorLuz(SensorAmbiental):
    """
    Representa un sensor de luminosidad (lux) dentro del sistema IoTMonitor.
    Puede instalarse en interior o exterior.
    """

    def __init__(self, es_interior: bool = True):
        """
        Inicializa un sensor de luz.

        Args:
            es_interior: True si el sensor está instalado en interior, False si está al aire libre.
        """
        super().__init__(tipo="Luz", unidad="lux", requiere_calibracion=False)
        self._es_interior = es_interior
        self._rango_min = LUZ_MIN_LECTURA
        self._rango_max = LUZ_MAX_LECTURA

    def es_interior(self) -> bool:
        """Devuelve True si el sensor está instalado en interior."""
        return self._es_interior

    def set_es_interior(self, interior: bool) -> None:
        """Establece si el sensor está instalado en interior o exterior."""
        self._es_interior = interior


# ================================================================================
# ARCHIVO 8/9: sensor_temperatura.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_temperatura.py
# ================================================================================

from python_iotmonitor.entidades.sensores.sensor_base import SensorBase
from python_iotmonitor.constantes import TEMP_MIN_LECTURA, TEMP_MAX_LECTURA


class SensorTemperatura(SensorBase):
    """
    Representa un sensor de temperatura ambiental (°C).
    Hereda de SensorBase e incluye información del modelo y control de lecturas acumuladas.
    """

    def __init__(self, modelo: str):
        """
        Inicializa un sensor de temperatura.

        Args:
            modelo: Modelo o tipo de sensor (ej. DHT11, LM35, DS18B20).
        """
        super().__init__(tipo="Temperatura", unidad="°C", rango_min=TEMP_MIN_LECTURA, rango_max=TEMP_MAX_LECTURA)
        self._modelo = modelo
        self._lecturas_acumuladas = 0.0
        self._cantidad_lecturas = 0

    def get_modelo(self) -> str:
        """Devuelve el modelo o tipo de sensor."""
        return self._modelo

    def registrar_lectura(self, valor: float) -> None:
        """
        Registra una nueva lectura de temperatura y actualiza el promedio acumulado.

        Args:
            valor: Valor medido en grados Celsius.
        """
        self.set_valor_actual(valor)
        self._lecturas_acumuladas += valor
        self._cantidad_lecturas += 1

    def get_promedio_lecturas(self) -> float:
        """Devuelve el promedio de todas las lecturas registradas."""
        if self._cantidad_lecturas == 0:
            return 0.0
        return round(self._lecturas_acumuladas / self._cantidad_lecturas, 2)


# ================================================================================
# ARCHIVO 9/9: tipo_sensor.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/tipo_sensor.py
# ================================================================================

from enum import Enum

class TipoSensor(Enum):
    """
    Define los tipos de sensores disponibles en el sistema IoTMonitor.
    Este enum se utiliza por la fábrica de sensores (Factory Method).
    """

    TEMPERATURA = "Temperatura"
    HUMEDAD = "Humedad"
    CO2 = "CO2"
    LUZ = "Luz"


