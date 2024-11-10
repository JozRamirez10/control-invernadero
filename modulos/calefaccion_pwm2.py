import pigpio
import time

# Configuración de pines y variables
ZERO_CROSS_PIN = 17    # Pin GPIO para el cruce por cero
PWM_CONTROL_PIN = 27   # Pin GPIO conectado al control del dimmer
pi = pigpio.pi()       # Conexión al demonio pigpiod

if not pi.connected:
    print("No se pudo conectar con pigpiod.")
    exit()

# Configuración inicial
pi.set_mode(ZERO_CROSS_PIN, pigpio.INPUT)
pi.set_mode(PWM_CONTROL_PIN, pigpio.OUTPUT)
pi.write(PWM_CONTROL_PIN, 0)  # Asegura que esté apagado inicialmente

# Variables de control de brillo
brightness = 50       # Valor de brillo inicial (0 a 100)
delay_max = 0.01      # Máximo retardo en segundos para ángulo de fase

def zero_cross_callback(gpio, level, tick):
    """
    Callback para detectar el cruce por cero y aplicar retardo
    según el brillo configurado.
    """
    if brightness > 0:  # Solo genera pulsos si el brillo es mayor que 0
        if level == 1:  # Detecta el borde ascendente (RISING)
            delay = (delay_max * (100 - brightness)) / 100  # Ajusta el retardo
            time.sleep(delay)                               # Aplica el retardo
            pi.write(PWM_CONTROL_PIN, 1)                    # Activa el pulso
            time.sleep(0.0001)                              # Duración breve del pulso
            pi.write(PWM_CONTROL_PIN, 0)                    # Apaga el pulso
    else:
        pi.write(PWM_CONTROL_PIN, 0)  # Si el brillo es 0, apaga el foco inmediatamente

# Funciones para encender y apagar el foco
def turn_on():
    """
    Enciende el foco a un valor de brillo predefinido.
    """
    global brightness
    brightness = 100  # Brillo al máximo
    print(f"Foco encendido con brillo al {brightness}%")
    
def turn_off():
    """
    Apaga el foco.
    """
    global brightness
    brightness = 0  # Brillo apagado
    print("Foco apagado")

# Configura la detección de cruce por cero
pi.callback(ZERO_CROSS_PIN, pigpio.RISING_EDGE, zero_cross_callback)

try:
    while True:
        # Solicita al usuario que ingrese un valor de brillo
        action = input("Ingrese 'on' para encender, 'off' para apagar, o un valor de brillo (0-100): ").strip().lower()
        
        if action == 'on':
            turn_on()
        elif action == 'off':
            turn_off()
        elif action.isdigit():
            brightness = int(action)
            if 0 <= brightness <= 100:
                print(f"Brillo ajustado a: {brightness}%")
            else:
                print("Por favor, ingrese un valor entre 0 y 100.")
        else:
            print("Acción no válida. Por favor, ingrese 'on', 'off' o un valor de brillo entre 0 y 100.")

except KeyboardInterrupt:
    print("Apagando...")

finally:
    pi.stop()  # Detiene el demonio pigpio
