# ## ###########################################################
#
# fin.py
# Acciones antes de que se detenga el servidor
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

import shutil
from datetime import datetime
import RPi.GPIO as GPIO

# Realiza una copia de la gráfica mostrada en la página
def copiar_grafica():
    imagen_original = "img/temperatura_grafica.png"
    
    # TIMESTAMP para distinguir cada imagen por su fecha de creación
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_copia = f"img/grafica_{timestamp}.png"
    
    # Copiar la imagen
    try:
        shutil.copy(imagen_original, nombre_copia)
        print(f"Copia creada: {nombre_copia}")
    except Exception as e:
        print(f"Error al copiar la imagen: {e}")

# Termina la ejecución de los pines GPIO
GPIO.cleanup
copiar_grafica()