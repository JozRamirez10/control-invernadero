import time

class ControlInvernadero:
    
    foco = None
    ventilador1 = None
    ventilador2 = None
    electrovalvula = None
    sensor_temperatura1 = None
    sensor_temperatura2 = None
    sensor_humedad = None

    controlador_pid = None
    
    def __init__(self, foco, ventilador1, ventilador2, electrovalvula, sensor_temperatura1,
                sensor_temperatura2, sensor_humedad, controlador_pid):
        self.foco = foco
        self.ventilador1 = ventilador1
        self.ventilador2 = ventilador2
        self.electrovalvula = electrovalvula
        self.sensor_temperatura1 = sensor_temperatura1
        self.sensor_temperatura2 = sensor_temperatura2
        self.sensor_humedad = sensor_humedad
        self.controlador_pid = controlador_pid

    def ajustar_control(self):
        temperatura1 = self.sensor_temperatura1.obtenerTemperatura()
        temperatura2 = self.sensor_temperatura2.obtenerTemperatura()

        if temperatura1 is None or temperatura2 is None:
            print("Error al leer la temperatura")
            return

        temperatura_promedio = (temperatura1 + temperatura2) / 2

        print(f"Temperatura: {temperatura_promedio}")
        dt = 1
        salida = self.controlador_pid.controlPID(temperatura_promedio, dt)

        if salida > 0:
            intensidad_foco = min(max(int(salida), 0), 100)
            self.foco.cambiarIntensidad(str(intensidad_foco))
            print(f"Ajustando el foco a {intensidad_foco}")
        else:
            velocidad_ventilador = min(max(int(-salida), 0), 100)
            self.ventilador1.cambiarVelocidad(str(velocidad_ventilador))
            self.ventilador2.cambiarVelocidad(str(velocidad_ventilador))
            self.foco.apagar()
            print(f"Ajustando el ventilador a {velocidad_ventilador}")
    
    def run(self):
        try:
            while True:
                self.ajustar_control()
                time.sleep(1)
        except Exception as e:
            print(f"Error con el control de invernadero: {e}")