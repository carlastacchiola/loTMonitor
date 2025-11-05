"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: /home/carla/DS/loTMonitor/python_iotmonitor
Fecha de generacion: 2025-11-05 11:02:11
Total de archivos integrados: 65
Total de directorios procesados: 20
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: .
#   1. main.py
#   2. __init__.py
#   3. constantes.py
#
# DIRECTORIO: entidades
#   4. __init__.py
#
# DIRECTORIO: entidades/sensores
#   5. __init__.py
#   6. sensor.py
#   7. sensor_ambiental.py
#   8. sensor_base.py
#   9. sensor_co2.py
#   10. sensor_humedad.py
#   11. sensor_luz.py
#   12. sensor_temperatura.py
#   13. tipo_sensor.py
#
# DIRECTORIO: entidades/usuarios
#   14. __init__.py
#   15. credencial_acceso.py
#   16. dispositivo_asignado.py
#   17. tarea_usuario.py
#   18. usuario.py
#
# DIRECTORIO: entidades/zonas
#   19. __init__.py
#   20. red_monitoreo.py
#   21. registro_ambiental.py
#   22. zona.py
#
# DIRECTORIO: excepciones
#   23. __init__.py
#   24. iot_exception.py
#   25. mensajes_exception.py
#   26. persistencia_exception.py
#   27. sensor_exception.py
#   28. zona_exception.py
#
# DIRECTORIO: iot_control
#   29. __init__.py
#
# DIRECTORIO: iot_control/control
#   30. __init__.py
#   31. iot_control.py
#
# DIRECTORIO: iot_control/sensores
#   32. __init__.py
#   33. humedad_reader_task.py
#   34. temperatura_reader_task.py
#
# DIRECTORIO: patrones
#   35. __init__.py
#
# DIRECTORIO: patrones/factory
#   36. __init__.py
#   37. sensor_factory.py
#
# DIRECTORIO: patrones/observer
#   38. __init__.py
#   39. observable.py
#   40. observer.py
#
# DIRECTORIO: patrones/observer/eventos
#   41. __init__.py
#   42. evento_sensor_ambiental.py
#   43. evento_zona.py
#
# DIRECTORIO: patrones/singleton
#   44. __init__.py
#   45. sensor_registry.py
#
# DIRECTORIO: patrones/strategy
#   46. __init__.py
#   47. lectura_sensor_strategy.py
#
# DIRECTORIO: patrones/strategy/impl
#   48. __init__.py
#   49. lectura_constante_strategy.py
#   50. lectura_variable_strategy.py
#
# DIRECTORIO: servicios
#   51. __init__.py
#
# DIRECTORIO: servicios/sensores
#   52. __init__.py
#   53. co2_service.py
#   54. humedad_service.py
#   55. luz_service.py
#   56. presion_service.py
#   57. sensor_service.py
#   58. sensor_service_registry.py
#   59. temperatura_service.py
#
# DIRECTORIO: servicios/usuarios
#   60. __init__.py
#   61. usuario_service.py
#
# DIRECTORIO: servicios/zonas
#   62. __init__.py
#   63. red_service.py
#   64. registro_service.py
#   65. zona_service.py
#



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 1/65: main.py
# Directorio: .
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/__init__.py
# ==============================================================================

import os
import sys
import time
from datetime import datetime

# Añadir paquete al path (para ejecutar desde cualquier lugar)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Importaciones necesarias ---
from python_iotmonitor.patrones.factory.sensor_factory import SensorFactory
from python_iotmonitor.patrones.singleton.sensor_registry import SensorRegistry
from python_iotmonitor.iot_control.control.iot_control import ControlAmbientalTask
from python_iotmonitor.constantes import CONTROL_AMBIENTAL_CICLO_SEGUNDOS as CICLO_CONTROL
from python_iotmonitor.entidades.zonas.zona import Zona
from python_iotmonitor.servicios.zonas.red_service import RedMonitoreoService

def setup_sistema():
    """
    Configura los sensores y el controlador principal del sistema IoTMonitor.
    """
    print("----------------------------------------------------------------------")
    print("  CONFIGURACIÓN INICIAL DEL SISTEMA DE MONITOREO AMBIENTAL")
    print("----------------------------------------------------------------------")

    # 1️⃣ Crear sensores con el Factory Method
    sensor_temp = SensorFactory.crear_sensor("Temperatura", id_sensor=1)
    sensor_hum = SensorFactory.crear_sensor("Humedad", id_sensor=2)

    # 2️⃣ Registrar sensores globalmente (Singleton)
    registry = SensorRegistry.get_instance()
    registry.registrar_sensor(sensor_temp.id_sensor, sensor_temp)
    registry.registrar_sensor(sensor_hum.id_sensor, sensor_hum)

    # 3️⃣ Crear la zona ambiental y el controlador central
    zona_lab = Zona(
        id_zona=1,
        nombre="Laboratorio Central",
        ubicada_en="Edificio Principal",
        tipo="Interior"
    )


    control_ambiental = ControlAmbientalTask(zona_lab, registry)

    # 4️⃣ Enlazar sensores con el controlador (Observer)
    sensor_temp.agregar_observer(control_ambiental)
    sensor_hum.agregar_observer(control_ambiental)

    return sensor_temp, sensor_hum, control_ambiental


# =========================================================================
# === MAIN SIMULACIÓN ===
# =========================================================================

