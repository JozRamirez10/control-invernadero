import sys

from calefaccion_pwm import *
from irrigacion import *
from temperatura import *
from sensor_humedad import *
from ventilador_pwm import *

iniciarCalefaccion()
iniciarIrrigacion()
iniciarSensorHumedad()
ventiladorIzq = iniciarVentilador(21)
ventiladorDer = iniciarVentilador(14)

menu = "Selecciona una opción:\n  1-Prender y apagar foco\n  2-Irrigacion\n  3-Sensor temperatura\n  4-Sensor humedad\n  5-Ventilador\n  0-Salir\n\n>>"

while True:
    entrada = int(input(menu))
    if entrada == 1:
        calefaccion()
    elif entrada == 2:
        irrigacion()
    elif entrada == 3:
        sensor_temperatura()
    elif entrada == 4:
        sensor_humedad()
    elif entrada == 5:
        ventilador = int(input("Selecciona un ventilador:\n  1-Izquierda\n  2-Derecha\n\n>> "))
        speed = input("Introduce la velocidad del ventilador (0-100): ")
        pwm = None
        
        if(ventilador == 1):
            pwm = ventiladorIzq
        elif(ventilador == 2):
            pwm = ventiladorDer
        
        cambiarPWM(speed, pwm)
    elif entrada == 0:
        sys.exit(0)