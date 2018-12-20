#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

import time
import datetime


class db_opt(object):
    """description of class"""

    def __init__(self):
        self.connect_db()
        
    def connect_db(self):
        self._conn = psycopg2.connect(database="EnIOT", user="postgres", password="abcd-1234", host="127.0.0.1", port="5432")
        print "Open database successfully"
  
    def close_db(self):
        self._conn.close()

    def excute(self, sql):
        print "SQL:-------------------------"
        print sql
        print "-----------------------------"
        cur = self._conn.cursor()
        try:
            cur.execute(sql)
            self._conn.commit()
        except:
            print "Failed to excute the SQL"
        