def main_simulacion():
    """
    Simula el funcionamiento completo del sistema IoTMonitor.
    (Factory + Singleton + Observer + Strategy)
    """

    print("======================================================================")
    print("          SISTEMA DE MONITOREO AMBIENTAL - PATRONES DE DISEÑO")
    print("======================================================================")

    # ----------------------------------------------------------------------
    # 1. SINGLETON
    # ----------------------------------------------------------------------
    registry1 = SensorRegistry.get_instance()
    registry2 = SensorRegistry.get_instance()

    print("----------------------------------------------------------------------")
    print("   PATRÓN SINGLETON: Registro global de sensores")
    print("----------------------------------------------------------------------")
    print(f"ID de instancia: {id(registry1)}")
    if registry1 is registry2:
        print("[OK] SensorRegistry es Singleton (una sola instancia compartida)")
    else:
        print("[ERROR] SensorRegistry no es Singleton.")
        return

    # ----------------------------------------------------------------------
    # 2. CREACIÓN DE SENSORES (FACTORY METHOD)
    # ----------------------------------------------------------------------
    sensor_temp, sensor_hum, control_ambiental = setup_sistema()

    print("----------------------------------------------------------------------")
    print("   CREACIÓN DE SENSORES Y CONTROLADOR (FACTORY + OBSERVER)")
    print("----------------------------------------------------------------------")
    print(f"[Sensor] TemperaturaReaderTask-#{sensor_temp.id_sensor} creado.")
    print(f"[Sensor] HumedadReaderTask-#{sensor_hum.id_sensor} creado.")
    print("[Control] ControlAmbientalTask inicializado correctamente.")

    # ----------------------------------------------------------------------
    # 3. SIMULACIÓN (OBSERVER + STRATEGY + CONCURRENCIA)
    # ----------------------------------------------------------------------
    print("\n[Simulación] Iniciando tareas concurrentes...")
    sensor_temp.start()
    sensor_hum.start()
    control_ambiental.start()

    print("\n[Simulación] Ejecución activa por 10 segundos...\n")
    time.sleep(10)

    # ----------------------------------------------------------------------
    # 4. DETENER HILOS (GRACEFUL SHUTDOWN)
    # ----------------------------------------------------------------------
    print("\n[Sistema] Deteniendo sensores y controlador...")
    sensor_temp.parar()
    sensor_hum.parar()
    control_ambiental.parar()

    sensor_temp.join(timeout=0.5)
    sensor_hum.join(timeout=0.5)
    control_ambiental.join(timeout=0.5)

    print("[OK] Todos los hilos detenidos correctamente.")

    # === Persistencia ===
    print("\n[Sistema] Guardando estado de la red de monitoreo...")
    try:
        red_service = RedMonitoreoService()
        red_service.guardar_red(red_service)  
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la red: {e}")


    # ----------------------------------------------------------------------
    # 5. LOG DE RESULTADOS
    # ----------------------------------------------------------------------
    print("\n----------------------------------------------------------------------")
    print("   RESUMEN DE SIMULACIÓN")
    print("----------------------------------------------------------------------")
    print(f"[Tiempo total] {CICLO_CONTROL * 4:.1f} segundos estimados.")
    print(f"[Fecha finalización] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("[OK] FACTORY     - Creación dinámica de sensores")
    print("[OK] SINGLETON   - Registro global de sensores")
    print("[OK] OBSERVER    - Comunicación Sensor → Control")
    print("[OK] STRATEGY    - Variación de lecturas por estrategia de simulación")
    print("======================================================================\n")


# Punto de entrada principal
if __name__ == "__main__":
    main_simulacion()



# ==============================================================================
# ARCHIVO 2/65: __init__.py
# Directorio: .
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/__init__.py
# ==============================================================================


# ==============================================================================
# ARCHIVO 3/65: constantes.py
# Directorio: .
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/constantes.py
# ==============================================================================

import os

# ===============================================
# === Persistencia ===
# ===============================================
RUTA_PERSISTENCIA = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
NOMBRE_ARCHIVO_PERSISTENCIA = "red_monitoreo_test.dat"

# ===============================================
# === Constantes de Excepciones y Mensajes ===
# ===============================================

ERROR_SENSOR_NO_ENCONTRADO_CODE = "ERR-S01"
ERROR_ZONA_NO_ENCONTRADA_CODE = "ERR-Z02"
ERROR_PERSISTENCIA_CODE = "ERR-P03"
ERROR_FACTORY_CODE = "ERR-F04"
ERROR_REGISTRO_CODE = "ERR-R05"

# ===============================================
# === Constantes de Sensores (Factory / Observer) ===
# ===============================================

# Intervalos de muestreo (segundos)
INTERVALO_SENSOR_TEMPERATURA = 2.0
INTERVALO_SENSOR_HUMEDAD = 3.0
INTERVALO_SENSOR_CO2 = 4.0
INTERVALO_SENSOR_LUZ = 2.5

# Rangos de lectura simulada
TEMP_MIN_LECTURA = -10.0
TEMP_MAX_LECTURA = 45.0
HUMEDAD_MIN_LECTURA = 0.0
HUMEDAD_MAX_LECTURA = 100.0
CO2_MIN_LECTURA = 300.0     # ppm
CO2_MAX_LECTURA = 2000.0
LUZ_MIN_LECTURA = 100.0     # lux
LUZ_MAX_LECTURA = 10000.0

# ===============================================
# === Constantes del Control Ambiental (Strategy) ===
# ===============================================

# Límites críticos para activar estrategias automáticas
TEMP_CRITICA_ALTA = 30.0     # Activar enfriamiento
TEMP_CRITICA_BAJA = 10.0     # Activar calentamiento (opcional)
HUMEDAD_CRITICA_BAJA = 35.0  # Activar humidificación
CO2_CRITICO_ALTO = 1200.0    # Activar ventilación
LUZ_CRITICA_BAJA = 300.0     # Activar iluminación
LUZ_CRITICA_ALTA = 9000.0    # Reducir intensidad

# ===============================================
# === Ciclo de Control (Observer + Strategy) ===
# ===============================================

CONTROL_AMBIENTAL_CICLO_SEGUNDOS = 2.5  # Frecuencia de monitoreo del controlador central
DURACION_SIMULACION_SEGUNDOS = 30        # Tiempo total de simulación del sistema (tests)

# ===============================================
# === Usuarios y Roles ===
# ===============================================

ROLES_VALIDOS = ["admin", "tecnico", "observador"]

# ===============================================
# === Directorios / Logs ===
# ===============================================

DIRECTORIO_LOGS = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
NOMBRE_LOG_EVENTOS = "eventos_iot.log"



################################################################################
# DIRECTORIO: entidades
################################################################################

# ==============================================================================
# ARCHIVO 4/65: __init__.py
# Directorio: entidades
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: entidades/sensores
################################################################################

# ==============================================================================
# ARCHIVO 5/65: __init__.py
# Directorio: entidades/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 6/65: sensor.py
# Directorio: entidades/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 7/65: sensor_ambiental.py
# Directorio: entidades/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_ambiental.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 8/65: sensor_base.py
# Directorio: entidades/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_base.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 9/65: sensor_co2.py
# Directorio: entidades/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_co2.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 10/65: sensor_humedad.py
# Directorio: entidades/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_humedad.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 11/65: sensor_luz.py
# Directorio: entidades/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_luz.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 12/65: sensor_temperatura.py
# Directorio: entidades/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/sensor_temperatura.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 13/65: tipo_sensor.py
# Directorio: entidades/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/sensores/tipo_sensor.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: entidades/usuarios
################################################################################

# ==============================================================================
# ARCHIVO 14/65: __init__.py
# Directorio: entidades/usuarios
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 15/65: credencial_acceso.py
# Directorio: entidades/usuarios
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios/credencial_acceso.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 16/65: dispositivo_asignado.py
# Directorio: entidades/usuarios
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios/dispositivo_asignado.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 17/65: tarea_usuario.py
# Directorio: entidades/usuarios
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios/tarea_usuario.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 18/65: usuario.py
# Directorio: entidades/usuarios
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/usuarios/usuario.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: entidades/zonas
################################################################################

# ==============================================================================
# ARCHIVO 19/65: __init__.py
# Directorio: entidades/zonas
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/zonas/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 20/65: red_monitoreo.py
# Directorio: entidades/zonas
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/zonas/red_monitoreo.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 21/65: registro_ambiental.py
# Directorio: entidades/zonas
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/zonas/registro_ambiental.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 22/65: zona.py
# Directorio: entidades/zonas
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/entidades/zonas/zona.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: excepciones
################################################################################

# ==============================================================================
# ARCHIVO 23/65: __init__.py
# Directorio: excepciones
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 24/65: iot_exception.py
# Directorio: excepciones
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/iot_exception.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 25/65: mensajes_exception.py
# Directorio: excepciones
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/mensajes_exception.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 26/65: persistencia_exception.py
# Directorio: excepciones
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/persistencia_exception.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 27/65: sensor_exception.py
# Directorio: excepciones
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/sensor_exception.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 28/65: zona_exception.py
# Directorio: excepciones
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/excepciones/zona_exception.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: iot_control
################################################################################

# ==============================================================================
# ARCHIVO 29/65: __init__.py
# Directorio: iot_control
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/iot_control/__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: iot_control/control
################################################################################

# ==============================================================================
# ARCHIVO 30/65: __init__.py
# Directorio: iot_control/control
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/iot_control/control/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 31/65: iot_control.py
# Directorio: iot_control/control
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/iot_control/control/iot_control.py
# ==============================================================================

import threading
import time
from typing import TYPE_CHECKING
from python_iotmonitor.patrones.observer.observer import Observer
from python_iotmonitor.patrones.observer.eventos.evento_sensor_ambiental import EventoSensorAmbiental
from python_iotmonitor.constantes import (CONTROL_AMBIENTAL_CICLO_SEGUNDOS)

if TYPE_CHECKING:
    from python_iotmonitor.servicios.sensores.sensor_service_registry import SensorServiceRegistry
    from python_iotmonitor.entidades.zonas.zona import Zona


class ControlAmbientalTask(threading.Thread, Observer[EventoSensorAmbiental]):
    """
    Controlador Ambiental principal del sistema IoTMonitor.
    Actúa como hilo concurrente y observador de eventos de sensores.

    Se encarga de mantener condiciones ambientales estables reaccionando
    a los cambios en temperatura, humedad, CO₂ y luz.
    """

    def __init__(self, zona: "Zona", sensor_registry: "SensorServiceRegistry"):
        super().__init__()
        self.zona = zona
        self.sensor_registry = sensor_registry
        self._parar = threading.Event()
        self.name = f"ControlAmbientalThread-{zona.get_id_zona()}"
        self._lock = threading.Lock()

        # Últimos valores registrados
        self._ultima_temperatura = 0.0
        self._ultima_humedad = 50.0
        self._ultimo_co2 = 400.0
        self._ultima_luz = 250.0

    # -----------------------------------------------------------------------
    # Ciclo principal
    # -----------------------------------------------------------------------
    def run(self):
        """Inicia el ciclo continuo de monitoreo ambiental."""
        print(f"[{self.name}] Control ambiental iniciado.")
        while not self._parar.is_set():
            try:
                self._aplicar_control_ambiental()
            except Exception as e:
                print(f"[{self.name}]  Error en control ambiental: {e}")

            self._parar.wait(CONTROL_AMBIENTAL_CICLO_SEGUNDOS)

        print(f"[{self.name}] Control ambiental detenido.")

    # -----------------------------------------------------------------------
    # Observador de sensores
    # -----------------------------------------------------------------------
    def actualizar(self, evento: EventoSensorAmbiental) -> None:
        """Recibe notificaciones de los sensores y actualiza sus últimas lecturas."""
        with self._lock:
            if evento.tipo_sensor == "Temperatura":
                self._ultima_temperatura = evento.valor
            elif evento.tipo_sensor == "Humedad":
                self._ultima_humedad = evento.valor
            elif evento.tipo_sensor == "CO2":
                self._ultimo_co2 = evento.valor
            elif evento.tipo_sensor == "Luz":
                self._ultima_luz = evento.valor

    # -----------------------------------------------------------------------
    # Lógica de control ambiental
    # -----------------------------------------------------------------------
    def _aplicar_control_ambiental(self):
        """
        Evalúa las condiciones actuales y ejecuta acciones automáticas.
        Aplica estrategias de enfriamiento, ventilación, humidificación y ajuste de luz.
        """
        with self._lock:
            T = self._ultima_temperatura
            H = self._ultima_humedad
            C = self._ultimo_co2
            L = self._ultima_luz

        print(
            f"[{self.name}] Estado actual → T:{T}°C | H:{H}% | CO₂:{C}ppm | L:{L}lux"
        )

        # --- Temperatura (Strategy Enfriar / Calentar) ---
        if T < 8:
            print(" Activando calefacción ambiental...")
        elif T > 28:
            print(" Activando ventilación y enfriamiento...")

        # --- Humedad (Strategy Humidificar) ---
        if H < 40:
            print(" Activando humidificador...")
        elif H > 80:
            print(" Deshumidificando ambiente...")

        # --- CO₂ (Strategy Ventilar) ---
        if C > 900:
            print(" Nivel crítico de CO₂ — ventilación forzada activada.")
        elif C > 600:
            print(" Nivel alto de CO₂ — ventilación moderada.")

        # --- Luz (Strategy AjustarLuz) ---
        if L < 200:
            print(" Encendiendo luces automáticas.")
        elif L > 700:
            print(" Ambiente sobreiluminado — reduciendo luz artificial.")

    def parar(self):
        """Detiene el hilo de control ambiental de forma segura."""
        self._parar.set()



################################################################################
# DIRECTORIO: iot_control/sensores
################################################################################

# ==============================================================================
# ARCHIVO 32/65: __init__.py
# Directorio: iot_control/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/iot_control/sensores/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 33/65: humedad_reader_task.py
# Directorio: iot_control/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/iot_control/sensores/humedad_reader_task.py
# ==============================================================================

import threading
import time
import random
from typing import TYPE_CHECKING
from python_iotmonitor.patrones.observer.observable import Observable
from python_iotmonitor.patrones.observer.eventos.evento_sensor_ambiental import EventoSensorAmbiental
from python_iotmonitor.constantes import (
    INTERVALO_SENSOR_TEMPERATURA, TEMP_MIN_LECTURA, TEMP_MAX_LECTURA,
    INTERVALO_SENSOR_HUMEDAD, HUMEDAD_MIN_LECTURA, HUMEDAD_MAX_LECTURA,
)

if TYPE_CHECKING:
    from python_iotmonitor.patrones.observer.observer import Observer

class HumedadReaderTask(Observable[EventoSensorAmbiental], threading.Thread):
    """Simula lecturas periódicas de humedad ambiental (US-008, US-010)."""

    def __init__(self, id_sensor: int):
        Observable.__init__(self)
        threading.Thread.__init__(self)
        self.id_sensor: int = id_sensor
        self._parar = threading.Event()
        self.name = f"HumedadReaderTask-{self.id_sensor}"
        self._observers: list["Observer[EventoSensorAmbiental]"] = []

    def run(self):
        print(f"[{self.name}] Sensor iniciado. Lectura cada {INTERVALO_SENSOR_HUMEDAD}s.")
        while not self._parar.is_set():
            humedad = round(random.uniform(HUMEDAD_MIN_LECTURA, HUMEDAD_MAX_LECTURA), 1)
            evento = EventoSensorAmbiental("Humedad", humedad, "%", self.id_sensor)
            self.notificar_observers(evento)
            self._parar.wait(INTERVALO_SENSOR_HUMEDAD)

    def parar(self):
        self._parar.set()
        print(f"[{self.name}] Sensor detenido correctamente.")


# ==============================================================================
# ARCHIVO 34/65: temperatura_reader_task.py
# Directorio: iot_control/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/iot_control/sensores/temperatura_reader_task.py
# ==============================================================================

import threading
import time
import random
from typing import TYPE_CHECKING
from python_iotmonitor.patrones.observer.observable import Observable
from python_iotmonitor.patrones.observer.eventos.evento_sensor_ambiental import EventoSensorAmbiental
from python_iotmonitor.constantes import (
    INTERVALO_SENSOR_TEMPERATURA, TEMP_MIN_LECTURA, TEMP_MAX_LECTURA,
    INTERVALO_SENSOR_HUMEDAD, HUMEDAD_MIN_LECTURA, HUMEDAD_MAX_LECTURA,
)

if TYPE_CHECKING:
    from python_iotmonitor.patrones.observer.observer import Observer


class TemperaturaReaderTask(Observable[EventoSensorAmbiental], threading.Thread):
    """Simula lecturas periódicas de temperatura ambiental (US-008, US-010)."""

    def __init__(self, id_sensor: int):
        Observable.__init__(self)
        threading.Thread.__init__(self)
        self.id_sensor: int = id_sensor
        self._parar = threading.Event()
        self.name = f"TempReaderTask-{self.id_sensor}"
        self._observers: list["Observer[EventoSensorAmbiental]"] = []  # para que VS Code lo reconozca

    def run(self):
        print(f"[{self.name}] Sensor iniciado. Lectura cada {INTERVALO_SENSOR_TEMPERATURA}s.")
        while not self._parar.is_set():
            temperatura = round(random.uniform(TEMP_MIN_LECTURA, TEMP_MAX_LECTURA), 1)
            evento = EventoSensorAmbiental("Temperatura", temperatura, "°C", self.id_sensor)
            self.notificar_observers(evento)
            self._parar.wait(INTERVALO_SENSOR_TEMPERATURA)

    def parar(self):
        self._parar.set()
        print(f"[{self.name}] Sensor detenido correctamente.")


################################################################################
# DIRECTORIO: patrones
################################################################################

# ==============================================================================
# ARCHIVO 35/65: __init__.py
# Directorio: patrones
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: patrones/factory
################################################################################

# ==============================================================================
# ARCHIVO 36/65: __init__.py
# Directorio: patrones/factory
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/factory/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 37/65: sensor_factory.py
# Directorio: patrones/factory
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/factory/sensor_factory.py
# ==============================================================================

from typing import Union
from python_iotmonitor.iot_control.sensores.temperatura_reader_task import TemperaturaReaderTask
from python_iotmonitor.iot_control.sensores.humedad_reader_task import HumedadReaderTask

# Alias de tipo: puede expandirse con más sensores en el futuro
TipoSensor = Union[TemperaturaReaderTask, HumedadReaderTask]


class SensorFactory:
    """
    Implementación del patrón Factory Method (US-004).

    Permite crear sensores sin conocer sus clases concretas.
    Mejora la extensibilidad y evita condicionales repetitivos.
    """

    _factories = {
        "Temperatura": TemperaturaReaderTask,
        "Humedad": HumedadReaderTask,
    }

    @staticmethod
    def crear_sensor(tipo: str, id_sensor: int) -> TipoSensor:
        """
        Crea una instancia de sensor según su tipo.

        Args:
            tipo: Tipo del sensor ("Temperatura", "Humedad", etc.)
            id_sensor: Identificador único del sensor.

        Returns:
            Instancia del sensor correspondiente.

        Raises:
            ValueError: Si el tipo no está registrado.
        """
        tipo_normalizado = tipo.strip().capitalize()
        if tipo_normalizado not in SensorFactory._factories:
            raise ValueError(f"Tipo de sensor desconocido: {tipo}")

        clase_sensor = SensorFactory._factories[tipo_normalizado]
        return clase_sensor(id_sensor)



################################################################################
# DIRECTORIO: patrones/observer
################################################################################

# ==============================================================================
# ARCHIVO 38/65: __init__.py
# Directorio: patrones/observer
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 39/65: observable.py
# Directorio: patrones/observer
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/observable.py
# ==============================================================================

from typing import TypeVar, Generic, List, TYPE_CHECKING
import threading

T = TypeVar("T")

if TYPE_CHECKING:
    from python_iotmonitor.patrones.observer.observer import Observer


class Observable(Generic[T]):
    """
    Clase base genérica para objetos que emiten notificaciones (patrón Observer).

    En el sistema PythonIoTMonitor, los observables suelen ser:
      - Sensores (TemperaturaReaderTask, HumedadReaderTask)
      - Módulos que generan eventos ambientales (CO₂, luz, etc.)

    Los observadores pueden ser:
      - ControlAmbientalTask
      - Sistemas de registro o alarmas
    """

    def __init__(self):
        self._observers: List["Observer[T]"] = []
        self._lock = threading.Lock()  # Asegura la concurrencia

    # -----------------------------------------------------------------------
    # Registro / eliminación de observadores
    # -----------------------------------------------------------------------
    def agregar_observer(self, observer: "Observer[T]") -> None:
        """Agrega un nuevo observador si aún no está registrado."""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)

    def remover_observer(self, observer: "Observer[T]") -> None:
        """Elimina un observador del registro."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    # -----------------------------------------------------------------------
    # Notificación de eventos
    # -----------------------------------------------------------------------
    def notificar_observers(self, evento: T) -> None:
        """
        Notifica a todos los observadores registrados con un evento específico.

        Args:
            evento: Instancia del evento generado (por ejemplo, EventoSensorAmbiental).
        """
        # Se notifica sin lock para evitar deadlocks si el observador hace tareas pesadas
        for observer in list(self._observers):
            observer.actualizar(evento)


# ==============================================================================
# ARCHIVO 40/65: observer.py
# Directorio: patrones/observer
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/observer.py
# ==============================================================================

from typing import Protocol, TypeVar, Generic

T = TypeVar("T")

class Observer(Generic[T], Protocol):
    """
    Interfaz genérica del patrón Observer.
    Define el contrato que deben cumplir todos los observadores de eventos.

    En el contexto de PythonIoTMonitor, los observadores pueden ser:
    - ControlAmbientalTask (observador principal)
    - Servicios automáticos de monitoreo
    - Sistemas de alerta
    """

    def actualizar(self, evento: T) -> None:
        """
        Método llamado por el Observable para notificar un nuevo evento.

        Args:
            evento: Instancia del evento emitido (por ejemplo, EventoSensorAmbiental).
        """
        ...



################################################################################
# DIRECTORIO: patrones/observer/eventos
################################################################################

# ==============================================================================
# ARCHIVO 41/65: __init__.py
# Directorio: patrones/observer/eventos
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/eventos/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 42/65: evento_sensor_ambiental.py
# Directorio: patrones/observer/eventos
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/eventos/evento_sensor_ambiental.py
# ==============================================================================

from datetime import datetime


class EventoSensorAmbiental:
    """
    Clase que encapsula la información emitida por un sensor ambiental.
    Representa un evento dentro del sistema IoTMonitor.
    """

    def __init__(self, tipo: str, valor: float, unidad: str, id_sensor: int):
        """
        Inicializa un nuevo evento ambiental.

        Args:
            tipo: Tipo de sensor (Temperatura, Humedad, CO₂, Luz, etc.).
            valor: Valor leído por el sensor.
            unidad: Unidad de medida (°C, %, ppm, lux, etc.).
            id_sensor: Identificador único del sensor emisor.
        """
        self.timestamp = datetime.now()
        self.tipo_sensor = tipo
        self.valor = valor
        self.unidad = unidad
        self.id_sensor = id_sensor

    def __str__(self):
        """Devuelve una representación legible del evento."""
        return (
            f"[{self.tipo_sensor} #{self.id_sensor} @ "
            f"{self.timestamp.strftime('%H:%M:%S')}] → {self.valor}{self.unidad}"
        )


# ==============================================================================
# ARCHIVO 43/65: evento_zona.py
# Directorio: patrones/observer/eventos
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/eventos/evento_zona.py
# ==============================================================================

from datetime import datetime
from typing import Any


class EventoZona:
    """
    Clase que encapsula los eventos o cambios significativos 
    que ocurren dentro de una Zona de Monitoreo Ambiental (US-010, US-012).
    """

    def __init__(self, tipo: str, origen: str, datos_adicionales: Any = None):
        """
        Args:
            tipo: Tipo de evento (ejemplo: 'VENTILACION_ACTIVADA', 'ALERTA_CO2').
            origen: Identificador o nombre del componente que generó el evento 
                    (p. ej., 'Sensor CO₂ #3', 'ControlAmbientalTask-1').
            datos_adicionales: Información adicional relevante (valor medido, acción ejecutada, etc.).
        """
        self.timestamp = datetime.now()
        self.tipo = tipo
        self.origen = origen
        self.datos_adicionales = datos_adicionales

    def __str__(self):
        """Devuelve una representación textual del evento."""
        detalle = (
            f"Detalles: {self.datos_adicionales}"
            if self.datos_adicionales
            else "Sin detalles"
        )
        return (
            f"[EVENTO ZONA] Tipo: {self.tipo} | Origen: {self.origen} | "
            f"{detalle} | Hora: {self.timestamp.strftime('%H:%M:%S')}"
        )



################################################################################
# DIRECTORIO: patrones/singleton
################################################################################

# ==============================================================================
# ARCHIVO 44/65: __init__.py
# Directorio: patrones/singleton
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/singleton/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 45/65: sensor_registry.py
# Directorio: patrones/singleton
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/singleton/sensor_registry.py
# ==============================================================================

from threading import Lock
from typing import Dict


class SensorRegistry:
    """
    Singleton que mantiene un registro global de sensores activos.
    (US-008)

    Permite registrar, obtener y listar sensores del sistema IoTMonitor.
    Garantiza que solo exista una única instancia de registro.
    """

    _instance = None
    _lock = Lock()

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._sensors: Dict[int, object] = {}
        self._initialized = True

    # -------------------------------------------------------------------------
    # Método Singleton
    # -------------------------------------------------------------------------
    @classmethod
    def get_instance(cls) -> "SensorRegistry":
        """Devuelve la única instancia del registro de sensores."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # doble chequeo
                    cls._instance = cls()
        return cls._instance

    # -------------------------------------------------------------------------
    # Métodos de gestión
    # -------------------------------------------------------------------------
    def registrar_sensor(self, id_sensor: int, sensor: object) -> None:
        """Registra un nuevo sensor en el sistema."""
        if id_sensor in self._sensors:
            print(f"[SensorRegistry] Sensor #{id_sensor} ya registrado.")
        else:
            self._sensors[id_sensor] = sensor
            print(f"[SensorRegistry] Sensor #{id_sensor} agregado correctamente.")

    def obtener_sensor(self, id_sensor: int) -> object:
        """Devuelve el sensor correspondiente al ID."""
        return self._sensors.get(id_sensor)

    def listar_sensores(self) -> Dict[int, object]:
        """Devuelve un diccionario con todos los sensores registrados."""
        return dict(self._sensors)



