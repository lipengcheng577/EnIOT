#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name:fetp_mqtt.py
# Python Version:2.7

import paho.mqtt.client as mqtt
import json

import sys
sys.path.append("..")

import logging
import codecs
import json
import redis
import iaas.dev_info
import time
import random
from single_dev import *
from iaas.dev_info import *


class rtdata_channel:
    def __init__(self):
        self.__conn = redis.Redis(host='127.0.0.1')
        self.chan_sub = 'rtdata_channel'
        self.chan_pub = 'rtdata_channel'

    def public(self, msg):
        self.__conn.publish(self.chan_pub, msg)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub


MQTT_SUB_CHANNEL = "trina_energy_iot_up"
class my_mqtt():
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_disconnect

        HOST = "127.0.0.1"

        self.connect(HOST, 1883, 60)

        client.loop_start()

        while True:
            str = raw_input()
            if str:
                client.publish("chat", json.dumps({"user": user, "say": str}))             


if __name__ == "__main__":
    print '!!!!!!!!!!!!!!!!!!!!\n   FEP SIMULATOR\n!!!!!!!!!!!!!!!!!!!!\n'
    # Print out the menu:
    print "Input: " 
    print "stop --exit the program"

    #cmd = raw_input( "> " )
    #if cmd == 'start':
    #    print u'启动程序'

    #定义日志输出格式
    logging.basicConfig(level=logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = "log.txt",
    filemode = 'a+')

    rt_ch = rtdata_channel()
    dev_info_obj = dev_info()

    dev_ids = []
    for i in range(10001,10023):
        dev_ids.append(i)
    #dev_ids = [10001, 10002, 10003, 10004]

    dev_objs = []
    for dev_id in dev_ids:
        dev_obj = single_dev(dev_id, dev_info_obj, rt_ch)
        #time.sleep(0.5)
        dev_obj.start()
        dev_objs.append(dev_obj)

    #TODO
    #循环判断所连接的设备，100ms计数吧，到时间了召唤，
    #上送的数据，由回调函数完成
    while True:
        print 'Fep is running...'

        cmd = raw_input( "> " ) 
        if cmd == 'stop':
            print u"End Fep simu..."
            for dev_obj in dev_objs:
                dev_obj.stop()
            time.sleep(15)
            break
        else:
            print u"无效命令"
        time.sleep(1)


