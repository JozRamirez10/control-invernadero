#!/usr/bin/env python3
# ## ###############################################
#
# webserver.py
# Starts a custom webserver and handles all requests
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import mimetypes
from urllib.parse import urlparse  # Importar urlparse para manejar la URL
from http.server import BaseHTTPRequestHandler, HTTPServer

# Nombre o dirección IP del sistema anfitrión del servidor web
address = "192.168.1.1"
# Puerto en el cual el servidor estará atendiendo solicitudes HTTP
# El default de un servidor web en produción debe ser 80
port = 8080

class WebServer(BaseHTTPRequestHandler):
    def _serve_file(self, rel_path):
        # Ignorar parámetros en la URL
        parsed_path = urlparse(rel_path)
        file_path = parsed_path.path  # Obtener solo la ruta del archivo

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

    def _serve_ui_file(self):
        ui_path = os.path.join(os.path.dirname(__file__), "index.html")
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

    def _parse_post(self, json_obj):
        if 'action' not in json_obj or 'value' not in json_obj:
            return
        switcher = {
            'direction': direction,
            'velocity' : velocity,
            'grades'   : grades
        }
        func = switcher.get(json_obj['action'], None)
        if func:
            print(f'\tLlamando {func.__name__}({json_obj["value"]})')
            func(json_obj['value'])

    """do_GET controla todas las solicitudes recibidas vía GET, es
    decir, páginas. Por seguridad, no se analizan variables que lleguen
    por esta vía"""
    def do_GET(self):
        # Revisamos si se accede a la raiz.
        # En ese caso se responde con la interfaz por defecto
        if self.path == '/':
            # 200 es el código de respuesta satisfactorio (OK)
            # de una solicitud
            self.send_response(200)
            # La cabecera HTTP siempre debe contener el tipo de datos mime
            # del contenido con el que responde el servidor
            self.send_header("Content-type", "text/html")
            # Fin de cabecera
            self.end_headers()
            # Por simplicidad, se devuelve como respuesta el contenido del
            # archivo html con el código de la página de interfaz de usuario
            self._serve_ui_file()
        else:
            self._serve_file(self.path[1:])

    """do_POST controla todas las solicitudes recibidas vía POST, es
    decir, envíos de formulario. Aquí se gestionan los comandos para
    la Raspberry Pi"""
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


def iniciarServidorWeb():
    webServer = HTTPServer((address, port), WebServer)
    print("Servidor iniciado")
    print(f"\tAtendiendo solicitudes en http://{address}:{port}")

    try:
        # Mantiene al servidor web ejecutándose en segundo plano
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Maneja la interrupción de cierre CTRL+C
        print("\nInterrupción recibida, deteniendo servidor...")
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        # Detiene el servidor web cerrando todas las conexiones
        webServer.server_close()
        # Reporta parada del servidor web en consola
        print("Servidor detenido.")

