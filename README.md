# Laboratorio 2-Conexión del robot lego EV3 con ROS

Integrantes: Daniel Felipe Cantor Santana, Giovanni Obregon, Thomas Hernandez Ochoa, Andres Felipe Zuleta Romero

Para realizar la conexión del robot EV3 con ROS, se empleó el protocolo MQTT,para esto se realizaron los siguientes pasos:

## Booteo tarjetas SD
Para no reemplazar, o incluso dañar, el software del robot EV3, se usó una versión de linux compatible con dicho robot mediante el Booteo de una tarjeta SD. Se siguieron los pasos de la página [EV3Dev](https://www.ev3dev.org). Cabe aclarar que al instalar el software en la SD, si se requiere volver al sistema operativo predeterminado, basta con extraer la tarjeta SD del robot.

## Prueba de funcionamiento via Wifi
El primer paso para la conexión del robot es generar y verificar una conexión estable entre el robot y el PC, para esto se compró una antena wifi compatible con el EV3. Nuevamente siguiendo los pasos  disponibles de la página [EV3Dev](https://www.ev3dev.org). La conexión via Wifi pueden verse en la siguiente imagen:


![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Prueba_Wifi.jpg)

Con la conexión establecida, se abrió la consola del robot y se envió un primero código llamado "helloWorld.py" para verificar que la conexión fue existosa.




## Creación del servicio MQTT

![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Servicio_MQTT.png)

![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Suscriptor_MQTT.png)

## Creación paquete de ROS
Por otro lado se creó un paquete en ROS para almacenar los archivos que se utilizarán



## Solución de fallos

## Pruebas de funcionamiento

![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Ejecucion_en_ROS.png)
