#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading  
import time 
import json
import redis
import logging
import random
from my_mqtt import *


class single_dev(threading.Thread): 
    def __init__(self, dev_id, dev_info, channel, mqtt_obj):  
        threading.Thread.__init__(self)  
        self.interval = 15 #15秒的周期  
        self.thread_stop = False  
        self.dev_id = dev_id
        self.dev_info = dev_info
        self.channel = channel
        self.latest_soc = 0
        self._mqtt = mqtt_obj

        json_s = self.dev_info.get_dev_meas_info(dev_id)
        logging.info(json_s)
        self.points = json.loads(json_s)


    def get_latest_soc(self):
        return self.latest_soc


    def set_latest_soc(self, soc):
        self.latest_soc = soc


    #cmd[命令：request, answer] data[量测字典，all-全部]
    def call_new_data(self):
        #TODO 发送召唤内容
        send_data = {}
        send_data['id'] = self.dev_id
        send_data['data'] = "all"
        send_data['cmd'] = 'request'
        soc = int(time.time())
        timestruct = time.localtime(soc)
        timestring = time.strftime("'%Y-%m-%d %H:%M:%S'", timestruct)
        send_data['time'] = timestring
        send_data['soc'] = soc

        print("call data: ")
        print(send_data)
        self._mqtt.publish(json.dumps(send_data))


    def update_rtdb(self, new_data):
        print("update rtdb data")
        print("send data, dev id = %d" % (self.dev_id))
        json_ret = json.dumps(new_data, sort_keys=True)
        self.channel.public(json_ret)