################################################################################
# DIRECTORIO: patrones/strategy
################################################################################

# ==============================================================================
# ARCHIVO 46/65: __init__.py
# Directorio: patrones/strategy
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 47/65: lectura_sensor_strategy.py
# Directorio: patrones/strategy
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/lectura_sensor_strategy.py
# ==============================================================================

from abc import ABC, abstractmethod

class LecturaSensorStrategy(ABC):
    """
    Interfaz base del patrón Strategy para generar lecturas de sensores.
    (US-010)
    """

    @abstractmethod
    def generar_valor(self) -> float:
        """
        Genera un valor de lectura simulado o calculado para un sensor,
        dependiendo de su tipo (temperatura, humedad, CO₂, luz, etc.).
        """
        pass



################################################################################
# DIRECTORIO: patrones/strategy/impl
################################################################################

# ==============================================================================
# ARCHIVO 48/65: __init__.py
# Directorio: patrones/strategy/impl
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/impl/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 49/65: lectura_constante_strategy.py
# Directorio: patrones/strategy/impl
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/impl/lectura_constante_strategy.py
# ==============================================================================

from enum import Enum
from python_iotmonitor.patrones.strategy.lectura_sensor_strategy import LecturaSensorStrategy


class TipoConstante(Enum):
    HUMEDAD = "Humedad"
    LUZ = "Luz"


