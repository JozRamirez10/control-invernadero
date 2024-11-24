# ## ###########################################################
#
# ventilador.py
# Clase para el control del ventilador (5V)
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

import RPi.GPIO as GPIO

class Ventilador:

    PIN = None
    pwm = None
    frecuencia = None
    potencia = None
    control = None # False - Automático, True - Manual

    def __init__(self, pin, frecuencia):
        self.PIN = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.OUT)

        self.frecuencia = frecuencia
        self.pwm = GPIO.PWM(self.PIN, self.frecuencia)
        self.control = False
        self.pwm.start(0)
    
    def cambiarVelocidad(self, velocidad):
        self.pwm.start(0)
        if 0 <= velocidad <= 100:
            self.pwm.ChangeDutyCycle(velocidad)
            self.potencia = velocidad
        else:
            print("Ventilador: Error al leer valor entre 0 y 100")
        
    def detener(self):
        self.pwm.stop()
        self.potencia = 0
    
    def getPotencia(self):
        if(self.potencia == None):
            return 0
        return self.potencia
    
    def setControl(self, valor):
        self.control = valor
    
    def getControl(self):
        return self.control