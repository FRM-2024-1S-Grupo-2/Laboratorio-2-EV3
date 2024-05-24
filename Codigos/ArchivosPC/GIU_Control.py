#!/usr/bin/env python3

"""
Nombre del programa: GIU_Control.py
Autor: Juan Sebastian Daleman Martinez
Curso: Fundamentos de robotica movil
Departamento de Ingeniería Mecánica y Mecatrónica
Universidad Nacional de Colombia - Sede Bogotá
Año: 2024-1S.

Programa para el control de un robot Ev3 usando el sistema ev3dev
a traves de una GIU para el usuario y mensajes jason por protocolo MQTT
para el manejo de motores y obtención de datos de un giro sensor.
Este programa esta basado en la serie de videos de: David Fisher 
https://www.youtube.com/watch?v=ZKR8pdr7CnI
"""

#Impotación de las librerias necesarias
import tkinter
from tkinter import ttk
import rospy
import math
from geometry_msgs.msg import Twist
import json
import paho.mqtt.client as paho
from collections.abc import Iterable
from paho import mqtt

#Creación de la clase personalizada para la recepción de mensajes MQTT
class MyDelegate(object):

    """ Los metodos de esta clase seran los que procesen los mensajes MQTT recibidos
        los atributos seran elementos de control necesarios en el procesamiento """

    def __init__(self):

        #label donde se presentara los datos de orientación dado por el giro sensor
        self.label = None

        #Variable de control para la actualización de la orientación del turtlesim
        self.Orientation = 0

        #Elementos para el mensaje del control de la tortuga de turtlesim
        self.cmd_vel_msg = Twist()
        self.cmd_vel_msg.linear.x = 0
        self.cmd_vel_msg.linear.y = 0
    """
    def setlabel(self,label):
        #Función para declaración de label que se usara para datos del giro sensor
        self.label = label
    """
    def print_message(self, message):
        #Función para procesamiento de mensaje recibido de tipo "print_message"

        #Impression del mesaje recibido
        print("Message received:", message)
    """
    def Angle(self, angle):
        #Función para procesamiento de mensaje recibido de tipo "Angle"

        #Se pone el angulo en convencion anti-horaria
        angle = angle*-1
        #Actualización del label de presentación e impresion del angulo recibido
        self.label.config(text=str(angle))
        print("Angle received:", angle)
        
        #Declaración de velocidad angular del mensaje para el turtlesim 
        self.cmd_vel_msg.angular.z = 0

        #Verificación orientación y actualizar el valor según el valor recibido de angulo 
        if self.Orientation != angle:
            self.cmd_vel_msg.angular.z = ((angle-self.Orientation)*(math.pi/180))
            self.Orientation = angle

        # Publicación del mensaje Twist para el control de la tortuga
        turtle_vel_pub.publish(self.cmd_vel_msg)
    """

#Dirección IP del broker MQTT usado por defecto
mqtt_broker_ip_address = "3e4254d24aca4a2185849d5b0a0487b0.s1.eu.hivemq.cloud"

#Declaración de número de indentificación del robot
Lego_ID = 1

