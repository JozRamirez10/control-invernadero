import RPi.GPIO as GPIO
import time

RELAY_PIN = 16

def iniciarIrrigacion():
    # Configurar el modo de numeración de pines
    GPIO.setmode(GPIO.BCM)

    # Configurar el pin del relé como salida
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    GPIO.output(RELAY_PIN, GPIO.HIGH)


def irrigacion():

    try:
        # Encender el relé (está normalmente LOW, pero depende de tu módulo)
        GPIO.output(RELAY_PIN, GPIO.LOW)
        print("Relé encendido")
        time.sleep(2)  # Esperar 2 segundos

        # Apagar el relé
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Relé apagado")
        time.sleep(2)  # Esperar 2 segundos
        

    except KeyboardInterrupt:
        print("Programa interrumpido")

    finally:
        # Limpiar la configuración de los pines GPIO al finalizar
        #GPIO.cleanup()
        pass
