# ## ###########################################################
#
# grafica.py
# Genera las gráficas de temperatura
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

import matplotlib.pyplot as plt
import time
import shutil
from datetime import datetime
import pytz

# Almacenamiento de los valores que usa la gráfica
time_graph = []
temp1_graph = []  
temp2_graph = []  
avg_temp_graph = []  
humidity_graph = []  
cont_time = 0  

# Genera la gráfica de temperatura y humedad
def graph(temperatura1, temperatura2, humedad):
    global time_graph, temp1_graph, temp2_graph, avg_temp_graph, humidity_graph, cont_time

    # Obtener el tiempo actual y lo almacena
    cont_time += time.time()
    time_graph.append(cont_time)

    if temperatura1 is None and temperatura2 is None:
        print("Error al obtener el promedio de temperatura")
        temperatura_promedio = 0
    elif temperatura1 is None:
        temperatura_promedio = temperatura2
    elif temperatura2 is None:
        temperatura_promedio = temperatura1
    else:
        try:
            temperatura_promedio = (temperatura1 + temperatura2) / 2
        except Exception as e:
            temperatura_promedio = 0

    avg_temp_graph.append(temperatura_promedio)

    # Agrega las temperaturas individuales y la humedad
    temp1_graph.append(temperatura1)
    temp2_graph.append(temperatura2)
    humidity_graph.append(humedad)

    # Configuración del gráfico
    plt.plot(time_graph, temp1_graph, label='Temperatura 1', marker='o')
    plt.plot(time_graph, temp2_graph, label='Temperatura 2', marker='x')
    plt.plot(time_graph, avg_temp_graph, label='Temperatura Promedio', linestyle='--')
    plt.plot(time_graph, humidity_graph, label='Humedad', linestyle=':')

    # Configuración de los límites y etiquetas
    plt.ylim(-20, 70)  # Rango de temperatura
    plt.title('Gráfica de Temperatura y Humedad')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Valor')
    plt.grid(True)
    
    # Mostrar leyenda
    plt.legend()

    # Guardar la imagen en un archivo PNG
    plt.savefig('img/temperatura_grafica.png', format='png')
    plt.clf()  # Limpiar el gráfico 

# Realiza una copia de la gráfica mostrada en la página
def copiar_grafica():
    imagen_original = "img/temperatura_grafica.png"
    
    # Configurar la zona horaria de México
    timezone = pytz.timezone('America/Mexico_City')
    timestamp = datetime.now(timezone).strftime("%Y%m%d_%H%M%S")
    nombre_copia = f"img/grafica_{timestamp}.png"
    
    # Copiar la imagen
    try:
        shutil.copy(imagen_original, nombre_copia)
        print(f"Copia creada: {nombre_copia}")
    except Exception as e:
        print(f"Error al copiar la imagen: {e}")
