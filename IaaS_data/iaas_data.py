#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

import ConfigParser

#from iaas.db_opt import *

import db_opt
from init_table import *
from rtdata import *
from iaas.dev_info import *
import logging
import codecs
import json

def table_init():
    table_opt = init_table()

    table_opt.drop_all_table()
    table_opt.create_all_table()

    table_opt.init_instance_table("data_point_dict", "")
    table_opt.init_instance_table("dev_type", "")
    table_opt.init_instance_table("dev_model", "")
    table_opt.init_instance_table("dev_instance", "")

    table_opt.init_point_table()

    #table_opt.create_point_table_file(1001001)

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

    rt_ch = rtdata_channel()
    
    while True:
        rt_sub = rt_ch.subscribe()
        msg= rt_sub.parse_response()
        print msg
        logging.info(msg)
        msg_string = json.dumps(msg)
        rt_data = json.loads(msg_string)
        data_dict = eval(rt_data[2])
        if type(data_dict) == type({}):
            if data_dict.has_key('id'):  
                id = data_dict['id']
                print "dev id = %d" % id
            else:
                print "Wrong data, there is no ID"

        



        #rtd = rtdata()
        #rtd.mupdate_new_frame()

    
