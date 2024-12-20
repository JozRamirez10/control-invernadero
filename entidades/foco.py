# ## ###########################################################
#
# foco.py
# Clase para el control del foco incandescente
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

import pigpio
import time

class Foco: 
    PIN_CRUCE_ZERO = None
    PIN_PWM = None

    intensidad = None
    retardo_fase = 0.01

    pigpio_conexion = None

    control = None # False - Automático, True - Manual

    def __init__(self, cruce_zero, pwm):
        
        # Para que el cruce por cero sea registrado como un evento, se debe usar pigpio
        self.pigpio_conexion = pigpio.pi()
        if not self.pigpio_conexion.connected:
            print("No se pudo conectar con pigpiod")
            return
    
        self.control = False
        
        self.PIN_CRUCE_ZERO = cruce_zero
        self.PIN_PWM = pwm
        self.intensidad = 0

        self.pigpio_conexion.set_mode(self.PIN_CRUCE_ZERO, pigpio.INPUT)
        self.pigpio_conexion.set_mode(self.PIN_PWM, pigpio.OUTPUT)

        # Habilita la intensidad del foco en cero
        self.pigpio_conexion.write(self.PIN_PWM, 0)

        # Configura el cruce por cero como un evento
        self.pigpio_conexion.callback(self.PIN_CRUCE_ZERO, pigpio.RISING_EDGE, self.crucePorCero)

    # Ajusta el retardo de fase para el cruce por cero
    def crucePorCero(self, gpio, level, tick):
        if self.intensidad > 0:
            if level == 1:
                retardo = (self.retardo_fase * (100 - self.intensidad)) / 100
                time.sleep(retardo)
                self.pigpio_conexion.write(self.PIN_PWM, 1)
                time.sleep(0.0001)
                self.pigpio_conexion.write(self.PIN_PWM, 0)
        else:
            self.pigpio_conexion.write(self.PIN_PWM, 0)
    
    def prender(self):
        self.intensidad = 100

    def apagar(self):
        self.intensidad = 0
    
    def cambiarIntensidad(self, intensidad):
        if 0 <= intensidad <= 100:
            self.intensidad = intensidad
        else:
            print("Foco: Error al leer valor entre 0 y 100")
    
    def getPotencia(self):
        return self.intensidad

    def setControl(self, valor):
        self.control = valor
    
    def getControl(self):
        return self.control

