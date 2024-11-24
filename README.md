# Sistema embebido: Control de invernadero

## Descripción

El sistema está diseñado para que, mediante un controlador PID, pueda tomar deciciones y logre alcanzar una temperatura objetivo. Para ello se apoya del uso de un foco incandescente, ventiladores y sensores de temperatura. Además, permite tener control de un sistema de irrigación para el paso del agua. 
El sistema también ofrece la posiblidad de guardar todos los registros en un histórico que el usuario puede consultar.
La aplcación se despliega mediante una interfaz web y los dispositivos son controlados por los puertos GPIO de Raspberry Pi.

## Funcionalidades

- Controlador PID.
- Permite definir la temperatura objetivo.
- Ajuste de intensidad de foco incandescente.
- Ajuste de ventiladores.
- Lector de sensores de temperatura.
- Lector de sensor de humedad.
- Gráfica de temperatura en tiempo real.
- Almacénamiento de históricos.
- Control y monitoreo a través de aplicación web.

## Aplicación

La aplicación web permite tener un monitoreo en tiempo real de la temperatura y toma de decisiones para los ajustes del foco y ventiladores. Si se desea, estos periféricos se pueden ajustar manualmente.
También ofrece el control de encendido/apagado tanto del invernadero como del sistema de irrigación.

![Captura de pantalla 2024-11-23 a la(s) 23 12 51](https://github.com/user-attachments/assets/93fcd5e8-19af-47ec-b70f-8a7c8a81738c)

## Ejecución

Da permisos de ejecución al script 'start.sh'
```
chmod +x start.sh
```

Ejecuta con privilegios de root el script 'start.sh'
```
sudo ./start.sh
```

La primera vez que se ejecute el script va a instalar todas los paquetes y dependencias, además de configurar los archivos correspondientes para su ejecución.
Cuando terminé de configurar, el sistema se va a reiniciar y cuando terminé de iniciarse habrá creado su propia red "Sistema-Invernadero".
Para acceder a la aplicación web, la dirección es: 192.168.1.1:8080

Para comprobar que el sistema funciona correctamente:
```
sudo systemctl status invernadero.service
```

## Video demostrativo

Puedes acceder al siguiente video en [YouTube](https://youtu.be/Qtefp4gEyoY)

---

## Autores

- Jose Miguel Ramírez González
- Rojas Garcia Marco Daniel

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
