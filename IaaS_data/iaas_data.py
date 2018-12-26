#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser

from db_opt import *
from init_table import *
import logging
import codecs

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


if __name__ == "__main__":

    #定义日志输出格式
    logging.basicConfig(level=logging.INFO,
    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    filename = "log.txt",
    filemode = 'a+')

#    table_init()
