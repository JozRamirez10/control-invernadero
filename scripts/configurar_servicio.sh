#!/bin/bash
# ## ###########################################################
#
# configurar_servicio.sh
# Configura el programa como un servicio systemd para que inicie
# siempre que la Raspberry Pi sea encendida
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

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

# Crea el archivo del servicio
echo "Creando el archivo del servicio en $SERVICE_PATH..."
echo "$SERVICE_CONTENT" | sudo tee $SERVICE_PATH > /dev/null

# Recarga los servicios de systemd para detectar el nuevo servicio
echo "Recargando systemd..."
sudo systemctl daemon-reload

# Habilita el servicio para que inicie al arrancar el sistema
echo "Habilitando el servicio..."
sudo systemctl enable invernadero.service

# Inicia el servicio
echo "Iniciando el servicio..."
sudo systemctl start invernadero.service

# Comprueba el estado del servicio
echo "Estado del servicio:"
sudo systemctl status invernadero.service
