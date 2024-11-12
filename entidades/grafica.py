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

    try:
        # Calcula la temperatura promedio
        temperatura_promedio = (temperatura1 + temperatura2) / 2
        avg_temp_graph.append(temperatura_promedio)
    except Exception as e:
        print("Error al obtener el promedio de temperatura")
        temperatura_promedio = 0

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