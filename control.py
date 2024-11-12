import RPi.GPIO as GPIO
import threading
import time

from entidades import *
from config import *

def iniciarControl():
    foco = Foco(PIN_CRUCE_CERO_FOCO, PIN_PWM_FOCO)
    electrovalvula = Electrovalvula(PIN_ELECTROVALVULA)
    ventilador1 = Ventilador(PIN_VENTILADOR1, FRECUENCIA_VENTILADOR)
    ventilador2 = Ventilador(PIN_VENTILADOR2, FRECUENCIA_VENTILADOR)
    sensor_humedad = SensorHumedad(PIN_SENSOR_HUMEDAD)
    sensor_temperatura1 = SensorTemperatura(ID_SENSOR_TEMPERATURA1)
    sensor_temperatura2 = SensorTemperatura(ID_SENSOR_TEMPERATURA2)

    controlador_pid = ControladorPID(kp=2.2, ki=0.7, kd=0.2, setpoint=SETPOINT_TEMPERATURA)

    control_invernadero = ControlInvernadero(
        foco, 
        ventilador1, 
        ventilador2, 
        electrovalvula, 
        sensor_temperatura1,
        sensor_temperatura2,
        sensor_humedad,
        controlador_pid
    )
    return control_invernadero

def ejecutarControl(control_invernadero):
    try:
        control_invernadero.run()
    except Exception as e:
        pass
    finally:
        print("Adios")
        GPIO.cleanup()

def modificarSistema(control_invernadero, accion):
    if accion:
        control_invernadero.prender()
    else:
        control_invernadero.apagar()

def modificarIrrigacion(control_invernadero, accion):
    if accion:
        control_invernadero.prenderIrrigacion()
    else:
        control_invernadero.apagarIrrigacion()



 
