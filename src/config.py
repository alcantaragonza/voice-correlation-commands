# Configuraciones globales
SAMPLE_RATE = 44100
CHANNELS = 1

# Mapeo maestro de comandos y acciones
# Estructura: "palabra": ["ruta_audio", "tipo_accion", "valor_accion"]
ACTIONS_DICT = {
    "word": {
        "path": "patterns/word.wav",
        "type": "software",
        "action": "start winword"  # Comando para Windows
    },
    "excel": {
        "path": "patterns/excel.wav",
        "type": "software",
        "action": "start excel"
    },
    "meso": {
        "path": "patterns/meso.wav",
        "type": "url",
        "action": "https://www.umes.edu.gt"
    },
    "lampara": {
        "path": "patterns/lampara.wav",
        "type": "hardware",
        "action": "L"  # Carácter que el Arduino recibirá por Serial
    },
    "motor": {
        "path": "patterns/motor.wav",
        "type": "hardware",
        "action": "M"
    }
}