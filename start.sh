#!/bin/bash

# Archivo de bandera para verificar si ya se ejecutaron los scripts de configuración
FLAG_FILE="config_done.flag"

# Nombre del programa Python que quieres ejecutar
PROGRAM="webserver.py"

# Verifica si el archivo de bandera existe
if [ ! -f "$FLAG_FILE" ]; then
  echo "Ejecutando dependencias.sh, w1.sh y web.sh por primera vez..."
  sudo bash ./scripts/dependencias.sh
  sudo bash ./scripts/w1.sh
  sudo bash ./scripts/web.sh
  # Crea el archivo de bandera
  touch "$FLAG_FILE"
  echo "Configuración completada. Archivo de bandera creado."

  sudo reboot now
else
  echo "Los scripts de configuración ya se ejecutaron previamente. Omitiendo."
fi

# Ejecuta el programa principal con permisos de superusuario
echo "Ejecutando $PROGRAM con permisos de superusuario..."
sudo python3 "$PROGRAM"

sudo python3 fin.py

echo "Ejecución completada."
