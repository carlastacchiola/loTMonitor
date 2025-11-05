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
