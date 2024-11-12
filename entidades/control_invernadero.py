# ## ###########################################################
#
# control_invernadero.py
# Clase para el control del invernadero
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

import time

from grafica import graph

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

    # De acuerdo a la temperatura registrada toma acciones para llegar a la temperatura deseada
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

        # Ejecución de controlador PID
        dt = 1
        salida = self.controlador_pid.controlPID(temperatura_promedio, dt)

        humedad = self.sensor_humedad.obtenerHumedad()
        print(f"Humedad: {humedad}")

        # Grafica de la temperatura y humedad
        graph(temperatura1, temperatura2, humedad)

        # Acciones tomadas por el valor recibido del controlador PID
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

    # Ejecución infinita del control de invernadero
    def run(self):
        try:
            while True:
                if(self.prendido): # El sistema debe estar encendido
                    self.ajustar_control()
                time.sleep(1)
        except Exception as e:
            print(f"Error con el control de invernadero: {e}")
        finally:
            pass

