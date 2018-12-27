#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from db_opt import *

#实时库入库、出库接口
class rtdata(object):
    def __init__(self):
        self.rds = redis.Redis(host='127.0.0.1', port=6379, db=0)
        #r.set('hello', 'world')
        #print(r.get('hello'))
        # 属性集合
        

    def mupdate_new_frame(self):
        attr_dict = {
            "name": "天合",
            "alias": "trina",
            "sex": "male",
            "height": 175,
            "postal code": 100086,
            "Tel": "138",
        }
        # 批量添加属性
        
        self.rds.hmset("rtdata_test", attr_dict)


