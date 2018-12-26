#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db_opt import *

#实时库入库、出库接口
class rtdata(object):
    def __init__(self):
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        #r.set('hello', 'world')
        #print(r.get('hello'))


