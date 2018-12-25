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

    #往实例化表里添加数据，读取响应配置文件
    def init_instance_table(self, table_name):
        print 'init_instance_table: ' + table_name
        config = ConfigParser.ConfigParser()

        file_name = "./ini/" + table_name + ".ini"
        try:
            config.read(file_name)
        except IOError:
            logging.error("打开 %s 失败！", file_name)
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

            sql = "insert into " + table_name + " " + sql_key + " values " + sql_value
            self._db.excute(sql)

    #依据dev_model中的data_attr, 以及dev_model中的point_table_name，生成空白配置文件
    #免去人工输入，
    def create_point_table_file(self, dev_model_id):
        print "创建点表配置文件, 设备型号: %d" % dev_model_id 
         #select id_father, point_table_name from dev_model where id=dev_model_id
         #select data_attr from dev_type where id = id_father
         #分割data_attr,生成如下文件
         #id = 1 序号
         #name = Ua
         #point = 
         #coef = 
         #offset = 

    #往实例化表里添加数据，读取响应配置文件 dev_model：point_table_name
    def init_point_table(self):
        #从dev_model里找出所有point_table_name，建表，然后 读取配置文件，插入数据
        #select point_table_name from dev_model
        print "init point table"


    #此函数没啥用了
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

    table_opt.drop_all_table()
    table_opt.create_all_table()

#    table_opt.init_data_point_dict()
    table_opt.init_instance_table("data_point_dict")
    table_opt.init_instance_table("dev_type")
    table_opt.init_instance_table("dev_model")
    table_opt.init_instance_table("dev_instance")