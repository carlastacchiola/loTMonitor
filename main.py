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
