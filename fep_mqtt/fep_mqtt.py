#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name:fetp_mqtt.py
# Python Version:2.7



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
from my_mqtt import *


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


#召唤数据间隔，单位秒
GET_DATA_INTERVAL = 15

if __name__ == "__main__":
    print '!!!!!!!!!!!!!!!!!!!!\n   FEP for MQTT\n!!!!!!!!!!!!!!!!!!!!\n'

    #定义日志输出格式
    logging.basicConfig(level=logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = "log.txt",
    filemode = 'a+')

    mqtt_obj = my_mqtt()
    rtdata_ch = rtdata_channel()
    dev_info_obj = dev_info()

    dev_ids = [10023,10024]

    dev_objs = []
    for dev_id in dev_ids:
        dev_obj = single_dev(dev_id, dev_info_obj, rtdata_ch, mqtt_obj)
        #time.sleep(0.5)
        dev_obj.start()
        dev_objs.append(dev_obj)

    #循环判断所连接的设备，到时间了召唤，
    #上送的数据，由回调函数完成
    while True:
        soc = int(time.time())

        for dev in dev_objs:
            if soc >= dev.get_latest_soc()+GET_DATA_INTERVAL:
                dev.call_new_data()
                dev.set_latest_soc(soc)

        time.sleep(0.3)


