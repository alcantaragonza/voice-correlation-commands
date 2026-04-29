import numpy as np
import soundfile as sf
import noisereduce as nr

def limpiar_y_preparar(data, samplerate):
    """
    Limpia el ruido, normaliza y asegura que el audio sea útil.
    """
    # 1. Reducción de ruido por software
    data_clean = nr.reduce_noise(y=data, sr=samplerate)
    
    # 2. Normalización (Escala de -1 a 1)
    if np.max(np.abs(data_clean)) > 0:
        data_clean = data_clean / np.max(np.abs(data_clean))
        
    return data_clean

def cargar_patrones(comandos_dict):
    """
    Carga todos tus archivos .wav en un diccionario de arreglos NumPy.
    """
    patrones_listos = {}
    for nombre, info in comandos_dict.items():
        data, sr = sf.read(info["path"])
        # Solo por seguridad, si es estéreo pasamos a mono
        if len(data.shape) > 1: data = data.mean(axis=1)
        patrones_listos[nombre] = limpiar_y_preparar(data, sr)
    return patrones_listos