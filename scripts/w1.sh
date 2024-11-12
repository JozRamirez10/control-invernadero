#!/bin/bash
# ## ###########################################################
#
# w1.sh
# Habilita el bus 1-Wire
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

archivo_configuracion="/boot/config.txt"
linea_w1="dtoverlay=w1-gpio"

# Verificar si la línea ya existe en el archivo
if grep -Fxq "$linea_w1" "$archivo_configuracion"; then
    echo "La línea '$linea_w1' ya existe en $archivo_configuracion."
else
    echo "La línea '$linea_w1' no se encontró. Agregando al final del archivo..."
    # Agregar la línea al final del archivo de configuración
    echo "$linea_w1" | sudo tee -a "$archivo_configuracion" > /dev/null
fi
