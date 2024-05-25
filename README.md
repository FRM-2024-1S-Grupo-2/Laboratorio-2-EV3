# Laboratorio 2-Conexión del robot lego EV3 con ROS

Integrantes: Daniel Felipe Cantor Santana, Giovanni Obregon, Thomas Hernandez Ochoa, Andres Felipe Zuleta Romero

Para realizar la conexión del robot EV3 con ROS, se empleó el protocolo MQTT,para esto se realizaron los siguientes pasos:

## Booteo tarjetas SD
Para no reemplazar, o incluso dañar, el software del robot EV3, se usó una versión de linux compatible con dicho robot mediante el Booteo de una tarjeta SD. Se siguieron los pasos de la página [EV3Dev](https://www.ev3dev.org). Cabe aclarar que al instalar el software en la SD, si se requiere volver al sistema operativo predeterminado, basta con extraer la tarjeta SD del robot.

## Prueba de funcionamiento via Wifi
El primer paso para la conexión del robot es generar y verificar una conexión estable entre el robot y el PC, para esto se compró una antena wifi compatible con el EV3. Nuevamente siguiendo los pasos  disponibles de la página [EV3Dev](https://www.ev3dev.org). La conexión via Wifi pueden verse en la siguiente imagen:


![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Prueba_Wifi.jpg)

```
ssh robot@<Dirección IP del robot>
```
NOTA: Cada que se pide la contraseña del robot, esta es "maker"


Con la conexión establecida, se abrió la consola del robot y se envió un primero código llamado "helloWorld.py" para verificar que la conexión fue existosa, para eso se creó la siguiente ruta de archivo en el PC:

```cd ~
mkdir pruebas
cd pruebas/
mkdir python
cd python/
mkdir Mov
cd Mov
```
La forma de copiar el archvivo fue, abrirl al terminal del pc donde se tiene el archivo a enviar y usar el siguiente comando:

```
scp pythonHello.py robot@<Dirección IP del robot>:/home/robot/pruebas/python/Mov/
```

Las pruebas de funcionamiento se ven en los siguientes videos:

[![Ver en YouTube](https://img.youtube.com/vi/cxmfSaQ0z-0/maxresdefault.jpg)](https://www.youtube.com/watch?v=cxmfSaQ0z-0)

[![Ver en YouTube](https://img.youtube.com/vi/uahnYYg7ls/maxresdefault.jpg)](https://www.youtube.com/watch?v=uahnYYg7ls)


## Creación del servicio MQTT

La conexión que se busca hacer es implentar un protocolo de comunicación MQTT, por lo tano creamos el servicio:
![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Servicio_MQTT.png)

De ahi, se toman el "URL Cluster" y el puerto ("PORT") que se usarán en los archivos [ev3_MQTT](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Codigos/Archivos_EV3/ev3_MQTT.py) y [GUI](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Codigos/ArchivosPC/GIU_Control.py).

Por último, creamos un suscriptor para activar el servicio,  en este caso tanto su nombre como su contraseña es "LegoEv302"
![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Suscriptor_MQTT.png)

Por ultimo los de la carpeta "archivo Ev3" se enviaron al EV3, no son antes crear una carpeta específica:

```
cd python
mkdir MQTT
```

## Creación paquete de ROS
- Estableciendo la conexión via wifi del PC con el EV3, debe actualizarse el apt, justo como se indica en los pasos de 
la pagina [EV3Dev](https://www.ev3dev.org), especificamente, el paso 6.1.

- Instalamos python y python3 al Ev3

    ```
    sudo apt install python3
    ```
    ```
    sudo apt install python
    ```

- Deben instalarse las librerias necesarias en el robot:
    ```
    cd ~
    mkdir Librerias
    git clone https://github.com/ev3dev/ev3dev-lang-python.git
    cd ~/librerias/ev3dev-lang-python
    sudo python3 setup.py install
    ```
- Ahora creamos el workspace, en la carpeta que se quiera:
    ```
    mkdir lab_rm_ws/src
    ```
- Almacenamos los archivos de a carpeta "Archivos PC" en la carpeta "src"
- Se creó un paquete 
    ```
    catkin_create_pkg <nombre_del_paquete> [dependencias]
    ```
-  Y por ultimo se realiza el comando "cat kin build"

    ```
    cd ~/lab_rm_ws
    catkin build
    ```

## Pruebas de funcionamiento
Con todo debidamente configurado es necesario inicializar 3 terminales
- La primera se inicia ros 
    ```
    roscore
    ```
- En la segunda se inicia la conexión  con el robot y se corre el archivo "ev3_MQTT.PY"
    ```
    cd ~
    cd pruebas
    cd pruebas/python/MQTT
    python3 ev3_MQTT.py

    ```
- La tercera terminal se abre dentro del workspace y se corre la interfa gráfica
    ```
    source devel/setup.bash
    python3 GUI_Control.py
    ```
Como se ve en la siguiente figura:
![imagen](https://github.com/FRM-2024-1S-Grupo-2/Laboratorio-2-EV3/blob/main/Imagenes/Ejecucion_en_ROS.png)

### Video de Demostración
Ya con todo en funcionamiento, puede verse el resultado en el siguiente video:

[![Ver en YouTube](https://img.youtube.com/vi/jtdHT5IY994/maxresdefault.jpg)](https://www.youtube.com/watch?v=jtdHT5IY994)


