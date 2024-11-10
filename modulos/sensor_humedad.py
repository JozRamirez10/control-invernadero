import time
import adafruit_dht
import board

dht_device = ''

def iniciarSensorHumedad():
    global dht_device
    dht_device = adafruit_dht.DHT11(board.D26, use_pulseio=False)

def sensor_humedad():
    global dht_device
    contador = 0

    while True:
        try:
            temperature_c = dht_device.temperature
            temperature_f = temperature_c * (9 / 5) + 32

            humidity = dht_device.humidity

            print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature_c, temperature_f, humidity))
            contador += 1
        except RuntimeError as err:
            print(err.args[0])

        time.sleep(2.0)
        if contador == 3:
            return

