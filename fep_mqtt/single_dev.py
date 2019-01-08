#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading  
import time 
import json
import redis
import logging
import random


class single_dev(threading.Thread): 
    def __init__(self, dev_id, dev_info, channel):  
        threading.Thread.__init__(self)  
        self.interval = 15 #15秒的周期  
        self.thread_stop = False  
        self.dev_id = dev_id
        self.dev_info = dev_info
        self.channel = channel

        json_s = self.dev_info.get_dev_meas_info(dev_id)
        logging.info(json_s)
        self.points = json.loads(json_s)

    def call_new_data(self):
        #TODO 发送召唤内容
        print "call new data"


    def update_rtdb(self, new_data):
        print "update rtdb data"
        ret = {}
        ret['id'] = self.dev_id
        soc = int(time.time())
        ret['SOC'] = soc
        timestruct = time.localtime(soc)
        timestring = time.strftime("'%Y-%m-%d %H:%M:%S'", timestruct)
        ret['date_time'] = timestring
        #TODO make a frame
        #for point_no in self.points:
        #    point_info = self.points[point_no]
        #    point_name = point_info[0]
        #    point_coef = float(point_info[1])
        #    point_offset = float(point_info[2])

        #    value = (float(point_no) * point_coef + point_offset) * random.uniform(0.8,1.2)
        #    ret[point_name] = value

        json_ret = json.dumps(ret, sort_keys=True)
        #print json_ret
        print "send data, dev id = %d, soc=%d" % (self.dev_id, soc)

        self.channel.public(json_ret)



