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
