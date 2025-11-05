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
