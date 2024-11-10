class ControladorPID:

    kp = None
    ki = None
    kd = None
    setpoint = None

    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint

        self.error_anterior = 0
        self.integral = 0
    
    def controlPID(self, valor_medido, intervalo_tiempo):
        error = self.setpoint - valor_medido
        propocional = self.kp * error
        self.integral += error * intervalo_tiempo
        integral = self.ki * self.integral
        derivativa = self.kd * (error - self.error_anterior) / intervalo_tiempo
        self.error_anterior = error
        salida = propocional + integral + derivativa
        return salida
    