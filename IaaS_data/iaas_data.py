#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

import ConfigParser
import logging
import codecs
import json
#from iaas.db_opt import *

import db_opt
from init_table import *
from rtdata import *
from dev_info import *
from hisdata import *
logging.getLogger().setLevel(logging.INFO)


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
    print '*********************\n   IAAS_DATA\n *********************\n'
    #定义日志输出格式
    logging.basicConfig(level=logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = "log.txt",
    filemode = 'a+')

    #console = logging.StreamHandler()
    #console.setLevel(logging.INFO)
    #formatter = logging.Formatter('%(name)s : %(levelname)s : %(message)s')
    #console.setFormatter(formatter)
    #logging.getLogger('').addHandler(console)

    #logging.info("++++++++++++++++++++++++++++")

    rtdb = rtdata()
    hisdb = hisdata()

#    table_init()

    rt_ch = rtdata_channel()
    rt_sub = rt_ch.subscribe()
    while True:
       
        msg= rt_sub.parse_response()
        logging.info(msg)

        msg_string = json.dumps(msg)
        rt_data = json.loads(msg_string)
        data_dict = eval(rt_data[2])
        if data_dict.has_key('id'):  
            id = data_dict['id']
            soc = data_dict['SOC']
            print "recv data, dev id = %d, soc=%d" % (id, soc)
            rtdb.mupdate_new_frame(int(id), data_dict)
            hisdb.insert_record(int(id), data_dict)
        else:
            print "Wrong data, there is no ID"


    
