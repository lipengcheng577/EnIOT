#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

import time
import datetime

import logging
logging.getLogger().setLevel(logging.INFO)


DB_HOST = "10.37.52.73"
#DB_HOST = "127.0.0.1"

class db_opt(object):
    """description of class"""

    def __init__(self):
        self.connect_db()
        
    def connect_db(self):
        try:
            self._conn = psycopg2.connect(database="EnIOT", user="postgres", password="abcd-1234", host=DB_HOST, port="5432")
            print("Open database successfully")
            logging.info("Open database successfully")
        except:
            logging.error("Open database failed")
  
    def close_db(self):
        self._conn.close()
        logging.info("Close database")

    def excute(self, sql):
        logging.info(sql)
        
        cur = self._conn.cursor()
        try:
            cur.execute(sql)
            self._conn.commit()
            return True
        except:
            self._conn.rollback() 
            cur.close()
            logging.error("Failed:" + sql)
            return False


    def if_table_exit(self, table_name):
        cur = self._conn.cursor()
        sql = "SELECT to_regclass('%s') is not null" % table_name
        cur.execute(sql)
        rows=cur.fetchall()
        return rows[0][0]


    def select(self, sql):
        logging.info(sql)
        
        cur = self._conn.cursor()
        try:
            cur.execute(sql)
            rows=cur.fetchall()
            return rows
        except:
            self._conn.rollback() 
            cur.close()
            logging.error("Failed:" + sql)
            return []