class LecturaConstanteStrategy(LecturaSensorStrategy):
    """
    Implementación del patrón Strategy:
    La lectura es constante o dentro de un rango fijo,
    ideal para sensores con baja variación (Humedad, Luz).
    """

    def __init__(self, tipo: TipoConstante):
        self._tipo = tipo

    def generar_valor(self) -> float:
        """
        Genera una lectura constante basada en el tipo de sensor.
        """
        if self._tipo == TipoConstante.HUMEDAD:
            # Simula una humedad ambiente promedio (entre 45–55%)
            return 50.0
        elif self._tipo == TipoConstante.LUZ:
            # Simula una intensidad de luz promedio (entre 400–500 lux)
            return 450.0
        else:
            return 0.0


# ==============================================================================
# ARCHIVO 50/65: lectura_variable_strategy.py
# Directorio: patrones/strategy/impl
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/strategy/impl/lectura_variable_strategy.py
# ==============================================================================

from datetime import datetime
from python_iotmonitor.patrones.strategy.lectura_sensor_strategy import LecturaSensorStrategy


class LecturaVariableStrategy(LecturaSensorStrategy):
    """
    Implementación del patrón Strategy:
    La lectura varía según la hora del día o la estación simulada.

    - De día → valores más altos (temperatura, luz, CO₂)
    - De noche → valores más bajos
    """

    def generar_valor(self) -> float:
        """
        Genera un valor de lectura variable basado en la hora actual.
        """
        hora_actual = datetime.now().hour

        # --- Simulación de variación diurna ---
        if 6 <= hora_actual < 18:
            # Día: temperatura/luz altas, CO₂ activo
            return round(20 + (hora_actual - 6) * 0.8, 1)  # Ej. entre 20°C y 30°C
        else:
            # Noche: valores más bajos y estables
            return round(10 + (hora_actual % 6) * 0.5, 1)  # Ej. entre 10°C y 13°C



