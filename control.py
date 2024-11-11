from entidades import *
from config import *
from servidorWeb.webserver import iniciarServidorWeb

import RPi.GPIO as GPIO

foco = Foco(PIN_CRUCE_CERO_FOCO, PIN_PWM_FOCO)
electrovalvula = Electrovalvula(PIN_ELECTROVALVULA)
ventilador1 = Ventilador(PIN_VENTILADOR1, FRECUENCIA_VENTILADOR)
ventilador2 = Ventilador(PIN_VENTILADOR2, FRECUENCIA_VENTILADOR)
sensor_humedad = SensorHumedad(PIN_SENSOR_HUMEDAD)
sensor_temperatura1 = SensorTemperatura(ID_SENSOR_TEMPERATURA1)
sensor_temperatura2 = SensorTemperatura(ID_SENSOR_TEMPERATURA2)

controlador_pid = ControladorPID(kp=2.0, ki=0.5, kd=0.1, setpoint=SETPOINT_TEMPERATURA)

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

#control_invernadero.run()
iniciarServidorWeb() 
