#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import queue

MQTT_SUB_CHANNEL = "trina_energy_iot_up"
MQTT_PUB_CHANNEL = "trina_energy_iot_down"

DATA_QUEUE = queue.Queue(maxsize = 100)

class my_mqtt():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        HOST = "127.0.0.1"
        self.client.connect(HOST, 1883, 60)
        self.client.loop_start()

                
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe("trina_energy_iot_up")
#        self.client.publish( MQTT_PUB_CHANNEL, json.dumps({"P": "FEP_MQTT", "Q": "the server is ready"})) 


    def on_disconnect(self, client, userdata, flags, rc):
        print("disconnected with result code "+str(rc) )


    def on_message(self, client, userdata, msg):
        #print "get：" + msg.payload.decode() 这一句可能有问题，加了就收不到信息了，估计是不能print
        data = json.loads(msg.payload.decode())
        DATA_QUEUE.put(data)


    def publish(self, msg):
        self.client.publish( MQTT_PUB_CHANNEL, msg) 