################################################################################
# DIRECTORIO: servicios
################################################################################

# ==============================================================================
# ARCHIVO 51/65: __init__.py
# Directorio: servicios
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: servicios/sensores
################################################################################

# ==============================================================================
# ARCHIVO 52/65: __init__.py
# Directorio: servicios/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 53/65: co2_service.py
# Directorio: servicios/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/co2_service.py
# ==============================================================================

from typing import TYPE_CHECKING
import random
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.entidades.sensores.sensor import Sensor

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class CO2Service(SensorService):
    """Servicio con lógica específica para sensores de CO₂."""

    def procesar_lectura(self, sensor: "Sensor") -> None:
        """
        Procesa la lectura actual de CO₂ y simula la activación
        de mecanismos de ventilación o alertas (US-008, US-010).
        """
        if sensor.get_tipo().lower() not in ["co2", "dioxido de carbono"]:
            raise TypeError("CO2Service solo puede operar con sensores de tipo 'CO₂'.")

        valor_actual = sensor.get_valor_actual()

        # --- Lógica de reacción ante niveles de CO₂ ---
        if valor_actual > 1000:
            accion = " Nivel crítico — activando ventilación forzada"
        elif valor_actual > 700:
            accion = " Nivel alto — aumentando ventilación"
        else:
            accion = " Nivel normal de CO₂"

        print(f"[CO2Service] Sensor {sensor.get_tipo()} #{sensor.get_id()} → {valor_actual:.1f} ppm ({accion})")

        # --- Simulación adicional ---
        # Cada cierto ciclo, el sensor puede generar una lectura aleatoria de calibración
        if random.random() < 0.1:
            print(f"[CO2Service] Sensor {sensor.get_id()} ejecutó calibración automática.")


