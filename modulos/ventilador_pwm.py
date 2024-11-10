import RPi.GPIO as GPIO
import time

# Izquierda - 21
# Derecha - 14

def iniciarVentilador(pin):
    # Configuración del pin GPIO
    fan_pin = pin  # El pin GPIO al que está conectado el MOSFET
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fan_pin, GPIO.OUT)

    # Configuración de PWM
    pwm_frequency = 1000  # Frecuencia en Hertz (puedes ajustarla si es necesario)
    pwm = GPIO.PWM(fan_pin, pwm_frequency)
    pwm.start(0)
    return pwm

def cambiarPWM(speed, pwm):
    if speed.isdigit():
        speed = int(speed)
        if 0 <= speed <= 100:
            # Establecer el ciclo de trabajo (duty cycle) del PWM
            pwm.ChangeDutyCycle(speed)
            print(f"Velocidad del ventilador ajustada a {speed}%")
        else:
            print("Por favor, ingresa un valor entre 0 y 100.")
    else:
        print("Entrada no válida. Por favor, ingresa un número.")
    
    time.sleep(1)

def ventilador_temp():
    global pwm
    # Inicio de PWM con ciclo de trabajo del 0% (apagado)

    try:
        while True:
            # Obtener la velocidad del ventilador (0-100)
            speed = input("Introduce la velocidad del ventilador (0-100): ")
            
            # Validar la entrada
            if speed.isdigit():
                speed = int(speed)
                if 0 <= speed <= 100:
                    # Establecer el ciclo de trabajo (duty cycle) del PWM
                    pwm.ChangeDutyCycle(speed)
                    print(f"Velocidad del ventilador ajustada a {speed}%")
                else:
                    print("Por favor, ingresa un valor entre 0 y 100.")
            else:
                print("Entrada no válida. Por favor, ingresa un número.")
            
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nPrograma interrumpido")

    finally:
        # Detener PWM y limpiar los pines GPIO
        pwm.stop()
        GPIO.cleanup()
        pass