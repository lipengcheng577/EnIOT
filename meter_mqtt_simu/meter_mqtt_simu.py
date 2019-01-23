#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name:meter_mqtt_simu.py
# 模拟采用mqtt通信的电表，与fep_mqtt进行通信
# Python Version:2.7
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import time
import datetime
import queue

MQTT_SUB_CHANNEL = "trina_energy_iot_down"
MQTT_PUB_CHANNEL = "trina_energy_iot_up"

from mainwindow import *

class my_mqtt():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set("admin", "password")  
        HOST = "127.0.0.1"
        self.client.connect(HOST, 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect  

        self.client.loop_start()
         
                
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code: "+str(rc))

        self.client.subscribe(MQTT_SUB_CHANNEL)
        self.client.publish( MQTT_PUB_CHANNEL, json.dumps({"heart": DEV_ID, "id": DEV_ID})) 


    def on_disconnect(self, client, userdata, flags, rc):
        print("disconnected with result code "+str(rc))


    def on_message(self, client, userdata, msg):
        MQTT_DOWN_QUEUE.put(msg)   


    def publish(self, msg):
        self.client.publish( MQTT_PUB_CHANNEL, msg) 



def start_window():
    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':

    print('*********************\n  METER SIMU MQTT\n *********************\n')
    mqttttt = my_mqtt()

    start_window()

    while True:
        mqttttt.publish(json.dumps({"heart": DEV_ID, "id": DEV_ID}))
        time.sleep(60)


