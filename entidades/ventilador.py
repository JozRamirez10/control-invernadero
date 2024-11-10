import RPi.GPIO as GPIO

class Ventilador:

    PIN = None
    pwm = None
    frecuencia = None

    def __init__(self, pin, frecuencia):
        self.PIN = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.OUT)

        self.frecuencia = frecuencia
        self.pwm = GPIO.PWM(self.PIN, self.frecuencia)
        self.pwm.start(0)
    
    def cambiarVelocidad(self, velocidad):
        if velocidad.isdigit():
            velocidad = int(velocidad)
            if 0 <= velocidad <= 100:
                self.pwm.ChangeDutyCycle(velocidad)
            else:
                print("Ventilador: Error al leer valor entre 0 y 100")
        else:
            print("Ventilador: Error al cambiar la velocidad")
        
    def detener(self):
        self.pwm.stop()