#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("D:\\platform\\code\\EnIOT\\iaas")

import logging
import codecs
import json
import redis
from dev_info import *


class rtdata_channel:

    def __init__(self):
        self.__conn = redis.Redis(host='127.0.0.1')
        self.chan_sub = 'rtdata_channel'
        self.chan_pub = 'fm104.5'

    def public(self, msg):
        self.__conn.publish(self.chan_pub, msg)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub


if __name__ == "__main__":

    print '!!!!!!!!!!!!!!!!!!!!\n   FEP SIMULATOR\n!!!!!!!!!!!!!!!!!!!!\n'
    #定义日志输出格式
    logging.basicConfig(level=logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = "log.txt",
    filemode = 'a+')

#    table_init()
    dev_info_obj = dev_info()
    json_s = dev_info_obj.get_dev_meas_info(10001)
    print json_s
    logging.info(json_s)

    points = json.loads(json_s)


    for point_no in points:
        point_info = points[point_no]
        point_name = point_info[0]
        print point_info[0]

    #rt_ch = rtdata_channel()
    #rt_sub = rt_ch.subscribe()
    #while true:
    #    msg= rt_sub.parse_response()
    #    print msg

    #    rtd = rtdata()
    #    rtd.mupdate_new_frame()

    

