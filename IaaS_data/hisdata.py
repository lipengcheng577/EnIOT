#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db_opt import *
from dev_info import *
import logging


#历史库入库、出库接口
class hisdata(object):
    """description of class"""
    def __init__(self):
        self._db = db_opt.db_opt()
        self._dev_info = dev_info()


    def test(self):
        ret = self._db.if_table_exit( "dev_info" )
        print ret


    def create_hisdata_table(self, dev_id):
        '''按照设备ID创建历史数据表'''
        meas_list = self._dev_info.get_dev_meas_names(dev_id)
        sql = "create table hisdata_%d ( index SERIAL, soc text, date_time TEXT" % dev_id
        
        for meas in meas_list:
            data_type = self._dev_info.get_meas_type(meas)
            sql += ", " + meas + " " + data_type
        sql += ")"
        print sql
        logging.info("SQL: " + sql)
        self._db.excute(sql)


    def insert_record(self, dev_id, data_dict):
        '''1、判断表是否存在；2、创建表；3、插入数据。 历史库表名：hisdata_devID, ex: hisdata_10001'''
        table_name = "hisdata_%d" % dev_id
        sql_field = "("
        sql_value = "("
        index = 0
        for data in data_dict:
            if data == "id":
                continue
            if index > 0:
                sql_field += ", "
                sql_value += ", "
            index += 1
            sql_field += data 
            sql_value += str(data_dict[data])

        sql_field += " ) "
        sql_value += " ) "
        sql = "insert into %s %s values %s " % (table_name, sql_field, sql_value)
        logging.info("SQL: " + sql)
        if self._db.excute(sql) is False:
            self.create_hisdata_table(dev_id)
            self._db.excute(sql)


    '''查询历史数据'''
    def query_data(self, start_time, end_time=0):
        if end_time == 0:
            return 1
        else:
            return []






