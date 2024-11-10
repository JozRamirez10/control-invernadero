from entidades import *
import board
import time
import RPi.GPIO as GPIO
import sys

PIN_CRUCE_CERO_FOCO = 17
PIN_PWM_FOCO = 27

PIN_ELECTROVALVULA = 16

PIN_VENTILADOR1 = 21
PIN_VENTILADOR2 = 14
FRECUENCIA_VENTILADOR = 1000 

PIN_SENSOR_HUMEDAD = board.D26

ID_SENSOR_TEMPERATURA1 = "28-1061021d64ff"
ID_SENSOR_TEMPERATURA2 = "28-9b6c001d64ff"

foco = Foco(PIN_CRUCE_CERO_FOCO, PIN_PWM_FOCO)
electrovalvula = Electrovalvula(PIN_ELECTROVALVULA)
ventilador1 = Ventilador(PIN_VENTILADOR1, FRECUENCIA_VENTILADOR)
ventilador2 = Ventilador(PIN_VENTILADOR2, FRECUENCIA_VENTILADOR)
sensor_humedad = SensorHumedad(PIN_SENSOR_HUMEDAD)
sensor_temperatura1 = SensorTemperatura(ID_SENSOR_TEMPERATURA1)
sensor_temperatura2 = SensorTemperatura(ID_SENSOR_TEMPERATURA2)
menu = "Selecciona una opción:\n  1-Prender y apagar foco\n  2-Irrigacion\n  3-Sensor temperatura\n  4-Sensor humedad\n  5-Ventilador\n  0-Salir\n\n>>"

while True:
    entrada = int(input(menu))
    if entrada == 1:
        intensidad = input("Seleccione la intensidad del foco [0-100]:")
        if intensidad == 0:
            foco.apagar()
        else:
            foco.prender()
            foco.cambiarIntensidad(intensidad)
    
    elif entrada == 2:
        electrovalvula.prender()
        time.sleep(2)
        electrovalvula.apagar()

    elif entrada == 3:
        print(f"{sensor_temperatura1.obtenerTemperatura()}C")
        print(f"{sensor_temperatura2.obtenerTemperatura()}C")
    
    elif entrada == 4:
        print(f"{sensor_humedad.obtenerHumedad()} de humedad")
    
    elif entrada == 5:
        velocidad1 = input("Seleccione la velocidad del ventilador 1 [0-100]:")
        ventilador1.cambiarVelocidad(velocidad1)

        velocidad2 = input("Seleccione la velocidad del ventilador 1 [0-100]:")
        ventilador2.cambiarVelocidad(velocidad2)

    elif entrada == 0:
        GPIO.cleanup()
        sys.exit(0)
