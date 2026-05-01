# voice-correlation-commands
Voice command recognition system using cross-correlation in Python, with hardware control via Arduino. | Sistema de reconocimiento de comandos de voz mediante correlación cruzada en Python, con control de hardware vía Arduino. 

# Proyecto Reconocimiento de Voz

## Información para el Equipo:
- **P1 (Audio):** Audios listos en `/patterns`.
- **Frecuencia (FS):** 44100 Hz (Mono).
- **Librerías necesarias:** `pip install numpy soundfile noisereduce sounddevice`

### Instrucciones para P2 (Lógica):
Usa `src/preprocessing.py` para cargar los patrones. Los arreglos ya vienen normalizados de -1 a 1. La correlación debe hacerse sobre estos arreglos.

Graba la voz del usuario (disparada por un pulsador físico en Arduino), la compara contra 4 patrones de audio pregrabados usando **correlación cruzada discreta** con NumPy, identifica el comando dicho y ejecuta la acción correspondiente — todo sin APIs externas.

### Comandos disponibles

| Comando     | Acción                                  |
|-------------|------------------------------------------|
| `word`      | Abre Microsoft Word                      |
| `excel`     | Abre Microsoft Excel                     |
| `meso`      | Abre `umes.edu.gt` en el navegador       |
| `lampara`   | Enciende la lámpara vía relé (Arduino)   |
| `motor`     | Activa el motor por 1 segundo (Arduino)  |

***

## Estructura del proyecto

```
voice-correlation-commands/
├── main.py                   ← Punto de entrada del sistema
├── patterns/
│   ├── word.wav
│   ├── excel.wav
│   ├── meso.wav
│   ├── lampara.wav
│   └── motor.wav
├── arduino/
│   └── arduino_voz.ino       ← Sketch para Arduino UNO/Nano
└── src/
    ├── __init__.py
    ├── config.py             ← Configuración global y diccionario de acciones
    ├── prepocessing.py       ← P1: carga y limpieza de audio
    ├── correlacion.py        ← P2: grabación, correlación y reconocimiento
    └── hardware_acciones.py  ← P3: Serial, Arduino y ejecución de acciones
```

***

## Instalación

```bash
git clone https://github.com/tu-usuario/voice-correlation-commands.git
cd voice-correlation-commands
pip install numpy soundfile noisereduce sounddevice pyserial
```

***

## Uso

```bash
python main.py
```

1. El sistema carga los patrones de voz al inicio
2. Conecta automáticamente con el Arduino por Serial
3. Espera que el usuario presione el pulsador físico
4. Graba 2.5 segundos de audio
5. Calcula la correlación cruzada contra los 5 patrones
6. Ejecuta la acción del comando con mayor correlación

***

## Hardware requerido

| Componente         | Conexión en Arduino |
|--------------------|---------------------|
| Pulsador           | Pin 2 + GND (INPUT_PULLUP) |
| Módulo Relé 5V     | Pin 7               |
| Motor DC / Lámpara | Conectado al relé   |
| Cable USB          | Comunicación Serial con Python |

Cargar `arduino/arduino_voz.ino` con el IDE de Arduino antes de ejecutar el script.

***

## Dependencias

| Librería       | Uso                                      |
|----------------|------------------------------------------|
| `numpy`        | Correlación cruzada y normalización      |
| `sounddevice`  | Grabación de audio desde el micrófono    |
| `soundfile`    | Lectura de archivos `.wav`               |
| `noisereduce`  | Reducción de ruido espectral             |
| `pyserial`     | Comunicación Serial con Arduino          |
| `scipy`        | Resamplear muestras                      |

***

## Cómo funciona la correlación

La similitud entre el patrón pregrabado `p[n]` y la entrada del usuario `e[n]` se mide con la correlación cruzada discreta:

```
R[k] = Σ p[n] · e[n+k]
```

El comando cuyo `max|R[k]|` sea mayor es el reconocido. Todos los audios se **normalizan** a [-1, 1] antes de correlacionar para que el reconocimiento dependa de la forma de la señal y no del volumen.

***

## Notas para el equipo

- **Frecuencia de muestreo:** 44100 Hz, canal único (Mono)
- **Patrones:** grabados y limpiados en Audacity, listos en `/patterns`
- **Preprocesamiento:** `src/prepocessing.py` entrega los arreglos ya normalizados — úsalos directamente en la correlación
- **Diccionario de acciones:** `src/config.py` contiene el mapeo completo de comandos → acciones; úsalo como referencia para ejecutar la acción correcta tras el reconocimiento

***

## Universidad Mesoamericana — Quetzaltenango

**Curso:** Teoría de Sistemas
**Entrega:** 30 de abril de 2026

**Miembros del Equipo:**

| # | Nombre |
|---|--------|
| 1 | Brayan Alexander de León Pereira | 202308112 |
| 2 | Bryan Alexander Pérez Santos | 202208024 |
| 3 | Andrés Fernando González Alcántara | 202308061 |
