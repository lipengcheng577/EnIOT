#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import logging
from db_opt import *

REDIS_HOST = "10.37.52.73"
#REDIS_HOST = "127.0.0.1"

#实时库入库、出库接口
class rtdata(object):
    def __init__(self):
        self.rds = redis.Redis(host=REDIS_HOST, port=6379, db=0)
        

    def mupdate_new_frame(self, dev_id, data):  
        self.rds.hmset(dev_id, data)
        logging.info("Update new data: " + "[" + str(dev_id) + "]" + str(data))


    def get_rtdata(self, dev_id):
        return self.rds.hgetall( dev_id )


