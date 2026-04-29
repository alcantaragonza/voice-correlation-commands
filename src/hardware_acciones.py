# Modulo para la parte fisica del sistema 
import serial
import serial.tools.list_ports
import os
import webbrowser
import time

# Importo las configuraciones de P1
from config import ACTIONS_DICT

# Configuracion de la comunicacion serial
BAUD_RATE   = 9600   # tiene que ser igual al del sketch
TIMEOUT_SEG = 10     # cuanto espero al pulsador antes de cancelar

# Busca el puerto donde esta conectado el Arduino
def detectar_puerto_arduino():
    puertos = serial.tools.list_ports.comports()
    for p in puertos:
        # Pruebo varios nombres porque depende del driver
        if "Arduino" in p.description or "CH340" in p.description or "USB Serial" in p.description:
            return p.device
    return None


# Abre la conexion con el Arduino
def conectar_arduino():
    puerto = detectar_puerto_arduino()
    if puerto is None:
        print("[ERROR] No se encontro el Arduino")
        return None
    
    try:
        arduino = serial.Serial(puerto, BAUD_RATE, timeout=1)
        time.sleep(2)   # espero que el Arduino se reinicie despues de abrir el puerto
        print(f"[OK] Arduino conectado en {puerto}")
        return arduino
    except serial.SerialException as e:
        print(f"[ERROR] No se pudo abrir el puerto: {e}")
        return None


# Se queda esperando a que el usuario presione el pulsador fisico
def esperar_pulsador(arduino):
    print("[ESPERANDO] Presiona el pulsador para grabar...")
    inicio = time.time()
    
    while True:
        # Reviso si llego algo desde el Arduino
        if arduino.in_waiting > 0:
            linea = arduino.readline().decode("utf-8").strip()
            if linea == "P":
                print("[OK] Pulsador detectado, arrancando grabacion.")
                return True
        
        # Si paso mucho tiempo sin que aprieten nada, salgo
        if time.time() - inicio > TIMEOUT_SEG:
            print("[TIMEOUT] No se presiono el pulsador a tiempo.")
            return False
        
        time.sleep(0.05)   # para no quemar el procesador


# Manda la señal al Arduino para activar el rele (lampara o motor)
def activar_accion_fisica(arduino, señal):
    if arduino:
        arduino.write(señal.encode())
        print(f"[ARDUINO] Señal '{señal}' enviada al rele.")


# Abre una aplicacion del sistema
def abrir_aplicacion(comando):
    print(f"[ACCION] Abriendo aplicacion: {comando}")
    os.system(comando)   # esto es para Windows
    # Si fuera Linux seria: os.system(f"xdg-open {comando}")


# Abre una URL en el navegador por defecto
def abrir_url(url):
    print(f"[ACCION] Abriendo URL: {url}")
    webbrowser.open(url)


# Funcion principal: recibe el comando que reconocio P2 y ejecuta lo que toque
def ejecutar_accion(nombre_comando, arduino):
    if nombre_comando not in ACTIONS_DICT:
        print(f"[ERROR] El comando '{nombre_comando}' no se encuentra en el diccionario.")
        return
    
    accion = ACTIONS_DICT[nombre_comando]
    
    if accion["type"] == "software":
        abrir_aplicacion(accion["action"])
    elif accion["type"] == "url":
        abrir_url(accion["action"])
    elif accion["type"] == "hardware":
        activar_accion_fisica(arduino, accion["action"])
    else:
        print(f"[ERROR] Tipo de accion desconocido: {accion['tipo']}")