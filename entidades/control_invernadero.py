import time
import matplotlib.pyplot as plt

class ControlInvernadero:
    
    prendido = None

    foco = None
    ventilador1 = None
    ventilador2 = None
    electrovalvula = None
    sensor_temperatura1 = None
    sensor_temperatura2 = None
    sensor_humedad = None

    controlador_pid = None
    
    def __init__(self, foco, ventilador1, ventilador2, electrovalvula, sensor_temperatura1,
                sensor_temperatura2, sensor_humedad, controlador_pid):
        self.foco = foco
        self.ventilador1 = ventilador1
        self.ventilador2 = ventilador2
        self.electrovalvula = electrovalvula
        self.sensor_temperatura1 = sensor_temperatura1
        self.sensor_temperatura2 = sensor_temperatura2
        self.sensor_humedad = sensor_humedad
        self.controlador_pid = controlador_pid
        self.prendido = True

    def ajustar_control(self):
        temperatura1 = self.sensor_temperatura1.obtenerTemperatura()
        temperatura2 = self.sensor_temperatura2.obtenerTemperatura()

        if temperatura1 is None or temperatura2 is None:
            print("Error al leer la temperatura")
            return

        try:
            temperatura_promedio = (temperatura1 + temperatura2) / 2
        except Exception as e:
            temperatura_promedio = 0

        print(f"Temperatura: {temperatura_promedio}")
        dt = 1
        salida = self.controlador_pid.controlPID(temperatura_promedio, dt)

        humedad = self.sensor_humedad.obtenerHumedad()
        print(f"Humedad: {humedad}")
        graph(temperatura1, temperatura2, humedad)

        if salida > 0:
            intensidad_foco = min(max(int(salida), 0), 100)
            self.foco.cambiarIntensidad(str(intensidad_foco))
            print(f"Ajustando el foco a {intensidad_foco}")
        else:
            velocidad_ventilador = min(max(int(-salida), 0), 100)
            self.ventilador1.cambiarVelocidad(str(velocidad_ventilador))
            self.ventilador2.cambiarVelocidad(str(velocidad_ventilador))
            self.foco.apagar()
            print(f"Ajustando el ventilador a {velocidad_ventilador}")
        
    def prender(self):
        self.prendido = True

    def apagar(self):
        self.prendido = False
    
    def prenderIrrigacion(self):
        self.electrovalvula.prender()
    
    def apagarIrrigacion(self):
        self.electrovalvula.apagar()

    def run(self):
        try:
            while True:
                if(self.prendido):
                    self.ajustar_control()
                time.sleep(1)
        except Exception as e:
            print(f"Error con el control de invernadero: {e}")
        finally:
            copiar_grafica()


# Inicializamos las listas globales
time_graph = []
temp1_graph = []  # Temperatura 1
temp2_graph = []  # Temperatura 2
avg_temp_graph = []  # Temperatura promedio
humidity_graph = []  # Humedad
cont_time = 0  # Tiempo global

def graph(temperatura1, temperatura2, humedad):
    global time_graph, temp1_graph, temp2_graph, avg_temp_graph, humidity_graph, cont_time

    # Obtener el tiempo actual y agregar a las listas
    cont_time += time.time()
    time_graph.append(cont_time)

    try:
        # Calcular temperatura promedio
        temperatura_promedio = (temperatura1 + temperatura2) / 2
        avg_temp_graph.append(temperatura_promedio)
    except Exception as e:
        print("Error al obtener el promedio de temperatura")
        temperatura_promedio = 0

    # Agregar las temperaturas individuales y la humedad
    temp1_graph.append(temperatura1)
    temp2_graph.append(temperatura2)
    humidity_graph.append(humedad)

    # Configurar el gráfico
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
    plt.clf()  # Limpiar el gráfico para evitar superposición en futuras iteraciones
