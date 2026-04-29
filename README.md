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
En `src/config.py` tienes el diccionario de comandos para mapear las acciones (ej: si detecta "meso", abrir URL).
