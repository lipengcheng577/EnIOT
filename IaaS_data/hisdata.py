#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

from iaas.db_opt import *


#历史库入库、出库接口
class hisdata(object):
    """description of class"""
    def __init__(self):
        self._db = db_opt()


