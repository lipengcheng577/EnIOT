#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser

from db_opt import *


class init_table(object):
    def __init__(self):
        self._db = db_opt()

    '''read table_info.ini'''
    def init_table(self):
        print 'init table program start ...'

        config = ConfigParser.ConfigParser()

        try:
            config.read("./ini/table_info.ini")
        except IOError:
            print "打开table_info.ini 失败！"
            return

        tables = config.sections()

        for table in tables:
            columns = config.items(table)

            counter = 1
            sql = "create table " + table + " ( "
            for column in columns:
                sql += column[0] + ' ' + column[1]
                if counter != len(columns):
                    sql += ', '
                counter += 1
            sql += " )"

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
                sql_value += column[1]
                if counter != len(columns):
                    sql_key += ', '
                    sql_value += ', '
                counter += 1
            sql_key += " )"
            sql_value += " )"
            print sql_key
            print sql_value
            sql = "insert into data_point_dict " + sql_key + " values " + sql_value
            self._db.excute(sql)

if __name__ == "__main__":

    table_opt = init_table()
    #table_opt.init_table()
    table_opt.init_data_point_dict();