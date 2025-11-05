"""
Archivo integrador generado automaticamente
Directorio: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/eventos
Fecha: 2025-11-05 11:02:11
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/eventos/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: evento_sensor_ambiental.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/eventos/evento_sensor_ambiental.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/3: evento_zona.py
# Ruta: /home/carla/DS/loTMonitor/python_iotmonitor/patrones/observer/eventos/evento_zona.py
# ================================================================================

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