# ==============================================================================
# ARCHIVO 54/65: humedad_service.py
# Directorio: servicios/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/humedad_service.py
# ==============================================================================

from typing import TYPE_CHECKING
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.constantes import HUMEDAD_MAX_RIEGO
from python_iotmonitor.entidades.sensores.sensor import Sensor

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class HumedadService(SensorService):
    """Servicio con lógica específica para sensores de humedad."""

    def procesar_lectura(self, sensor: "Sensor") -> None:
        """
        Procesa la lectura actual del sensor de humedad e identifica
        si deben activarse mecanismos de humidificación o alertas (US-008).
        """
        if sensor.get_tipo().lower() != "humedad":
            raise TypeError("HumedadService solo puede operar con sensores de tipo 'Humedad'.")

        valor_actual = sensor.get_valor_actual()

        # --- Lógica de control ambiental específica ---
        if valor_actual < 20:
            accion = " Activando humidificador (nivel crítico)"
        elif valor_actual < HUMEDAD_MAX_RIEGO:
            accion = " Activando humidificación moderada"
        else:
            accion = " Humedad adecuada"

        print(f"[HumedadService] Sensor {sensor.get_tipo()} #{sensor.get_id()} → {valor_actual:.1f}% ({accion})")


# ==============================================================================
# ARCHIVO 55/65: luz_service.py
# Directorio: servicios/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/luz_service.py
# ==============================================================================

from typing import TYPE_CHECKING
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.entidades.sensores.sensor import Sensor

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class LuzService(SensorService):
    """Servicio con lógica específica para sensores de luz."""

    def procesar_lectura(self, sensor: "Sensor") -> None:
        """
        Procesa la lectura actual de luz y aplica decisiones automáticas
        sobre iluminación ambiental (US-008, US-010).
        """
        if sensor.get_tipo().lower() not in ["luz", "luminosidad"]:
            raise TypeError("LuzService solo puede operar con sensores de tipo 'Luz'.")

        valor_actual = sensor.get_valor_actual()

        # --- Lógica específica de control lumínico ---
        if valor_actual < 200:
            accion = " Intensificando iluminación (ambiente oscuro)"
        elif valor_actual < 500:
            accion = " Iluminación adecuada"
        else:
            accion = " Ambiente sobreiluminado — reduciendo luz artificial"

        print(f"[LuzService] Sensor {sensor.get_tipo()} #{sensor.get_id()} → {valor_actual:.1f} lux ({accion})")


# ==============================================================================
# ARCHIVO 56/65: presion_service.py
# Directorio: servicios/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/presion_service.py
# ==============================================================================

from typing import TYPE_CHECKING
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.entidades.sensores.sensor import Sensor

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class PresionService(SensorService):
    """Servicio con lógica específica para sensores de presión atmosférica."""

    def procesar_lectura(self, sensor: "Sensor") -> None:
        """
        Procesa la lectura actual del sensor de presión y aplica
        ajustes o alertas según los valores registrados (US-008).
        """
        if sensor.get_tipo().lower() not in ["presion", "presión"]:
            raise TypeError("PresionService solo puede operar con sensores de tipo 'Presión'.")

        valor_actual = sensor.get_valor_actual()

        # --- Lógica específica: fluctuaciones de presión ---
        if valor_actual < 950:
            estado = " Presión baja — posible tormenta"
        elif valor_actual > 1030:
            estado = " Presión alta — clima estable"
        else:
            estado = " Presión normal"

        print(f"[PresionService] Sensor {sensor.get_tipo()} #{sensor.get_id()} → {valor_actual:.1f} hPa ({estado})")

        # --- Simula “madurez” o recalibración periódica ---
        if hasattr(sensor, "necesita_recalibracion") and sensor.necesita_recalibracion():
            sensor.calibrar()
            print(f"[PresionService] Sensor #{sensor.get_id()} recalibrado automáticamente.")


# ==============================================================================
# ARCHIVO 57/65: sensor_service.py
# Directorio: servicios/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/sensor_service.py
# ==============================================================================

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from python_iotmonitor.patrones.strategy.lectura_sensor_strategy import LecturaSensorStrategy

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class SensorService(ABC):
    """
    Clase abstracta base para los servicios de sensores.
    Contiene la inyección del patrón Strategy (US-008, US-010),
    utilizado para calcular lecturas y calibraciones.
    """

    def __init__(self, lectura_strategy: LecturaSensorStrategy):
        self._lectura_strategy = lectura_strategy

    # -----------------------------------------------------------------------
    # Lógica específica de cada sensor
    # -----------------------------------------------------------------------
    @abstractmethod
    def procesar_lectura(self, sensor: "Sensor") -> None:
        """Lógica específica de procesamiento o transformación de lectura."""
        pass

    # -----------------------------------------------------------------------
    # Estrategia de lectura común (Strategy)
    # -----------------------------------------------------------------------
    def aplicar_lectura(self, sensor: "Sensor") -> float:
        """
        Aplica la estrategia de lectura al sensor inyectado.
        Devuelve el valor leído y actualiza el sensor.
        """
        valor_leido = self._lectura_strategy.generar_valor()
        sensor.set_valor_actual(valor_leido)
        return valor_leido

    # -----------------------------------------------------------------------
    # Calibración genérica
    # -----------------------------------------------------------------------
    def calibrar_sensor(self, sensor: "Sensor") -> None:
        """
        Simula la calibración del sensor.
        Este método puede ser sobreescrito por clases concretas.
        """
        print(f"[SensorService] Calibrando sensor {sensor.get_tipo()}...")
        sensor.calibrar()


# ==============================================================================
# ARCHIVO 58/65: sensor_service_registry.py
# Directorio: servicios/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/sensor_service_registry.py
# ==============================================================================

from typing import Dict
from python_iotmonitor.patrones.strategy.impl.lectura_variable_strategy import LecturaVariableStrategy
from python_iotmonitor.patrones.strategy.impl.lectura_constante_strategy import LecturaConstanteStrategy, TipoConstante
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.servicios.sensores.temperatura_service import TemperaturaService
from python_iotmonitor.servicios.sensores.humedad_service import HumedadService
from python_iotmonitor.servicios.sensores.co2_service import CO2Service
from python_iotmonitor.servicios.sensores.luz_service import LuzService


