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
