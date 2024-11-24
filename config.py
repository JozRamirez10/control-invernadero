# ## ###########################################################
#
# config.py
# Archivo de configuración de los pines y ids correspondientes al  
# control de los objetos
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

import board

SETPOINT_TEMPERATURA = 22

PIN_CRUCE_CERO_FOCO = 17
PIN_PWM_FOCO = 27

PIN_ELECTROVALVULA = 16

PIN_VENTILADOR1 = 21
PIN_VENTILADOR2 = 14
FRECUENCIA_VENTILADOR = 1000 

PIN_SENSOR_HUMEDAD = board.D26

ID_SENSOR_TEMPERATURA1 = "28-5769001d64ff"
ID_SENSOR_TEMPERATURA2 = "28-9b6c001d64ff"
