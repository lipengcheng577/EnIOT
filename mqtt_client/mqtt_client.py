#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("lettuce")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.username_pw_set("admin", "password") # 必须设置，否则会返回「Connected with result code 4」
client.on_connect = on_connect
client.on_message = on_message

HOST = "127.0.0.1"

client.connect(HOST, 61613, 60)
client.loop_forever()

