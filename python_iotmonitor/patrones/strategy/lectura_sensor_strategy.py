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
