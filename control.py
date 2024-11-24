# ## ###########################################################
#
# control.py
# Control del invernadero
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

import RPi.GPIO as GPIO

from entidades import *
from config import *


# Configura todas las entidades y las adjunta al Control Invernadero
def iniciarControl():
    foco = Foco(PIN_CRUCE_CERO_FOCO, PIN_PWM_FOCO)
    electrovalvula = Electrovalvula(PIN_ELECTROVALVULA)
    ventilador1 = Ventilador(PIN_VENTILADOR1, FRECUENCIA_VENTILADOR)
    ventilador2 = Ventilador(PIN_VENTILADOR2, FRECUENCIA_VENTILADOR)
    sensor_humedad = SensorHumedad(PIN_SENSOR_HUMEDAD)
    sensor_temperatura1 = SensorTemperatura(ID_SENSOR_TEMPERATURA1)
    sensor_temperatura2 = SensorTemperatura(ID_SENSOR_TEMPERATURA2)

    controlador_pid = ControladorPID(kp=15, ki=5, kd=10, setpoint=SETPOINT_TEMPERATURA)

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

# Pone en funcionamiento el control de invernadero
def ejecutarControl(control_invernadero):
    try:
        control_invernadero.run()
    except Exception as e:
        pass
    finally:
        GPIO.cleanup()

# Prende o apaga el sistema
def modificarSistema(control_invernadero, accion):
    if accion:
        control_invernadero.prender()
    else:
        control_invernadero.apagar()

# Prende o apaga el sistema de irrigación
def modificarIrrigacion(control_invernadero, accion):
    if accion:
        control_invernadero.prenderIrrigacion()
    else:
        control_invernadero.apagarIrrigacion()

def modificarTemperaturaObjetivo(control_invernadero, valor):
    control_invernadero.modificarTemperaturaObjetivo(valor)

def modificarVentilador1(control_invernadero, valor):
    control_invernadero.modificarVentilador1(valor)

def modificarVentilador2(control_invernadero, valor):
    control_invernadero.modificarVentilador2(valor)

def modificarControlVentilador1(control_invernadero, valor):
    control_invernadero.modificarControlVentilador1(valor)

def modificarControlVentilador2(control_invernadero, valor):
    control_invernadero.modificarControlVentilador2(valor)

def modificarControlFoco(control_invernadero, valor):
    control_invernadero.modificarControlFoco(valor)

def modificarFoco(control_invernadero, valor):
    control_invernadero.modificarFoco(valor)

def almacenarGrafica(control_invernadero):
    control_invernadero.almacenarGrafica()


 
