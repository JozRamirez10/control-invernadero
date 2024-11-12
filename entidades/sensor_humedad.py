# ## ###########################################################
#
# sensor_humedad.py
# Clase para el control del sensor de humedad (DHT11)
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

import adafruit_dht

class SensorHumedad:
    
    #PIN = board.D26 por defecto
    PIN = None
    sensor = None

    def __init__(self, pin):
        self.PIN = pin
        # Configura el sensor de humedad
        self.sensor = adafruit_dht.DHT11(self.PIN , use_pulseio=False)
    
    def obtenerTemperatura(self):
        try:
            return self.sensor.temperature
        except Exception as e:
            print(e)

    def obtenerHumedad(self):
        try:
            return self.sensor.humidity
        except Exception as e:
            print(e)

    

