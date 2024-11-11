#!/bin/bash

# Nombre del entorno virtual
ENV_DIR="env"
# Nombre del programa Python que quieres ejecutar
PROGRAM="control.py"

# Verifica si el entorno virtual ya existe
if [ ! -d "$ENV_DIR" ]; then
  echo "Creando entorno virtual en $ENV_DIR..."
  python3 -m venv "$ENV_DIR"
  echo "Activando el entorno virtual e instalando dependencias..."
  source "$ENV_DIR/bin/activate"
  bash ./scripts/dependencias.sh
  bash ./scripts/w1.sh
  bash ./scripts/web.sh
else
  echo "Entorno virtual encontrado en $ENV_DIR."
  # Activa el entorno virtual
  source "$ENV_DIR/bin/activate"
fi

# Ejecuta el programa
echo "Ejecutando $PROGRAM..."
python3 "$PROGRAM"

# Desactiva el entorno virtual
deactivate
echo "Ejecución completada."
