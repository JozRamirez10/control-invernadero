import adafruit_dht

class SensorHumedad:
    
    sensor = None
    #PIN = board.D26
    PIN = None

    def __init__(self, pin):
        self.PIN = pin
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

    

