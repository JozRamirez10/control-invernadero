# ## ###########################################################
#
# servidor_web.py
# Levanta el servidor web e inicia el control del invernadero
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import mimetypes
import threading

from urllib.parse import urlparse  # Importar urlparse para manejar la URL
from http.server import BaseHTTPRequestHandler, HTTPServer

from control import *

# Dirección IP del servidor web
address = "192.168.1.1"
# Puerto para atender solicitudes HTTP
port = 8080

class ServidorWeb(BaseHTTPRequestHandler):    
    def _serve_file(self, rel_path):
        # Ignora parámetros en la URL
        parsed_path = urlparse(rel_path)
        # Obtuebe solo la ruta del archivo
        file_path = parsed_path.path  

        if not os.path.isfile(file_path):
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            print(f"Archivo no encontrado: {file_path}")
            return

        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        self.send_response(200)
        self.send_header("Content-type", mime_type)
        self.end_headers()
        try:
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
        except Exception as e:
            print(f"Error al servir el archivo {file_path}: {e}")

    # Obtiene la interfaz de usuario: index.html
    def _serve_ui_file(self):
        ui_path = "web/index.html"
        if not os.path.isfile(ui_path):
            err = "index.html no encontrado."
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(err, "utf-8"))
            print(err)
            return

        try:
            with open(ui_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
            print(f"Servido {ui_path} correctamente.")
        except Exception as e:
            content = f"Error leyendo {ui_path}: {e}"
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))

    # Definición de funciones con las que interactúa el usuario
    def _parse_post(self, json_obj):
        if 'action' not in json_obj:
            return
        switcher = {
            'modificarSistema': modificar_sistema,
            'modificarIrrigacion' : modificar_irrigacion,
        }
        print(json_obj)
        func = switcher.get(json_obj['action'], None)
        if func:
            print(f'\tLlamando {func.__name__}({json_obj["value"]})')
            func(json_obj['value'])

    # Controla las solicitudes GET recibidas por el usuario
    def do_GET(self):
        if self.path == '/':
            self.send_response(200) # OK
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self._serve_ui_file()
        # Ell usuario solicita la temperatura
        if self.path == '/get_temperatura':
            data = {
                "temperatura": obtenerTemperatura()
            }
            self.send_response(200) # OK
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return
        # El usuario solicita la humedad
        if self.path == '/get_humedad':
            data = {
                "humedad": obtenerHumedad()
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return
        # El ususario solicita el estado del sistema
        if self.path == '/get_estado':
            data = {
                "estado": estadoSistema()
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return
        # El usuario solicita el estado de irrigación
        if self.path == '/get_estado_irrigacion':
            data = {
                "estado": estadoIrrigacion()
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return
        else:
            self._serve_file(self.path[1:])

    # Controla las solicitudes POST recibidas por el usuario
    def do_POST(self):
        # Obtener la longitud del contenido
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length < 1:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # Permite cualquier origen
            self.end_headers()
            response = {"error": "No se recibió ningún dato."}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        # Leer los datos recibidos
        post_data = self.rfile.read(content_length)

        try:
            # Decodificar y procesar el JSON recibido
            jobj = json.loads(post_data.decode("utf-8"))
            self._parse_post(jobj)

            # Enviar una respuesta de éxito
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # Permite cualquier origen
            self.end_headers()
            response = {"status": "éxito", "mensaje": "Acción procesada correctamente."}
            self.wfile.write(json.dumps(response).encode("utf-8"))

        except json.JSONDecodeError:
            # Manejar errores de decodificación JSON
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            response = {"error": "JSON inválido."}
            self.wfile.write(json.dumps(response).encode("utf-8"))

        except Exception as e:
            # Manejar cualquier otro tipo de error
            print(f"Error al procesar POST: {e}")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            response = {"error": "Error interno del servidor."}
            self.wfile.write(json.dumps(response).encode("utf-8"))

# Levanta el servidor web y atiende peticiones
def iniciarServidorWeb():
    servidorWeb = HTTPServer((address, port), ServidorWeb)
    print("Servidor iniciado")
    print(f"\tAtendiendo solicitudes en http://{address}:{port}")

    try:
        # Mantiene al servidor web ejecutándose en segundo plano
        servidorWeb.serve_forever()
    except KeyboardInterrupt:
        # Maneja la interrupción de cierre CTRL+C
        print("\nInterrupción recibida, deteniendo servidor...")
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        # Detiene el servidor web cerrando todas las conexiones
        servidorWeb.server_close()
        # Reporta parada del servidor web en consola
        print("Servidor detenido.")

# Obtiene la temperatura promedio
def obtenerTemperatura():
    global control
    try:
        temperatura = (control.sensor_temperatura1.obtenerTemperatura() + control.sensor_temperatura2.obtenerTemperatura()) / 2
    except Exception:
        return "Error"
    return temperatura

def obtenerHumedad():
    global control
    return control.sensor_humedad.obtenerHumedad()

def estadoSistema():
    global control
    if control.prendido:
        return "Encendido"
    else:
        return "Apagado"

def estadoIrrigacion():
    global control
    if control.electrovalvula.estado:
        return "Encendido"
    else:
        return "Apagado"

# Prende o apaga el sistema, depende de la accion
def modificar_sistema(accion):
    global control
    modificarSistema(control, accion)

# Prende o apaga el sistema de irrigación, depende de la accion
def modificar_irrigacion(accion):
    global control
    modificarIrrigacion(control, accion)

# Inicia el control del invernadero
control = iniciarControl()

# Ejecuta el control del invernadero y el servidor web en hilos independientes
#hilo_control = threading.Thread(target=ejecutarControl, args=(control,))
hilo_servidor = threading.Thread(target=iniciarServidorWeb)

#hilo_control.start()
hilo_servidor.start()




