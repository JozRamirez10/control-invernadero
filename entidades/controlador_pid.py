# ## ###########################################################
#
# controlador_pid.py
# Clase para el controlador PID
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

class ControladorPID:

    kp = None
    ki = None
    kd = None
    setpoint = None

    # Recibe las variables y el setpoint de la temperatura
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint

        self.error_anterior = 0
        self.integral = 0
    
    # Calcula el valor de acuerdo a la formula de PID
    def controlPID(self, valor_medido, intervalo_tiempo):
        error = self.setpoint - valor_medido
        propocional = self.kp * error
        self.integral += error * intervalo_tiempo
        integral = self.ki * self.integral
        derivativa = self.kd * (error - self.error_anterior) / intervalo_tiempo
        self.error_anterior = error
        salida = propocional + integral + derivativa
        return salida
    
    # Actualiza el setpoint
    def setSetpoint(self, setpoint):
        self.setpoint = setpoint
        modificarTemperaturaArchivoConfig(setpoint)
    
    def getSetpoint(self):
        return self.setpoint
    
def modificarTemperaturaArchivoConfig(valor):
    # Nombre del archivo de configuración
    archivo_config = 'config.py'
    
    # Abrir el archivo para leerlo
    with open(archivo_config, 'r') as file:
        lineas = file.readlines()
    
    # Abrir el archivo en modo escritura para modificarlo
    with open(archivo_config, 'w') as file:
        for linea in lineas:
            # Si encontramos la línea que contiene SETPOINT_TEMPERATURA, la modificamos
            if linea.startswith("SETPOINT_TEMPERATURA"):
                file.write(f"SETPOINT_TEMPERATURA = {valor}\n")
            else:
                file.write(linea)