class SensorServiceRegistry:
    """
    Patrón Registry implementado como Singleton (US-TECH-005).
    Mapea el tipo de sensor a su Service correspondiente con la Strategy inyectada.
    """
    _instance: "SensorServiceRegistry" = None
    _registry: Dict[str, SensorService] = {}

    def __new__(cls):
        """Implementa Singleton simple (sin locks, suficiente en Python)."""
        if cls._instance is None:
            cls._instance = super(SensorServiceRegistry, cls).__new__(cls)
            cls._instance._inicializar_registro()
        return cls._instance

    # -----------------------------------------------------------------------
    # Inicialización de servicios con sus estrategias respectivas
    # -----------------------------------------------------------------------
    def _inicializar_registro(self):
        """Inicializa los servicios y asocia estrategias de lectura adecuadas."""

        # Strategy Variable para sensores dinámicos (temperatura, CO₂)
        variable_strategy = LecturaVariableStrategy()
        self._registry["Temperatura"] = TemperaturaService(lectura_strategy=variable_strategy)
        self._registry["CO2"] = CO2Service(lectura_strategy=variable_strategy)

        # Strategy Constante para sensores estables (humedad, luz)
        constante_humedad = LecturaConstanteStrategy(TipoConstante.HUMEDAD)
        constante_luz = LecturaConstanteStrategy(TipoConstante.LUZ)
        self._registry["Humedad"] = HumedadService(lectura_strategy=constante_humedad)
        self._registry["Luz"] = LuzService(lectura_strategy=constante_luz)

    # -----------------------------------------------------------------------
    # Acceso público
    # -----------------------------------------------------------------------
    def get_service(self, tipo_sensor: str) -> SensorService:
        """
        Obtiene el servicio de sensor según su tipo.
        
        Args:
            tipo_sensor: Tipo textual del sensor (Temperatura, CO2, etc.).

        Raises:
            ValueError: Si no existe un servicio para ese tipo de sensor.
        """
        tipo_normalizado = tipo_sensor.strip().capitalize()
        service = self._registry.get(tipo_normalizado)

        if service is None:
            raise ValueError(f"Servicio no encontrado para el tipo de sensor: {tipo_sensor}")

        return service


# ==============================================================================
# ARCHIVO 59/65: temperatura_service.py
# Directorio: servicios/sensores
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/sensores/temperatura_service.py
# ==============================================================================

from typing import TYPE_CHECKING
from python_iotmonitor.servicios.sensores.sensor_service import SensorService
from python_iotmonitor.entidades.sensores.sensor import Sensor

if TYPE_CHECKING:
    from python_iotmonitor.entidades.sensores.sensor import Sensor


class TemperaturaService(SensorService):
    """
    Servicio para sensores de temperatura.
    Implementa la lógica de procesamiento y control térmico básico (US-008, US-010).
    """

    def procesar_lectura(self, sensor: "Sensor") -> None:
        """
        Lógica de procesamiento para lecturas de temperatura.
        Aplica ajustes de tendencia térmica según el rango medido.
        """
        if sensor.get_tipo().lower() != "temperatura":
            raise TypeError("TemperaturaService solo puede operar con sensores de tipo 'Temperatura'.")

        valor_actual = sensor.get_valor_actual()

        # Simula un ajuste basado en tendencias térmicas
        if valor_actual < 10:
            accion = "Activando calefacción"
        elif valor_actual > 30:
            accion = "Activando ventilación"
        else:
            accion = "Temperatura estable"

        print(f"[TemperaturaService] {sensor.get_tipo()} #{sensor.get_id()} → {valor_actual:.2f}°C ({accion})")



################################################################################
# DIRECTORIO: servicios/usuarios
################################################################################

# ==============================================================================
# ARCHIVO 60/65: __init__.py
# Directorio: servicios/usuarios
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/usuarios/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 61/65: usuario_service.py
# Directorio: servicios/usuarios
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/usuarios/usuario_service.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: servicios/zonas
################################################################################

# ==============================================================================
# ARCHIVO 62/65: __init__.py
# Directorio: servicios/zonas
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/zonas/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 63/65: red_service.py
# Directorio: servicios/zonas
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/zonas/red_service.py
# ==============================================================================

import os
import pickle
from python_iotmonitor.entidades.zonas.red_monitoreo import RedMonitoreo
from python_iotmonitor.constantes import RUTA_PERSISTENCIA
from python_iotmonitor.excepciones.persistencia_exception import PersistenciaException


class RedMonitoreoService:
    """
    Servicio con lógica de negocio y persistencia específica para la entidad RedMonitoreo.
    Gestiona las métricas globales y la persistencia de la red (equivalente al RegistroForestal).
    """

    def __init__(self):
        # Asegura que exista la carpeta de datos
        os.makedirs(RUTA_PERSISTENCIA, exist_ok=True)

    # -----------------------------------------------------------------------
    # Cálculo de cobertura y monitoreo
    # -----------------------------------------------------------------------
    def calcular_cobertura(self, red: RedMonitoreo) -> dict:
        """
        Calcula las métricas de cobertura general de la red de monitoreo.

        Args:
            red: Instancia de la red de monitoreo.

        Returns:
            Un diccionario con métricas de cobertura (zonas, sensores promedio, etc.).
        """
        total_zonas = red.get_total_zonas()
        total_sensores = red.get_total_sensores()
        promedio_sensores_por_zona = (
            total_sensores / total_zonas if total_zonas > 0 else 0
        )

        return {
            "total_zonas": total_zonas,
            "total_sensores": total_sensores,
            "promedio_sensores_por_zona": round(promedio_sensores_por_zona, 2),
        }

    # -----------------------------------------------------------------------
    # Actualización del valor de red (equivalente al "avaluo")
    # -----------------------------------------------------------------------
    def actualizar_prioridad(self, red: RedMonitoreo, peso_zonas: int) -> float:
        """
        Calcula y devuelve un índice de prioridad ambiental de la red,
        basado en la cantidad de zonas y sensores (equivalente al avalúo).

        Args:
            red: La red de monitoreo.
            peso_zonas: Valor ponderado de cada zona según criticidad.

        Returns:
            Índice de prioridad ambiental de la red.
        """
        prioridad = (
            red.get_total_zonas() * peso_zonas
            + red.get_total_sensores() * 0.1  # ponderación secundaria
        )
        return round(prioridad, 2)

    # -----------------------------------------------------------------------
    # Persistencia (equivalente a RegistroForestalService)
    # -----------------------------------------------------------------------
    def guardar_red(self, red: RedMonitoreo, nombre_archivo: str = "red_monitoreo.dat") -> None:
        """
        Serializa y guarda la red de monitoreo en /data.
        """
        ruta = os.path.join(RUTA_PERSISTENCIA, nombre_archivo)
        try:
            with open(ruta, "wb") as f:
                pickle.dump(red, f)
            print(f"[OK] Red de monitoreo guardada en: {ruta}")
        except Exception as e:
            raise PersistenciaException(f"Error al guardar la red: {e}")

    def cargar_red(self, nombre_archivo: str = "red_monitoreo.dat") -> RedMonitoreo:
        """
        Carga la red de monitoreo desde un archivo en /data.
        """
        ruta = os.path.join(RUTA_PERSISTENCIA, nombre_archivo)
        try:
            with open(ruta, "rb") as f:
                red = pickle.load(f)
            print(f"[OK] Red de monitoreo cargada desde: {ruta}")
            return red
        except FileNotFoundError:
            raise PersistenciaException("Archivo de red no encontrado.")
        except Exception as e:
            raise PersistenciaException(f"Error al leer la red: {e}")


# ==============================================================================
# ARCHIVO 64/65: registro_service.py
# Directorio: servicios/zonas
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/zonas/registro_service.py
# ==============================================================================

import pickle
from python_iotmonitor.entidades.zonas.registro_ambiental import RegistroAmbiental
from python_iotmonitor.excepciones.persistencia_exception import PersistenciaException, TipoOperacion


