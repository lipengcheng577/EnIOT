#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name:fetp_mqtt.py
# Python Version:2.7


import sys
sys.path.append("..")
sys.path.append("../iaas")

import logging
import codecs
import json
import redis
import time
import random
from single_dev import *
from iaas.dev_info import *
from my_mqtt import *


REDIS_HOST = "10.37.52.73"
#REDIS_HOST = "127.0.0.1"
class rtdata_channel:
    def __init__(self):
        self.__conn = redis.Redis(host=REDIS_HOST)
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


#召唤数据间隔，单位秒
GET_DATA_INTERVAL = 5

if __name__ == "__main__":
    print('!!!!!!!!!!!!!!!!!!!!\n   FEP for MQTT\n!!!!!!!!!!!!!!!!!!!!\n')

    #定义日志输出格式
    logging.basicConfig(level=logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = "log.txt",
    filemode = 'a+')

    _mqtt = my_mqtt()
    _rtdata_ch = rtdata_channel()
    _dev_info = dev_info()

    dev_ids = [51001,51002,51003,51004,51005]
    dev_objs = []
    dev_dict = {}
    for dev_id in dev_ids:
        dev_obj = single_dev(dev_id, _dev_info, _rtdata_ch, _mqtt)
        #time.sleep(0.5)
        dev_obj.start()
        dev_objs.append(dev_obj)
        dev_dict[dev_id] = dev_obj

    #循环判断所连接的设备，到时间了召唤，
    #上送的数据，由回调函数完成
    counter = 0
    while True:
        soc = int(time.time())

        while not DATA_QUEUE.empty():
            print(counter)
            counter += 1
            data = DATA_QUEUE.get()
            
            if 'id' in data.keys():
                if 'heart' in data.keys():
                    print("get haert report, id = %d" % data["id"])
                else:  
                    id = data["id"]
                    if id in dev_dict.keys():
                        dev_dict[id].update_rtdb(data)
                    continue
            else:
                print("wwwwwwwwwww")
                print(data)

        for dev in dev_objs:
            if soc >= dev.get_latest_soc()+GET_DATA_INTERVAL:
                dev.call_new_data()
                dev.set_latest_soc(soc)

        time.sleep(0.3)


