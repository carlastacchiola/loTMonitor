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
