#!/bin/bash
# ## ###########################################################
#
# web.sh
# Configuración para que la Raspberry Pi funcione
# como un AP
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

# Archivos de configuración
ARCHIVO_DHCPD="/etc/dhcpcd.conf"
ARCHIVO_DNSMASQ="/etc/dnsmasq.conf"
ARCHIVO_HOSTAPD="/etc/hostapd/hostapd.conf"
ARCHIVO_DAMEON_HOSTAPD="/etc/default/hostapd"

# Configuraciones
CONFIG_DHCPD="
interface wlan0
    static ip_address=192.168.1.1/24
    nohook wpa_supplicant
"

CONFIG_DNSMASQ="
interface=wlan0
dhcp-range=192.168.1.2,192.168.1.200,255.255.255.0,24h
"

CONFIG_HOSTAPD="
interface=wlan0
driver=nl80211

ssid=Sistema-Invernadero
wpa_passphrase=12345678
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP

hw_mode=g
channel=5
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
rsn_pairwise=CCMP
"

DAEMON_HOSTAPD='DAEMON_CONF="/etc/hostapd/hostapd.conf"'

# Revisa si la interfaz wlan0 esta bloqueada y la desbloquea
rfkill unblock wlan
ip link set wlan0 up
ifconfig wlan0 up

# Detiene los servicios
systemctl stop dnsmasq
systemctl stop hostapd

# Verificamos si ya existe la configuración
if grep -q "interface wlan0" "$ARCHIVO_DHCPD"; then
    echo "La configuración ya existe en $ARCHIVO_DHCPD."
else
    # Agregamos la configuración al final del archivo
    echo "$CONFIG_DHCPD" | sudo tee -a "$ARCHIVO_DHCPD" > /dev/null
    echo "Configuración agregada exitosamente a $CONFIG_DHCPD."
fi

service dhcpcd restart 

# Verificamos si ya existe alguna de las líneas para evitar duplicados
if grep -q "interface=wlan0" "$ARCHIVO_DNSMASQ" && grep -q "dhcp-range=192.168.1.2,192.168.1.150,255.255.255.0,24h" "$ARCHIVO_DNSMASQ"; then
    echo "La configuración ya existe en $ARCHIVO_DNSMASQ."
else
    # Agregamos el bloque de configuración al final del archivo
    echo "$CONFIG_DNSMASQ" | sudo tee -a "$ARCHIVO_DNSMASQ" > /dev/null
    echo "Configuración agregada exitosamente a $ARCHIVO_DNSMASQ."
fi

systemctl start dnsmasq

# Verifica si la configuración ya existe en el archivo
if grep -q "ssid=Sistema-Invernadero" "$ARCHIVO_HOSTAPD"; then
    echo "La configuración ya existe en $ARCHIVO_HOSTAPD."
else
    # Agrega el bloque de configuración al final del archivo
    echo "$CONFIG_HOSTAPD" | sudo tee -a "$ARCHIVO_HOSTAPD" > /dev/null
    echo "Configuración agregada exitosamente a $ARCHIVO_HOSTAPD."
fi

# Reemplaza la línea que comienza con #DAEMON_CONF o añade la línea si no existe
if grep -q "^#DAEMON_CONF" "$ARCHIVO_DAMEON_HOSTAPD" || grep -q "^DAEMON_CONF" "$ARCHIVO_DAMEON_HOSTAPD"; then
    sudo sed -i 's|^#*DAEMON_CONF=.*|'"$DAEMON_HOSTAPD"'|' "$ARCHIVO_DAMEON_HOSTAPD"
    echo "Línea DAEMON_CONF actualizada en $ARCHIVO_DAMEON_HOSTAPD."
else
    echo "$DAEMON_HOSTAPD" | sudo tee -a "$ARCHIVO_DAMEON_HOSTAPD" > /dev/null
    echo "Línea DAEMON_CONF agregada a $ARCHIVO_DAMEON_HOSTAPD."
fi

# Habilita y levanta el servicio 
systemctl unmask hostapd
systemctl enable hostapd
systemctl start hostapd