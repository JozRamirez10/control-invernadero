# ## ###########################################################
#
# sensor_temperatura.py
# Clase para el control de sensores de temperatura (DS18B20)
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

class SensorTemperatura:
    
    id = None
    temperatura = None

    def __init__(self, id):
        self.id = id
    
    # Obtiene el valor de temperatura de archivos específicos 
    # usados por el bus 1-Wire
    def obtenerTemperatura(self):
        try:
            archivoTemperatura = open(f'/sys/bus/w1/devices/{self.id}/temperature', "r")
            archivoTemperatura.seek(0) # Coloca el cursor al inicio
            self.temperatura = int(archivoTemperatura.read())
            self.temperatura = self.temperatura/1000 
            archivoTemperatura.close()
        except Exception as e:
            print(f"Error al leer el archivo de temperatura con id: {self.id}")
            self.temperatura = None
        finally:
            return self.temperatura