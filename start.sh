#!/bin/bash
# ## ###########################################################
#
# start.sh
# Ejecuta todos los scripts para la correcta ejecución del sistema
# de invernadero
#
# Autor: José Ramírez
# License: MIT
#
# ## ###########################################################

# Archivo de bandera para verificar si ya se ejecutaron los scripts de configuración
FLAG_FILE="config_done.flag"

# Nombre del programa Python que levanta toda la aplicación
PROGRAM="servidor_web.py"

# Verifica si el archivo de bandera existe
if [ ! -f "$FLAG_FILE" ]; then
  echo "Ejecutando dependencias.sh, w1.sh y web.sh por primera vez..."
  bash ./scripts/dependencias.sh
  bash ./scripts/w1.sh
  bash ./scripts/web.sh
  
  # Crea el archivo de bandera
  touch "$FLAG_FILE"
  echo "Configuración completada. Archivo de bandera creado."

  # Despues de configurar por primera vez, el sistema se reinicia
  reboot now
else
  echo "Los scripts de configuración ya se ejecutaron previamente. Omitiendo."
fi

# Ejecuta el programa principal con permisos de superusuario
python3 "$PROGRAM"

# Fin de la ejecución del sistema
python3 fin.py

echo "Ejecución completada."
