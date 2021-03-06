#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
sys.path.append("../iaas")

import configparser
import logging
import codecs
import json
#from iaas.db_opt import *

import db_opt
from init_table import *
from rtdata import *
from dev_info import *
from hisdata import *

import http.server

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

    
import numpy as np
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)


from data_server import *

if __name__ == "__main__":
    print('*********************\n   IAAS_DATA\n *********************\n')

    serverAddress = ('', 5000)
    server = http.server.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()


    #定义日志输出格式
    logging.basicConfig(level=logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = "log.txt",
    filemode = 'a+')

    rtdb = rtdata()
    hisdb = hisdata()

    table_init()

    #MQ，数据队列
    rt_ch = rtdata_channel()
    rt_sub = rt_ch.subscribe()

    while True:    
        msg= rt_sub.parse_response()
        logging.info(msg)

        msg_string = json.dumps(msg, cls=MyEncoder)
        rt_data = json.loads(msg_string)
        data_dict = eval(rt_data[2])
        if 'id' in data_dict.keys():  
            id = data_dict['id']
            soc = data_dict['soc']
            print("recv data, dev id = %d, soc=%d" % (id, soc))
            rtdb.mupdate_new_frame(int(id), data_dict)
            hisdb.insert_record(int(id), data_dict)
        else:
            logging.error("Wrong data, the msg has no ID" )
            print("Wrong data, the msg has no ID")


    
