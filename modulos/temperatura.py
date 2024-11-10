from time import sleep

id_sensor1 = "28-1061021d64ff" # Izquierda
id_sensor2 = "28-9b6c001d64ff" # Derecha

def leer_sensor(id_sensor):
    try:
        archivoTemperatura = open(f'/sys/bus/w1/devices/{id_sensor}/temperature', "r")
        archivoTemperatura.seek(0) # Coloca el cursor al inicio del archivo
        temperatura = int(archivoTemperatura.read())
        temperatura = temperatura / 1000
        archivoTemperatura.close()
        return temperatura
    except Exception as e:
        print(e)
    finally:
        archivoTemperatura.close()

def sensor_temperatura():
    contador = 0
    while(True):
        temp1 = leer_sensor(id_sensor1)
        temp2 = leer_sensor(id_sensor2)
        print(f'Sensor 1: {temp1}C; Sensor 2: {temp2} ')
        sleep(1)
        contador += 1
        if contador == 3:
            return
