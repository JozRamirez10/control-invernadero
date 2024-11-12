import shutil
from datetime import datetime
import RPi.GPIO as GPIO

def copiar_grafica():
    # Nombre de la imagen original
    imagen_original = "img/temperatura_grafica.png"
    
    # Generar un nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_copia = f"img/grafica_{timestamp}.png"
    
    # Copiar el archivo
    try:
        shutil.copy(imagen_original, nombre_copia)
        print(f"Copia creada: {nombre_copia}")
    except Exception as e:
        print(f"Error al copiar la imagen: {e}")

GPIO.cleanup
copiar_grafica()