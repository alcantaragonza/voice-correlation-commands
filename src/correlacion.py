# src/correlacion.py
# P2 - Correlacion y reconocimiento de comandos de voz
# Teoria de Sistemas - Universidad Mesoamericana

import numpy as np
import sounddevice as sd
from scipy.signal import resample

from config import SAMPLE_RATE, CHANNELS, ACTIONS_DICT, SAMPLE_RATE_CORRELACION
from prepocessing import cargar_patrones, limpiar_y_preparar

DURACION_GRABACION = 2.5   # segundos que se graba al usuario

def igualar_longitud(a, b):
    """
    Rellena con ceros el arreglo más corto para que ambos
    tengan la misma longitud antes de correlacionar.
    Sin esto, np.correlate puede dar resultados incorrectos
    si los audios tienen duraciones distintas.
    """
    diff = len(a) - len(b)
    if diff > 0:
        b = np.pad(b, (0, diff))
    elif diff < 0:
        a = np.pad(a, (0, -diff))
    return a, b


def reducir_tasa_muestreo(audio, sr_original, sr_destino):
    """Reduce muestras antes de correlacionar para mayor velocidad."""
    num_muestras_nuevo = int(len(audio) * sr_destino / sr_original)
    return resample(audio, num_muestras_nuevo)


def calcular_correlacion(patron, entrada):
    """
    Correlación cruzada entre el patrón pregrabado y la entrada del usuario.

    Fórmula discreta:
        R[k] = sum( patron[n] * entrada[n+k] )

    Se usa mode='full' para evaluar todos los desplazamientos posibles.
    Retorna el valor máximo absoluto, que indica el nivel de similitud.
    Un valor más alto = mayor parecido entre las dos señales.
    """
    # Reducir tasa ANTES de igualar longitud
    p = reducir_tasa_muestreo(patron, SAMPLE_RATE, SAMPLE_RATE_CORRELACION)
    e = reducir_tasa_muestreo(entrada, SAMPLE_RATE, SAMPLE_RATE_CORRELACION)
    p, e = igualar_longitud(p.copy(), e.copy())
    correlacion = np.correlate(p, e, mode='full')
    return float(np.max(np.abs(correlacion)))

def grabar_entrada_usuario():
    """
    Graba audio del micrófono durante DURACION_GRABACION segundos.
    Retorna un arreglo numpy float32 limpio y normalizado (mono).
    """
    print(f"[GRABANDO] Habla ahora... ({DURACION_GRABACION}s)")
    grabacion = sd.rec(
        int(DURACION_GRABACION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='float32'
    )
    sd.wait()
    print("[OK] Grabacion finalizada.")

    audio = grabacion.flatten()
    audio = limpiar_y_preparar(audio, SAMPLE_RATE)
    return audio


def reconocer_comando(patrones):
    """
    Flujo completo de reconocimiento:
      1. Graba la voz del usuario
      2. Correlaciona contra todos los patrones cargados
      3. Retorna el nombre del comando con mayor correlación

    Parámetros:
        patrones (dict): resultado de cargar_patrones(), 
                         { "word": array, "excel": array, ... }

    Retorna:
        str: nombre del comando reconocido (key de ACTIONS_DICT)
        None: si no se pudo grabar o todos los valores son 0
    """
    entrada = grabar_entrada_usuario()

    if np.max(np.abs(entrada)) == 0:
        print("[ERROR] El audio grabado esta vacio o en silencio.")
        return None

    print("\n[CORRELACIONES]")
    resultados = {}
    for nombre, patron in patrones.items():
        valor = calcular_correlacion(patron, entrada)
        resultados[nombre] = valor
        print(f"  {nombre:<12}: {valor:.6f}")

    # El comando con el valor de correlacion más alto
    mejor_comando = max(resultados, key=resultados.get)
    mejor_valor   = resultados[mejor_comando]

    print(f"\n[RECONOCIDO] '{mejor_comando}' (correlacion maxima: {mejor_valor:.6f})")
    return mejor_comando