class MqttClient(object):
    def __init__(self, delegate=None):
        #Declaración del cliente y un delegado opcional de manejo de datos
        self.client = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION2, client_id="", userdata=None, protocol=paho.MQTTv5)
        self.delegate = delegate

        #Declaración de topico de suscripción y publicación 
        self.subscription_topic_name = None
        self.publish_topic_name = None

        #Declaración de puerto de conexión del broker MQTT
        self.port = 8883

    def connect_to_ev3(self, mqtt_broker_ip_address=mqtt_broker_ip_address, lego_robot_number=Lego_ID):
        #Función para conectarse al Ev3
        #Sufijos para conectar el PC al Ev3
        self.connect("msgPC", "msgLegoEv3", mqtt_broker_ip_address, lego_robot_number)

    def connect_to_pc(self, mqtt_broker_ip_address=mqtt_broker_ip_address, lego_robot_number=Lego_ID):
        #Función para conectarse al PC
        #Sufijos para conectar el EV3 al PC
        self.connect("msgLegoEv3", "msgPC", mqtt_broker_ip_address, lego_robot_number)

    def connect(self, subscription_suffix, publish_suffix, mqtt_broker_ip_address=mqtt_broker_ip_address, lego_robot_number=Lego_ID):
        
        #Declaración de ID del robot y sufijos necesarios para el topico MQTT
        Robot_name = "LegoEV3" + str(lego_robot_number).zfill(2)
        self.subscription_topic_name = Robot_name + "/" + subscription_suffix
        self.publish_topic_name = Robot_name + "/" + publish_suffix
        
        #Mensaje y codigo cuando se conecte con el broker MQTT
        self.client.on_connect = self.on_connect

        # Se habilita el TLS para conección segura
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.message_callback_add(self.subscription_topic_name, self.on_message)

        
        #Se colocan el nombre de usuario y contraseña para la conexión con el broker MQTT
        #Por razones practicas el nombre del robot sera usado como usuario y contaseña
        self.client.username_pw_set(Robot_name,  Robot_name)

        #Se genera la conexión con el broker MQTT en el puerto
        self.client.connect(mqtt_broker_ip_address, self.port)
        print("Conectando al mqtt broker {}".format(mqtt_broker_ip_address), end="")

        #Se inicia el ciclo del funcionamiento del cliente MQTT
        self.client.loop_start()

    def send_message(self, function_name, parameter_list=None):
        #Función para envio de mensajes

        #Cración de diccionario message_dict con una key "type" y valor el nombre de la función llamada
        message_dict = {"type": function_name}

        #Revisión de si se tiene lista de parametros para la función llamada 
        if parameter_list:

            #Verificación de que los parametros hayan sido ingresados esten en una estructura iterable
            if isinstance(parameter_list, Iterable):
                
                #Se agraga al diccionario una key "payload" y valor la lista de parametros
                message_dict["payload"] = parameter_list

            else:
                # Se le informa al usuario que los paramtros no estan en una lista y se corrige el error 
                print("The parameter_list {} is not a list. Converting it to a list for you.".format(parameter_list))
                message_dict["payload"] = [parameter_list]

        #Conversión del diccionario message_dict en un mensaje jason
        message = json.dumps(message_dict)

        #Publicación del mensaje en el broker con el topico de publicación 
        self.client.publish(self.publish_topic_name, message)

    
    def on_connect(self,client, userdata, flags, rc, properties=None):
        #Función de acción al realizarse cuando se genera la conexión al broker

        #Verificación de varaible de conexión
        if rc == 0:
            print(" ... Connected!")
        else:
            print(" ... Error!!!")
            #Si se presenta un error de conexión descomente la siguente linea y verique que lo causa
            """
            0: Connection successful    
            1: Connection refused - incorrect protocol version
            2: Connection refused - invalid client identifier
            3: Connection refused - server unavailable
            4: Connection refused - bad username or password
            5: Connection refused - not authorised
            6-255: Currently unused."""
            #print("CONNACK received with code %s." % rc)
            exit()


        #Impresión de cual es el topico de publicación al que se conecto
        print("Publishing to topic:", self.publish_topic_name)

        #Declaración que la funcion on_subscribe es la misma de la clase cliente
        self.client.on_subscribe = self.on_subscribe

        #Suscripcion al topico declarado anteriormente
        self.client.subscribe(self.subscription_topic_name)

    def on_publish(self,client, userdata, mid, rc, properties=None):
        #Función para cuando la publicación fue exitosa

        #Cuando el mesaje qos es de confimación es exitoso se genera la siguiente impresión
        #impresión de identificardor de mensaje recibido
        print("mid: " + str(mid))

    
    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        #Función para cuando la suscripción fue exitosa

        #Si se quiere saber el grado qos y el mesaje de dentificación descomentar la siguiente linea
        #print("Subscribed: " + str(mid) + " " + str(granted_qos))

        #Impresión del topico al que se ha generado la suscripción
        print("Subscribed to topic:", self.subscription_topic_name)


    def on_message(self, client, userdata, msg):
        #Función para cuando se recibe un mensaje

        #Declaración de message con carga y decodificación del mensaje recibido
        message = msg.payload.decode()
        
        #Imprime el topico al que se asede el grado qos y el mensaje 
        #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        
        #Impresión del mensaje recibido por el servidor
        print("Received message:", message)

        #Si no se creo un delegado para mensajes no se procesa el mensaje
        #solo se retorna
        if not self.delegate:
            print("Missing a delegate")
            return

        
        #Atención al mensaje recivido y llamado a la función apropiada.
        try:
            #Se convierte el mensaje jason en un diccionario de python
            message_dict = json.loads(message)
        except ValueError:
            #Si no se puedde decodificar el mensaje se imprime el error y se retorna
            print("Unable to decode the received message as JSON")
            return

        #Se verifica que el diccionario tenga una key "type"
        if "type" not in message_dict:
            #Si no se tiene la key "type" se imprime el error y se retorna
            print("Received a messages without a 'type' parameter.")
            return
        
        #Se obtiene el valor asociado a la key "type"
        message_type = message_dict["type"]
        
        #Se verifica si el delegado creado tiene el metodo ingresado
        if hasattr(self.delegate, message_type):

            #Si existe el metodo se llama al metodo
            method_to_call = getattr(self.delegate, message_type)

            #Se asume que el usuario dio parametros correctos
            #Se verfica si se ingreso la lista de parametros 
            if "payload" in message_dict:

                #Si se tiene la lista de parametros se obtine esta
                message_payload = message_dict["payload"]
                #Se desempaqueta la lista y se ingra al metodo llamado
                attempted_return = method_to_call(*message_payload)

            else:

                #Si no se tiene lista de parametros solo se llama al metodo
                attempted_return = method_to_call()

            if attempted_return:
                #Si el metodo retorno algun valor se le informa al usuario ya que no es posible el manejo de valores retornados
                print("The method {} returned a value. That's not really how this library works." +
                      "The value {} was not magically sent back over".format(message_type, attempted_return))
        else:

            #Si no se encuentra el metodo llamado se le informa al usuario del error
            print("Attempt to call method {} which was not found.".format(message_type))

    def close(self):
        #Función para cerrar el cliente MQTT

        #Se imprime el mensaje de cierre del cliente y se cierra todos los elemenstos
        #Se declara al delegado como None
        print("Close MQTT")
        self.delegate = None
        self.client.loop_stop()
        self.client.disconnect()


