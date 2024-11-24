#!/bin/bash
# ## ###########################################################
#
# dependencias.sh
# Instalación de paquetes necesarios para que la aplicación 
# funcione
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

# Instalación por apt
apt install -y python3-venv python3-dev
apt install -y python3-pip
apt install -y python3-rpi.gpio
apt install -y dnsmasq hostapd 
apt install -y pigpio
apt install -y python3-matplotlib

# Instalación por pip3
pip3 install adafruit-circuitpython-dht Adafruit-Blinka
pip3 install -U python-magic
pip3 install pytz

# Habilitación de servicios
systemctl enable pigpiod
systemctl start pigpiod
