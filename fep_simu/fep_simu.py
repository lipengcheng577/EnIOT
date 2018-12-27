#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

import logging
import codecs
import json
import redis
from iaas.dev_info import *
import time


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


if __name__ == "__main__":

    print '!!!!!!!!!!!!!!!!!!!!\n   FEP SIMULATOR\n!!!!!!!!!!!!!!!!!!!!\n'
    #定义日志输出格式
    logging.basicConfig(level=logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = "log.txt",
    filemode = 'a+')

#    table_init()
    dev_id = 10001
    dev_info_obj = dev_info()
    json_s = dev_info_obj.get_dev_meas_info(dev_id)
    print json_s
    logging.info(json_s)

    points = json.loads(json_s)

    ret = {}
    ret['id'] = dev_id
    soc = int(time.time())
    ret['SOC'] = soc
    timestruct = time.localtime(soc)
    timestring = time.strftime("'%Y-%m-%d %H:%M:%S'", timestruct)
    ret['date_time'] = timestring
    for point_no in points:
        point_info = points[point_no]
        point_name = point_info[0]
        point_coef = float(point_info[1])
        point_offset = float(point_info[2])
        print point_info[0]

        value = float(point_no) * point_coef + point_offset
        ret[point_name] = value

    json_ret = json.dumps(ret, sort_keys=True)
    print json_ret

    rt_ch = rtdata_channel()
    try:
        rt_ch.public(json_ret)
    except:
        logging.error("Failed send meas data!")
    #while True:
    #    rt_ch.public(json_ret)
    #    sleep(15)



    #rt_ch = rtdata_channel()
    #rt_sub = rt_ch.subscribe()
    #while true:
    #    msg= rt_sub.parse_response()
    #    print msg

    #    rtd = rtdata()
    #    rtd.mupdate_new_frame()

    

