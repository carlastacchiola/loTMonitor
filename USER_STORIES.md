# Historias de Usuario - Sistema de Monitoreo Ambiental IoT

**Proyecto**: PythonIoTMonitor  
**Versión**: 1.0.0  
**Fecha**: Noviembre 2025  
**Metodología**: User Story Mapping  

---

## Índice

1. [Epic 1: Gestión de Zonas y Sensores](#epic-1-gestión-de-zonas-y-sensores)
2. [Epic 2: Registro y Lectura de Sensores](#epic-2-registro-y-lectura-de-sensores)
3. [Epic 3: Sistema de Control Ambiental Automático](#epic-3-sistema-de-control-ambiental-automático)
4. [Epic 4: Gestión de Usuarios y Monitoreo Manual](#epic-4-gestión-de-usuarios-y-monitoreo-manual)
5. [Epic 5: Persistencia y Auditoría de Datos](#epic-5-persistencia-y-auditoría-de-datos)
6. [Historias Técnicas (Patrones de Diseño)](#historias-técnicas-patrones-de-diseño)

---

## Epic 1: Gestión de Zonas y Sensores

### US-001: Registrar Zona Ambiental

**Como** administrador del sistema  
**Quiero** registrar una zona con su nombre, ubicación y tipo de ambiente  
**Para** poder asociarle sensores y monitorear sus condiciones  

#### Criterios de Aceptación

- [x] Una zona debe tener:
  - Nombre único  
  - Ubicación (texto descriptivo)  
  - Tipo de ambiente (interior, exterior, laboratorio, oficina, etc.)  
- [x] No puede haber dos zonas con el mismo nombre  
- [x] El sistema valida que los datos sean consistentes  
- [x] Las zonas deben poder modificarse posteriormente  

#### Detalles Técnicos

**Clase**: `Zona` (`python_iotmonitor/entidades/zona.py`)  
**Servicio**: `ZonaService` (`python_iotmonitor/servicios/zona_service.py`)  

**Código de ejemplo:**
```python
from python_iotmonitor.servicios.zona_service import ZonaService

zona_service = ZonaService()
zona = zona_service.crear_zona(
    nombre="Laboratorio Central",
    ubicacion="Edificio A - Planta 2",
    tipo_ambiente="interior"
)
```

**Validaciones:**
```python
zona.set_tipo_ambiente("exterior")  # OK
zona.set_tipo_ambiente("")  # ValueError: tipo de ambiente no puede ser vacío
```

**Trazabilidad**: `main.py` líneas 40-45

---

### US-002: Asociar Sensores a una Zona

**Como** técnico de mantenimiento  
**Quiero** vincular sensores a una zona existente  
**Para** poder registrar las mediciones correspondientes a ese ambiente  

#### Criterios de Aceptación

- [x] Una zona puede tener múltiples sensores asociados  
- [x] Cada sensor debe tener:
  - ID único  
  - Tipo (temperatura, humedad, CO₂, luz)  
  - Rango de lectura válido  
- [x] No se pueden duplicar sensores del mismo tipo en una misma zona  
- [x] El sistema debe validar la existencia de la zona  

#### Detalles Técnicos

**Clase**: `Sensor` (`python_iotmonitor/entidades/sensor.py`)  
**Servicio**: `SensorService` (`python_iotmonitor/servicios/sensor_service.py`)  

**Código de ejemplo:**
```python
from python_iotmonitor.servicios.sensor_service import SensorService

sensor_service = SensorService()
sensor_temp = sensor_service.crear_sensor("Temperatura", rango_min=-10, rango_max=60)
zona.agregar_sensor(sensor_temp)
```

**Trazabilidad**: `main.py` líneas 47-58

---

### US-003: Registrar Red de Monitoreo Completa

**Como** administrador del sistema  
**Quiero** registrar una red de zonas y sensores  
**Para** tener una estructura inicial de monitoreo ambiental  

#### Criterios de Aceptación

- [x] La red debe incluir:
  - Lista de zonas  
  - Lista de sensores activos  
  - Identificador único de red  
- [x] Cada zona debe tener al menos un sensor  
- [x] Los sensores deben poder listarse globalmente  

#### Detalles Técnicos

**Clase**: `RedMonitoreo` (`python_iotmonitor/entidades/red_monitoreo.py`)  
**Servicio**: `RedMonitoreoService` (`python_iotmonitor/servicios/red_service.py`)  

**Código de ejemplo:**
```python
red_service = RedMonitoreoService()
red = red_service.crear_red("Red Principal")
red.agregar_zona(zona)
```

**Trazabilidad**: `main.py` líneas 60-70

---

## Epic 2: Registro y Lectura de Sensores

### US-004: Crear Sensores mediante Factory Method

**Como** arquitecto de software  
**Quiero** crear sensores sin conocer sus clases concretas  
**Para** centralizar la lógica de creación y evitar código duplicado

#### Criterios de Aceptación

- [x] Soportar creación de:
  - Sensor de Temperatura
  - Sensor de Humedad
  - Sensor de CO₂
  - Sensor de Luz
- [x] Usar diccionario de factories en lugar de `if/elif`
- [x] Lanzar `ValueError` si el tipo de sensor no existe

#### Detalles Técnicos

**Clase**: `SensorFactory` (`python_iotmonitor/patrones/factory/sensor_factory.py`)  
**Patrón**: Factory Method

**Código de ejemplo:**
```python
from python_iotmonitor.patrones.factory.sensor_factory import SensorFactory

sensor = SensorFactory.crear_sensor("Temperatura")
print(sensor.get_tipo())  # "Temperatura"
```

**Trazabilidad**: `main.py` líneas 78-90

---

### US-005: Simular Lectura de Sensores

**Como** sistema de monitoreo  
**Quiero** generar lecturas periódicas de los sensores  
**Para** simular condiciones ambientales en tiempo real

#### Criterios de Aceptación

- [x] Cada sensor debe generar valores dentro de su rango válido
- [x] Las lecturas deben almacenarse como `Medición`
- [x] Cada lectura contiene:
  - Valor medido
  - Fecha y hora
  - Tipo de sensor
  - ID de zona
- [x] Debe poder obtenerse el histórico de lecturas

#### Detalles Técnicos

**Clase**: `Medicion` (`python_iotmonitor/entidades/medicion.py`)  
**Servicio**: `SensorService.registrar_medicion()`

**Código de ejemplo:**
```python
from datetime import datetime

valor = sensor.leer_valor()
sensor_service.registrar_medicion(sensor, valor, datetime.now())
```

**Trazabilidad**: `main.py` líneas 92-102

---

## Epic 3: Sistema de Control Ambiental Automático

### US-006: Implementar Observer entre Sensores y Control Central

**Como** ingeniero de control  
**Quiero** que el Control Central reciba notificaciones de cada sensor  
**Para** reaccionar automáticamente ante cambios ambientales

#### Criterios de Aceptación

- [x] Cada sensor actúa como `Observable[float]`
- [x] El Control Central implementa `Observer[float]`
- [x] Al detectar un valor fuera de rango, notifica al servicio de control
- [x] Se soportan múltiples observadores por sensor

#### Detalles Técnicos

**Clase**: `ControlAmbiental` (`python_iotmonitor/servicios/control_service.py`)  
**Patrón**: Observer

**Código de ejemplo:**
```python
sensor_temp.agregar_observador(control_ambiental)
sensor_humedad.agregar_observador(control_ambiental)
```

**Trazabilidad**: `main.py` líneas 110-125

---

### US-007: Aplicar Estrategias de Respuesta Automática

**Como** sistema automatizado  
**Quiero** decidir qué acción tomar ante condiciones críticas  
**Para** mantener el confort ambiental y evitar alertas

#### Criterios de Aceptación

- [x] Estrategias implementadas:
  - `VentilarStrategy` → si CO₂ alto
  - `EnfriarStrategy` → si temperatura alta
  - `HumidificarStrategy` → si humedad baja
  - `AjustarLuzStrategy` → si luz fuera de rango
- [x] Estrategias deben implementarse bajo interfaz `ControlStrategy`
- [x] El sistema elige e inyecta la estrategia adecuada

#### Detalles Técnicos

**Clases**:
- `ControlStrategy` (interfaz)
- `VentilarStrategy`, `EnfriarStrategy`, `HumidificarStrategy`, `AjustarLuzStrategy`  
**Ubicación**: `python_iotmonitor/patrones/strategy/`

**Código de ejemplo:**
```python
from python_iotmonitor.patrones.strategy.enfriar_strategy import EnfriarStrategy

estrategia = EnfriarStrategy()
estrategia.ejecutar(sensor)
```

**Trazabilidad**: `main.py` líneas 127-145

---

### US-008: Implementar Registro Global de Sensores (Singleton)

**Como** desarrollador del sistema  
**Quiero** mantener un registro único de sensores activos  
**Para** garantizar consistencia en las lecturas y evitar duplicados

#### Criterios de Aceptación

- [x] Debe existir una única instancia de `SensorRegistry`
- [x] Usar inicialización perezosa y `Lock` thread-safe
- [x] Proveer métodos:
  - `registrar_sensor()`
  - `obtener_sensor(id)`
  - `listar_sensores()`

#### Detalles Técnicos

**Clase**: `SensorRegistry` (`python_iotmonitor/patrones/singleton/sensor_registry.py`)  
**Patrón**: Singleton

**Código de ejemplo:**
```python
from python_iotmonitor.patrones.singleton.sensor_registry import SensorRegistry

registry = SensorRegistry.get_instance()
registry.registrar_sensor(sensor_temp)
```

**Trazabilidad**: `main.py` líneas 150-160

---

## Epic 4: Gestión de Usuarios y Monitoreo Manual

### US-009: Registrar Usuarios del Sistema

**Como** administrador  
**Quiero** registrar usuarios con roles (admin, técnico, observador)  
**Para** asignar permisos diferenciados en el monitoreo

#### Criterios de Aceptación

- [x] Cada usuario debe tener:
  - Nombre completo
  - Rol (admin, técnico, observador)
  - Clave de acceso
- [x] Los roles definen permisos de lectura/escritura

**Clase**: `Usuario` (`python_iotmonitor/entidades/usuario.py`)  
**Servicio**: `UsuarioService` (`python_iotmonitor/servicios/usuario_service.py`)

---

### US-010: Visualizar Lecturas Manualmente

**Como** observador del sistema  
**Quiero** consultar lecturas de una zona específica  
**Para** monitorear el comportamiento ambiental

#### Criterios de Aceptación

- [x] Permitir filtrar lecturas por zona, tipo de sensor o rango de fechas
- [x] Mostrar promedio, mínimo y máximo de las últimas lecturas

**Clase**: `ControlAmbientalService`  
**Método**: `mostrar_datos_zona()`

**Código de ejemplo:**
```python
control_service.mostrar_datos_zona("Laboratorio Central")
```

**Trazabilidad**: `main.py` líneas 162-175

---

## Epic 5: Persistencia y Auditoría de Datos

### US-011: Persistir Red de Monitoreo

**Como** administrador del sistema  
**Quiero** guardar la red completa de sensores y zonas  
**Para** mantener el estado del sistema entre ejecuciones

#### Criterios de Aceptación

- [x] Usar `pickle` para serializar la red
- [x] Guardar en carpeta `data/` con extensión `.dat`
- [x] Crear carpeta si no existe
- [x] Mostrar mensaje de confirmación

**Servicio**: `RedMonitoreoService.persistir()`  
**Constantes**:
```python
DIRECTORIO_DATA = "data"
EXTENSION_DATA = ".dat"
```

---

### US-012: Cargar Red Persistida

**Como** auditor del sistema  
**Quiero** cargar una red guardada previamente  
**Para** recuperar las zonas y sensores del monitoreo anterior

#### Criterios de Aceptación

- [x] Verificar existencia del archivo
- [x] Lanzar `PersistenciaException` si no se encuentra
- [x] Restaurar relaciones entre zonas y sensores

**Servicio**: `RedMonitoreoService.leer_red()`

---

## Historias Técnicas (Patrones de Diseño)

### US-TECH-001: Implementar Singleton en SensorRegistry
### US-TECH-002: Implementar Factory Method en SensorFactory
### US-TECH-003: Implementar Observer entre Sensores y ControlAmbiental
### US-TECH-004: Implementar Strategy en Estrategias de Control

---

## Resumen de Cobertura Funcional

| Epic | Historias | Completadas | Cobertura |
|------|-----------|-------------|-----------|
| Epic 1: Zonas y Sensores | 3 | 3 | 100% |
| Epic 2: Lecturas de Sensores | 2 | 2 | 100% |
| Epic 3: Control Automático | 3 | 3 | 100% |
| Epic 4: Usuarios y Monitoreo | 2 | 2 | 100% |
| Epic 5: Persistencia | 2 | 2 | 100% |
| Historias Técnicas | 4 | 4 | 100% |
| **TOTAL** | **16** | **16** | **100%** |

### Patrones de Diseño Cubiertos

- **Singleton** – `SensorRegistry`
- **Factory Method** – `SensorFactory`
- **Observer** – Comunicación Sensor → ControlAmbiental
- **Strategy** – Estrategias de acción ante condiciones ambientales

---

**Última actualización:** Noviembre 2025  
**Estado:** COMPLETO  
**Cobertura funcional:** 100%