class RegistroAmbientalService:
    """
    Servicio para manejar el Registro Ambiental, incluyendo operaciones de persistencia (US-012).
    """

    def guardar_registro(self, registro: RegistroAmbiental, ruta_archivo: str) -> None:
        """
        Serializa y guarda el objeto RegistroAmbiental en disco.

        Args:
            registro: Objeto del tipo RegistroAmbiental a guardar.
            ruta_archivo: Ruta completa del archivo de destino.
        """
        try:
            with open(ruta_archivo, "wb") as f:
                pickle.dump(registro, f)
            print(f"[RegistroAmbientalService] Registro guardado en {ruta_archivo}")
        except Exception as e:
            raise PersistenciaException.from_io_exception(
                TipoOperacion.ESCRITURA, ruta_archivo, e
            )

    def leer_registro(self, ruta_archivo: str) -> RegistroAmbiental:
        """
        Deserializa y carga un objeto RegistroAmbiental desde un archivo.

        Args:
            ruta_archivo: Ruta del archivo .dat que contiene el registro.

        Returns:
            Instancia de RegistroAmbiental.
        """
        try:
            with open(ruta_archivo, "rb") as f:
                registro = pickle.load(f)
                print(f"[RegistroAmbientalService] Registro cargado correctamente desde {ruta_archivo}")
                return registro
        except FileNotFoundError:
            raise PersistenciaException(
                TipoOperacion.LECTURA,
                ruta_archivo,
                FileNotFoundError("Archivo de registro ambiental no encontrado."),
                error_code="E_05_PERSISTENCIA"
            )
        except Exception as e:
            # Captura errores de deserialización o clases inexistentes
            raise PersistenciaException.from_class_not_found(
                TipoOperacion.LECTURA, ruta_archivo, e
            )

    def actualizar_prioridad_registro(self, registro: RegistroAmbiental, nueva_prioridad: int) -> None:
        """
        Actualiza el nivel de prioridad ambiental en el registro.

        Args:
            registro: Instancia de RegistroAmbiental a modificar.
            nueva_prioridad: Nuevo valor de prioridad ambiental.
        """
        if hasattr(registro, "_prioridad"):
            registro._prioridad = nueva_prioridad
            print(f"[RegistroAmbientalService] Prioridad del registro actualizada a {nueva_prioridad}.")
        else:
            print("[RegistroAmbientalService] Advertencia: el registro no contiene atributo '_prioridad'.")


# ==============================================================================
# ARCHIVO 65/65: zona_service.py
# Directorio: servicios/zonas
# Ruta completa: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/zonas/zona_service.py
# ==============================================================================

from typing import List, Optional, Type, TypeVar, Generic
import random
from python_iotmonitor.entidades.zonas.zona import Zona
from python_iotmonitor.entidades.sensores.sensor import Sensor
from python_iotmonitor.excepciones.zona_exception import ZonaNoEncontradaException
from python_iotmonitor.excepciones.sensor_exception import SensorFueraDeRangoException

# --- Clase genérica de empaquetado ---
T = TypeVar('T')  # Tipo genérico
S = TypeVar('S', bound=Sensor)  # Subclase de Sensor


class PaqueteLecturas(Generic[T]):
    """
    Clase genérica que representa un paquete de lecturas exportadas (US-010, US-012).
    Permite empaquetar lecturas o sensores de un tipo específico.
    """
    def __init__(self, tipo_sensor: str, contenido: List[T]):
        """
        Inicializa un nuevo paquete de lecturas.

        Args:
            tipo_sensor: Tipo de sensor (e.g., Temperatura, Humedad).
            contenido: Lista de lecturas o instancias exportadas.
        """
        self._tipo_sensor = tipo_sensor
        self._contenido = contenido

    def get_contenido(self) -> List[T]:
        """Devuelve la lista de lecturas o sensores contenidos."""
        return self._contenido

    def __str__(self) -> str:
        """Devuelve una representación textual del paquete."""
        salida = f"\nPaquete de {self._tipo_sensor} ({len(self._contenido)} registros)"
        salida += "\nContenido:\n"
        for item in self._contenido:
            salida += f"  - {item}\n"
        return salida


# ============================================================================


class ZonaService:
    """
    Servicio con la lógica central de gestión de Zonas (US-004, US-008, US-010, US-012).
    Maneja operaciones de sensores, lecturas y mantenimiento ambiental.
    """

    def __init__(self):
        self._contador_id_lectura = 0

    # -----------------------------------------------------------------------
    # Registrar sensores
    # -----------------------------------------------------------------------
    def agregar_sensor(self, zona: Zona, sensor: Sensor) -> None:
        """
        Agrega un sensor a una zona existente (US-004).

        Args:
            zona: La zona a la que se agregará el sensor.
            sensor: El sensor que se desea registrar.

        Raises:
            ZonaNoEncontradaException: Si la zona es nula o no existe.
        """
        if not zona:
            raise ZonaNoEncontradaException("Desconocida", 0)

        zona.agregar_sensor(sensor)
        print(f"[ZonaService] Sensor '{sensor.get_tipo()}' agregado correctamente a la zona '{zona.get_nombre()}'.")

    # -----------------------------------------------------------------------
    # Simular lecturas
    # -----------------------------------------------------------------------
    def simular_lecturas_zona(self, zona: Zona) -> None:
        """
        Simula un ciclo completo de lecturas ambientales para todos los sensores (US-008, US-010).

        Args:
            zona: Zona a simular.
        """
        sensores = zona.get_sensores_internal()
        if not sensores:
            raise ZonaNoEncontradaException(zona.get_nombre(), 0)

        print(f"\n[ZonaService] Iniciando simulación de lecturas para zona '{zona.get_nombre()}'.")
        for sensor in sensores:
            valor_simulado = random.uniform(*sensor.get_rango())
            try:
                sensor.set_valor_actual(valor_simulado)
                print(f"  - {sensor.get_tipo()}: {valor_simulado:.2f} {sensor.get_unidad()}")
            except SensorFueraDeRangoException as e:
                print(f"[ALERTA] {e.get_full_message()}")

        estado = zona.evaluar_condiciones()
        print(f"[ZonaService] Estado ambiental general: {estado}")

    # -----------------------------------------------------------------------
    # Exportar lecturas
    # -----------------------------------------------------------------------
    def exportar_datos_zona(self, zona: Zona, tipo_sensor: Type[S]) -> PaqueteLecturas[S]:
        """
        Exporta las lecturas de un tipo de sensor específico (US-012).

        Args:
            zona: La zona desde la que se exportarán los datos.
            tipo_sensor: Tipo de sensor (clase concreta).

        Returns:
            Un paquete genérico con los sensores exportados.
        """
        sensores = [s for s in zona.get_sensores() if isinstance(s, tipo_sensor)]
        nombre_sensor = tipo_sensor.__name__

        if not sensores:
            print(f"[AVISO] No hay sensores del tipo {nombre_sensor} registrados en la zona.")
            return PaqueteLecturas(nombre_sensor, [])

        print(f"[ZonaService] Exportando datos de {len(sensores)} sensores de tipo '{nombre_sensor}'.")
        return PaqueteLecturas(nombre_sensor, sensores)

    # -----------------------------------------------------------------------
    # Mantenimiento de sensores
    # -----------------------------------------------------------------------
    def recalibrar_sensores(self, zona: Zona) -> None:
        """
        Recalibra todos los sensores de una zona (US-010).

        Args:
            zona: La zona cuyos sensores se recalibrarán.
        """
        print(f"\n[ZonaService] Recalibrando sensores de la zona '{zona.get_nombre()}'.")
        for sensor in zona.get_sensores_internal():
            sensor.calibrar()
            print(f"  - Sensor {sensor.get_tipo()} calibrado correctamente.")



################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 64
# Generado: 2025-11-05 11:02:11
################################################################################
