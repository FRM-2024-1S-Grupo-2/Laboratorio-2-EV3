# Laboratorio 2-Conexión del robot lego EV3 con ROS

Integrantes: Daniel Felipe Cantor Santana, Giovanni Obregon, Thomas Hernandez Ochoa, Andres Felipe Zuleta Romero

Para realizar la conexión del robot EV3 con ROS, se empleó el protocolo MQTT,para esto se realizaron los siguientes pasos:

## Booteo tarjetas SD
Para no reemplazar, o incluso dañar, el software del robot EV3, se usó una versión de linux compatible con dicho robot mediante el Booteo de una tarjeta SD. Se siguieron los pasos de la página [EV3Dev](https://www.ev3dev.org). Cabe aclarar que al instalar el software en la SD, si se requiere volver al sistema operativo predeterminado, basta con extraer la tarjeta SD del robot.

## Prueba de funcionamiento via Wifi
El primer paso para la conexión del robot es generar y verificar una conexión estable entre el robot y el PC, para esto se compró una antena wifi compatible con el EV3. Nuevamente siguiendo los pasos  disponibles de la página [EV3Dev](https://www.ev3dev.org). La conexión via Wifi pueden verse en la siguiente imagen:


![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Prueba_Wifi.jpg)


Con la conexión establecida, se abrió la consola del robot y se envió un primero código llamado "helloWorld.py" para verificar que la conexión fue existosa, para eso se creó la siguiente ruta de archivo en el PC:

```cd ~
mkdir pruebas
cd pruebas/
mkdir python
cd python/
mkdir Mov
cd Mov
```


Como puede verse en los siguientes videos:

[![Ver en YouTube](https://img.youtube.com/vi/cxmfSaQ0z-0/maxresdefault.jpg)](https://www.youtube.com/watch?v=cxmfSaQ0z-0)

[![Ver en YouTube](https://img.youtube.com/vi/uahnYYg7ls/maxresdefault.jpg)](https://www.youtube.com/watch?v=uahnYYg7ls)


## Creación del servicio MQTT

La conexión que se busca hacer es implentar un protocolo de comunicación MQTT, por lo tano creamos el servicio:
![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Servicio_MQTT.png)

De ahi, se toman el "URL Cluster" y el puerto ("PORT") que se usarán en los archivos [ev3_MQTT](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Codigos/Archivos_EV3/ev3_MQTT.py) y [GUI](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Codigos/ArchivosPC/GIU_Control.py).

Por último, creamos un suscriptor para activar el servicio,  en este caso tanto su nombre como su contraseña es "LegoEv302"
![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Suscriptor_MQTT.png)

## Creación paquete de ROS
- Estableciendo la conexión via wifi del PC con el EV3, debe actualizarse el apt, justo como se indica en los pasos de 
la pagina [EV3Dev](https://www.ev3dev.org), especificamente, el paso 6.1.

- Una vez 


## Solución de fallos

## Pruebas de funcionamiento

![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Ejecucion_en_ROS.png)

### Video de Demostración

[![Ver en YouTube](https://img.youtube.com/vi/jtdHT5IY994/maxresdefault.jpg)](https://www.youtube.com/watch?v=jtdHT5IY994)


