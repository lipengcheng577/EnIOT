#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name:meter_mqtt_simu.py
# 模拟采用mqtt通信的电表，与fep_mqtt进行通信
# Python Version:2.7

import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("chat")
    client.publish("chat", json.dumps({"user": user, "say": "Hello,anyone!"}))


def on_message(client, userdata, msg):
    #print(msg.topic+":"+str(msg.payload.decode()))
    #print(msg.topic+":"+msg.payload.decode())
    payload = json.loads(msg.payload.decode())
    print(payload.get("user")+":"+payload.get("say"))


if __name__ == '__main__':
    client = mqtt.Client()
    client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message

    HOST = "127.0.0.1"

    client.connect(HOST, 1883, 60)
    #client.connect(HOST, 61680, 60)
    #client.loop_forever()

    user = raw_input("input name:")
    client.user_data_set(user)

    client.loop_start()

    while True:
        str = raw_input()
        if str:
            client.publish("chat", json.dumps({"user": user, "say": str}))


