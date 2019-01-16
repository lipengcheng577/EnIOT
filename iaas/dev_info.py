#!/usr/bin/env python
# -*- coding: utf-8 -*-
import db_opt
import logging
import codecs

import json

'''从数据库中获取数据，形成json'''


class dev_info(object):
    def __init__(self):
        self._db = db_opt.db_opt()


    def get_dev_id_list(self):
        sql = "select id from dev_instance"
        rows = self._db.select(sql)
        point_table_name = rows[0][0]
        id_list = []
        for row in rows:
            id_list.append(row[0])
            
        return id_list


    def get_dev_meas_names(self, dev_id):
        '''获取测点名称列表'''
        sql = "select dev_model from dev_instance where id=%d" % (dev_id)
        rows = self._db.select(sql)
        dev_model_id = int( rows[0][0])
        print 'dev_model= %d \n' % (dev_model_id)

        sql = "select point_table_name from dev_model where id=%d" % (dev_model_id)
        rows = self._db.select(sql)
        point_table_name = rows[0][0]

        sql = "select name from %s" % (point_table_name)
        rows = self._db.select(sql)
        meas_list = []
        for row in rows:
            meas_list.append(row[0])
            
        return meas_list


    def get_meas_type(self, name):
        sql = "select data_type from data_point_dict where name= '%s' " % (name)
        rows = self._db.select(sql)
        return rows[0][0]
        

    #从设备ID获取设备量点表，返回json格式
    def get_dev_meas_info(self, dev_id):
        sql = "select dev_model from dev_instance where id=%d" % (dev_id)
        rows = self._db.select(sql)
        dev_model_id = int( rows[0][0])
        print 'dev_model= %d \n' % (dev_model_id)

        sql = "select point_table_name from dev_model where id=%d" % (dev_model_id)
        rows = self._db.select(sql)
        point_table_name = rows[0][0]

        sql = "select point, name, coef, offset_value from %s" % (point_table_name)
        rows = self._db.select(sql)
        meas_dict = {}
        for row in rows:
            #print "%s %s %s %s\n" % (row[0], row[1], row[2], row[3])
            meas_dict[row[0]] = [row[1], row[2], row[3]]

        json_s = json.dumps(meas_dict, sort_keys=True)
        #print json_s
        return json_s





