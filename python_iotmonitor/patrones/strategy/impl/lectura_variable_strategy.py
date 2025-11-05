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
