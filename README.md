# voice-correlation-commands
Voice command recognition system using cross-correlation in Python, with hardware control via Arduino. | Sistema de reconocimiento de comandos de voz mediante correlación cruzada en Python, con control de hardware vía Arduino. 

# Proyecto Reconocimiento de Voz

## Información para el Equipo:
- **P1 (Audio):** Audios listos en `/patterns`.
- **Frecuencia (FS):** 44100 Hz (Mono).
- **Librerías necesarias:** `pip install numpy soundfile noisereduce sounddevice`

### Instrucciones para P2 (Lógica):
Usa `src/preprocessing.py` para cargar los patrones. Los arreglos ya vienen normalizados de -1 a 1. La correlación debe hacerse sobre estos arreglos.

### Instrucciones para P3 (Integración):
**Archivos entregados:**
    - `src/hardware_acciones.py` → comunicación serial con Arduino y ejecución de acciones
    - `arduino/arduino_voz.ino` → sketch para detectar el pulsador y controlar el rele
    
**Hardware requerido:**
    - Arduino Uno
    - Pulsador (conectado al pin 2)
    - Modulo rele de 5V (conectado al pin 7)
    - Motor o lampara de 12V (conectado al rele)
    - Cable USB para comunicacion serial

**Funciones disponibles para integrar:**
    - `conectar_arduino()` → busca y abre el puerto serial
    - `esperar_pulsador(arduino)` → espera la señal "P" del Arduino
    - `ejecutar_accion(nombre_comando, arduino)` → ejecuta la accion segun el comando reconocido

**Comandos serial:**
    - Arduino → PC: envia `"P"` cuando se presiona el pulsador
    - PC → Arduino: envia `"L"` para lampara o `"M"` para motor


