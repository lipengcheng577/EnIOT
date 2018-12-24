#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser

from db_opt import *
import logging


class init_table(object):
    def __init__(self):
        self._db = db_opt()
        self._tables = []
        self._table_dict = {}

        self.read_table_info_ini()


    '''read table_info.ini'''
    def read_table_info_ini(self):
        print 'read table info start ...'

        config = ConfigParser.ConfigParser()

        try:
            config.read("./ini/table_info.ini")
        except IOError:
            print "打开table_info.ini 失败！"
            return

        self._tables = config.sections()

        for table in self._tables:
            columns = config.items(table)
            self._table_dict[table] = columns 
     

    def create_all_table(self):
        for table in self._tables:
            columns = self._table_dict[table]
            self._table_dict[table] = columns 
            counter = 1
            sql = "create table " + table + " ( "
            for column in columns:
                sql += column[0] + ' ' + column[1]
                if counter != len(columns):
                    sql += ', '
                counter += 1
            sql += " )"
            self._db.excute(sql)


    def drop_all_table(self):
          for table in self._tables:
            sql = "drop table " + table
            self._db.excute(sql)

    def init_data_point_dict(self):
        print 'init_data_point_dict start ...'
        config = ConfigParser.ConfigParser()

        try:
            config.read("./ini/data_point_dict.ini")
        except IOError:
            print "打开data_point_dict.ini 失败！"
            return

        rows = config.sections()

        for row in rows:
            columns = config.items(row)
            #INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)
            counter = 1
            sql_key = "( "
            sql_value = "( "
            for column in columns:
                sql_key += column[0]
                sql_value += column[1].decode("utf-8")
                if counter != len(columns):
                    sql_key += ', '
                    sql_value += ', '
                counter += 1
            sql_key += " )"
            sql_value += " )"

            sql = "insert into data_point_dict " + sql_key + " values " + sql_value
            self._db.excute(sql)

if __name__ == "__main__":

    #定义日志输出格式
    logging.basicConfig(level=logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = "log.txt",
    filemode = 'a+')


    table_opt = init_table()

#    table_opt.drop_all_table()
    table_opt.create_all_table()

    table_opt.init_data_point_dict()