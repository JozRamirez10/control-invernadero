# ## ###########################################################
#
# electrovalvula.py
# Clase para el control de la electroválvula
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

import RPi.GPIO as GPIO

class Electrovalvula:
    
    #PIN = 16 por defecto 
    PIN = None
    estado = None

    def __init__(self, pin):
        self.PIN = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.OUT)
        
        # El relé funciona con una lógica inversa, por lo tanto HIGH es apagado
        GPIO.output(self.PIN, GPIO.HIGH) 
        self.estado = False
    
    def prender(self):
        GPIO.output(self.PIN, GPIO.LOW)
        self.estado = True
    
    def apagar(self):
        GPIO.output(self.PIN, GPIO.HIGH)
        self.estado = False