import pigpio
import time

class Foco: 
    PIN_CRUCE_ZERO = None
    PIN_PWM = None

    intensidad = None
    retardo_fase = 0.01

    pigpio_conexion = None

    def __init__(self, cruce_zero, pwm):
        self.pigpio_conexion = pigpio.pi()
        if not self.pigpio_conexion.connected:
            print("No se pudo conectar con pigpiod")
            return
        
        self.PIN_CRUCE_ZERO = cruce_zero
        self.PIN_PWM = pwm
        self.intensidad = 0

        self.pigpio_conexion.set_mode(self.PIN_CRUCE_ZERO, pigpio.INPUT)
        self.pigpio_conexion.set_mode(self.PIN_PWM, pigpio.OUTPUT)

        self.pigpio_conexion.write(self.PIN_PWM, 0)
        self.pigpio_conexion.callback(self.PIN_CRUCE_ZERO, pigpio.RISING_EDGE, self.crucePorCero)

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
        if intensidad.isdigit():
            intensidad = int(intensidad)
            if 0 <= intensidad <= 100:
                self.intensidad = intensidad
            else:
                print("Foco: Error al leer valor entre 0 y 100")
        else:
            print("Foco: Error al cambiar la intensidad")

