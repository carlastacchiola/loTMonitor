# IoTMonitor – Sistema de Monitoreo Ambiental con Patrones de Diseño

Proyecto académico desarrollado como simulador de un **sistema de control ambiental inteligente**,  
aplicando principios de **Programación Orientada a Objetos**, **Patrones de Diseño**,  
**Concurrencia** y **Persistencia de datos**.

---

##  Objetivo general

El proyecto busca representar el funcionamiento de una **red de monitoreo ambiental IoT**,  
capaz de medir temperatura y humedad en distintas zonas, reaccionar a los valores leídos,  
y aplicar estrategias automáticas de control (ventilación, enfriamiento, deshumidificación, etc.).  

El sistema está diseñado para **mostrar la integración de múltiples patrones de diseño** en un entorno concurrente y modular.

---

##  Arquitectura general

###  Estructura de paquetes

```
python_iotmonitor/
│
├── constantes.py
├── main.py
│
├── entidades/
│   └── zonas/
│       ├── zona.py
│       └── red_monitoreo.py
│
├── patrones/
│   ├── observer/
│   │   ├── observable.py
│   │   ├── observer.py
│   │   └── eventos/
│   │       └── evento_sensor_ambiental.py
│   ├── strategy/
│   │   ├── absorcion_agua_strategy.py
│   │   └── impl/
│   │       ├── absorcion_constante_strategy.py
│   │       └── absorcion_seasonal_strategy.py
│   └── singleton/
│       └── sensor_registry.py
│
├── iot_control/
│   ├── sensores/
│   │   ├── temperatura_reader_task.py
│   │   └── humedad_reader_task.py
│   └── control/
│       └── control_ambiental_task.py
│
├── servicios/
│   ├── red_monitoreo_service.py
│   └── zona_service.py
│
└── excepciones/
    ├── persistencia_exception.py
    └── mensajes_exception.py
```

---

##  Principales componentes

###  Sensores (Factory + Observer)
Los sensores (`TemperaturaReaderTask`, `HumedadReaderTask`) simulan lecturas periódicas concurrentes  
mediante hilos (`threading.Thread`) y notifican eventos al controlador ambiental a través del patrón **Observer**.

###  Control ambiental (Observer + Strategy)
La clase `ControlAmbientalTask` observa los eventos de los sensores y aplica reglas de control:
- Activación de ventilación y enfriamiento.
- Deshumidificación o humidificación del ambiente.
- Reajuste dinámico de temperatura y humedad (si está habilitado).

###  SensorRegistry (Singleton)
Centraliza el registro global de sensores activos, asegurando una única instancia compartida en todo el sistema.

###  SensorFactory (Factory Method)
Crea dinámicamente sensores de temperatura o humedad sin conocer sus clases concretas.

###  RedMonitoreoService (Persistencia)
Gestiona el guardado y carga automática de la red de monitoreo en formato `.dat` dentro del directorio `/data/`.

---

##  Ejecución del sistema

### ▶ Comando

```bash
python3 main.py
```

###  Ejemplo de salida (resumen)

```
======================================================================
          SISTEMA DE MONITOREO AMBIENTAL - PATRONES DE DISEÑO
======================================================================
----------------------------------------------------------------------
   PATRÓN SINGLETON: Registro global de sensores
----------------------------------------------------------------------
[SensorRegistry] Sensor #1 agregado correctamente.
[SensorRegistry] Sensor #2 agregado correctamente.
----------------------------------------------------------------------
   CREACIÓN DE SENSORES Y CONTROLADOR (FACTORY + OBSERVER)
----------------------------------------------------------------------
[Sensor] TemperaturaReaderTask-#1 creado.
[Sensor] HumedadReaderTask-#2 creado.
[Control] ControlAmbientalTask inicializado correctamente.

[Simulación] Iniciando tareas concurrentes...
[TempReaderTask-1] Sensor iniciado. Lectura cada 2.0s.
[HumedadReaderTask-2] Sensor iniciado. Lectura cada 3.0s.
[ControlAmbientalThread-1] Control ambiental iniciado.
[ControlAmbientalThread-1] Estado actual → T:34.3°C | H:75.4%
 Activando ventilación y enfriamiento...
[ControlAmbientalThread-1] Estado actual → T:20.7°C | H:82.8%
 Deshumidificando ambiente...

[Sistema] Guardando estado de la red de monitoreo...
[OK] Red de monitoreo guardada en: /data/red_monitoreo.dat
======================================================================
   RESUMEN FINAL
======================================================================
[OK] FACTORY     - Creación dinámica de sensores
[OK] SINGLETON   - Registro global de sensores
[OK] OBSERVER    - Comunicación Sensor → Control
[OK] STRATEGY    - Variación de lecturas por estrategia
[OK] PERSISTENCIA - Archivo red_monitoreo.dat generado
======================================================================
```

---

##  Patrones de diseño aplicados

| Patrón | Implementación | Módulo |
|--------|----------------|--------|
| **Singleton** | `SensorRegistry` asegura instancia única | `patrones/singleton/sensor_registry.py` |
| **Factory Method** | `SensorFactory` crea sensores dinámicamente | `iot_control/sensores` |
| **Observer** | Comunicación Sensor → Control Ambiental | `patrones/observer` |
| **Strategy** | Variación de comportamiento del control ambiental | `patrones/strategy` |
| **Persistencia (Custom)** | Serialización binaria automática | `servicios/red_monitoreo_service.py` |

---

##  Persistencia automática

Cada simulación genera (o sobreescribe) un archivo:
```
/data/red_monitoreo.dat
```
Este archivo guarda el estado completo de la red de monitoreo (zonas, sensores y controladores).  
Permite reanudar la simulación o verificar su integridad tras un reinicio.

---

##  Extensiones posibles

- Agregar sensores de **CO₂** y **Luz ambiental**.
- Implementar interfaz gráfica con PyQt o Tkinter.
- Integrar persistencia con **SQLite o JSON**.
- Crear panel web de monitoreo en Flask.

---

##  Autora

**Carla Stacchiola**  
 Facultad de Ingeniería 
 Materia: Diseño de Sistemas
 Año: 2025 