#Función de creación de GIU
def GIU():
    #Creación de ventana principal del GIU y titulo de este
    root = tkinter.Tk()
    root.title("Contol ev3 with MQTT messages")

    #Creación de frame y grid para grilla de posicion de elementos
    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    '''Creación de label para presnetar el valor de ángulo recibido y
       declaración en el objeto my_delagate del label que recibe dicho mensaje'''
    angle_label = ttk.Label(main_frame, text="Angle")
    angle_label.grid(row=0, column=0)
    angle_value_label = ttk.Label(main_frame, text="0")
    angle_value_label.grid(row=1, column=0)
    '''my_delegate.setlabel(angle_value_label)'''

    '''Creación del boton y tecla para solicitar el ángulo'''
    angle_button = ttk.Button(main_frame, text="Update")
    angle_button.grid(row=2, column=0)
    angle_button['command'] = lambda: send_message_special(mqtt_client, "Angle", "angle button")
    root.bind('<a>', lambda event: send_message_special(mqtt_client, "Angle", "angle key"))

    """Creación del boton y tecla para hacer que el robot pare"""
    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=2, column=1)
    stop_button['command'] = lambda: send_message_special(mqtt_client, "Stop", "Stop button")
    root.bind('<space>', lambda event: send_message_special(mqtt_client, "Stop", "Stop key"))

    """Creación del boton y tecla para hacer que el robot deje el programa"""
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=3, column=0)
    q_button['command'] = lambda: send_message_special(mqtt_client, "Quit", "Quit button")
    root.bind('<q>', lambda event: send_message_special(mqtt_client, "Quit", "Quit key"))

    """Creación del boton y tecla para salir de la GIU"""
    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=3, column=1)
    e_button['command'] = lambda: exit()
    root.bind('<e>', lambda event: exit())

    """Ciclo infinito de ejecución de la GIU"""
    root.mainloop()

    

#Funcion de envio de mensajes MQTT para mover el robot
def send_message_movtank(mqtt_client, left_speed_entry, right_speed_entry, msg):

    #Declaración de elementos de la lista de parametros
    msg_left = left_speed_entry
    msg_right = right_speed_entry

    #Declaración del tipo de mensaje y lista de parametros
    msgtype = "drive"
    msglist = [msg_left, msg_right]
    
    #Envio de mensaje tipo "drive" y mensaje con lista de parametros
    mqtt_client.send_message(msgtype, msglist)

    """Impresión de acciónn realizada, topico en donde se publica
       el mensaje y el mensaje enviado"""
    print(msg, end="\t")
    print(mqtt_client.publish_topic_name, end=" ")
    print(msgtype, msglist)


#Funcion de envio de mensajes MQTT para acciones diferentes a mover el robot
def send_message_special(mqtt_client, msg_special, msg):

    #Declaración del tipo de mensaje sin lista de parametros
    msgtype = msg_special

    #Envio de mensaje
    mqtt_client.send_message(msgtype)

    """Impresión de acciónn realizada, topico en donde se publica
       el mensaje y el mensaje enviado"""
    print(msg, end="\t")
    print(mqtt_client.publish_topic_name, end=" ")
    print(msg_special)


#ejecucón de script como principal o como modulo
if __name__ == '__main__':

    #Creación de nodo de ROS
    rospy.init_node('mqtt_to_ros_node', anonymous=True)
    #rate = rospy.Rate(10)

    #Creación de publicadores y suscriptores del nodo
    global turtle_vel_pub
    turtle_vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)


    #Cración de delegado para mensajes MQTT y cliente MQTT
    my_delegate = MyDelegate()
    mqtt_client = MqttClient(my_delegate)

    #Creación de suscripcion a topico MQTT LEGOEV301/msgPC y publicacion en topico  LegoEV301/msgLegoEv3
    mqtt_client.connect_to_ev3()
    
    #Llamado a GIU
    GIU()

    #Cerrado del cliente MQTT
    mqtt_client.close()



