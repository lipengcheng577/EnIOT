import paho.mqtt.client as mqtt
import json
import time
import datetime
import queue

MQTT_SUB_CHANNEL = "trina_energy_iot_down"
MQTT_PUB_CHANNEL = "trina_energy_iot_up"

MQTT_DOWN_QUEUE = queue.Queue(maxsize = 1000)

class my_mqtt():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set("admin", "password")  
        #HOST = "127.0.0.1"
        #self.client.connect(HOST, 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect  

        #self.client.loop_start()

    def start(self):
        HOST = "127.0.0.1"
        self.client.connect(HOST, 1883, 60)
        self.client.loop_start()


    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
         
                
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code: "+str(rc))

        self.client.subscribe(MQTT_SUB_CHANNEL)
        self.client.publish( MQTT_PUB_CHANNEL, json.dumps({"heart": DEV_ID, "id": DEV_ID})) 


    def on_disconnect(self, client, userdata, flags, rc):
        print("disconnected with result code "+str(rc))


    def on_message(self, client, userdata, msg):
        print('new msg')
        MQTT_DOWN_QUEUE.put(msg)   


    def publish(self, msg):
        self.client.publish( MQTT_PUB_CHANNEL, msg) 
