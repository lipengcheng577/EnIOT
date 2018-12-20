#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser

from db_opt import *


def read_ini():
    print 'init table program start ...'

    db = db_opt()

    config = ConfigParser.ConfigParser()

    try:
        config.read("table_info.ini")
    except IOError:
        print "打开table_info.ini 失败！"
        return

    tables = config.sections()

    for table in tables:
#        print table + ":"
        columns = config.items(table)
#        print columns

        counter = 1
        sql = "create table " + table + " ( "
        for column in columns:
            sql += column[0] + ' ' + column[1]
            if counter != len(columns):
                sql += ', '
            counter += 1
        sql += " )"

        db.excute(sql)


if __name__ == "__main__":
    read_ini()