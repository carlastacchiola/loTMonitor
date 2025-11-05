"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/zonas
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/zonas/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/4: red_service.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/zonas/red_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/4: registro_service.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/zonas/registro_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/4: zona_service.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/servicios/zonas/zona_service.py
# ================================================================================

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


