#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json

MQTT_SUB_CHANNEL = "trina_energy_iot_up"
MQTT_PUB_CHANNEL = "trina_energy_iot_down"

class my_mqtt():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_disconnect

        HOST = "127.0.0.1"

        self.client.connect(HOST, 1883, 60)

        self.client.loop_start()
         
                
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        self.client.subscribe(MQTT_SUB_CHANNEL)
        self.client.publish( MQTT_PUB_CHANNEL, json.dumps({"user": "my_mqtt", "say": "the server is ready"})) 


    def on_disconnect(self, client, userdata, flags, rc):
        print("disconnected with result code "+str(rc))


    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        print(payload.get("temperature")+":"+payload.get("humidity"))


    def publish(self, msg):
        self.client.publish( MQTT_PUB_CHANNEL, msg) 

