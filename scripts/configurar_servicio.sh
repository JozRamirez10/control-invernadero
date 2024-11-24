#!/bin/bash

# Ruta del archivo del servicio
SERVICE_PATH="/etc/systemd/system/invernadero.service"

# Contenido del archivo del servicio
SERVICE_CONTENT="[Unit]
Description=Servicio para ejecutar el sistema de invernadero
After=network-online.target
Wants=network-online.target

[Service]
ExecStartPre=/bin/sleep 10
ExecStart=/home/pi/control-invernadero/start.sh
WorkingDirectory=/home/pi/control-invernadero
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root
Environment=PATH=/usr/bin:/usr/local/bin

[Install]
WantedBy=multi-user.target"

# Crear el archivo del servicio
echo "Creando el archivo del servicio en $SERVICE_PATH..."
echo "$SERVICE_CONTENT" | sudo tee $SERVICE_PATH > /dev/null

# Recargar los servicios de systemd para detectar el nuevo servicio
echo "Recargando systemd..."
sudo systemctl daemon-reload

# Habilitar el servicio para que inicie al arrancar el sistema
echo "Habilitando el servicio..."
sudo systemctl enable invernadero.service

# Iniciar el servicio
echo "Iniciando el servicio..."
sudo systemctl start invernadero.service

# Comprobar el estado del servicio
echo "Estado del servicio:"
sudo systemctl status invernadero.service
