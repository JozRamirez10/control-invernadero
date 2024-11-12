import RPi.GPIO as GPIO

class Electrovalvula:
    
    #PIN = 16  
    PIN = None
    estado = None

    def __init__(self, pin):
        self.PIN = pin
        # Configurar el modo de numeración de pines
        GPIO.setmode(GPIO.BCM)
        # Configurar el pin del relé como salida
        GPIO.setup(self.PIN, GPIO.OUT)
        GPIO.output(self.PIN, GPIO.HIGH)
        self.estado = False
    
    def prender(self):
        GPIO.output(self.PIN, GPIO.LOW)
        self.estado = True
    
    def apagar(self):
        GPIO.output(self.PIN, GPIO.HIGH)
        self.estado = False