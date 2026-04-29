import sys
import os

# Para que Python encuentre los módulos dentro de /src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import ACTIONS_DICT
from prepocessing import cargar_patrones
from correlacion import reconocer_comando
from hardware_acciones import conectar_arduino, esperar_pulsador, ejecutar_accion


def main():
    print("=" * 50)
    print("  SISTEMA DE RECONOCIMIENTO DE COMANDOS DE VOZ")
    print("  Universidad Mesoamericana - Teoria de Sistemas")
    print("=" * 50)

    # Cargar patrones una sola vez al inicio
    print("\n[INICIO] Cargando patrones de voz...")
    patrones = cargar_patrones(ACTIONS_DICT)
    print(f"[OK] {len(patrones)} patrones cargados: {list(patrones.keys())}")

    # Conectar Arduino
    arduino = conectar_arduino()

    # Bucle principal
    while True:
        print("\n" + "-" * 50)

        # Esperar pulsador (o salir si hay timeout)
        if not esperar_pulsador(arduino):
            continue

        # Grabar + correlacionar + reconocer
        comando = reconocer_comando(patrones)

        # Ejecutar acción
        if comando:
            ejecutar_accion(comando, arduino)

        # Continuar o salir
        respuesta = input("\n¿Continuar? (s/n): ").strip().lower()
        if respuesta == 'n':
            break

    if arduino and arduino.is_open:
        arduino.close()
    print("\n[FIN] Sistema cerrado.")


if __name__ == "__main__":
    main()