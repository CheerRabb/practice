#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from os import path
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import NotConfigured
import datetime
import MySQLdb.cursors
from scrapy import signals
# import scrapy
import json
import codecs
import logging
import time
import traceback

import sys

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')


class MySqlManager(object):
    def __init__(self):
        self.MYSQL_SERVER = '101.201.41.164'
        self.MYSQL_DB = 'spider'
        self.MYSQL_USERNAME = 'root'
        self.MYSQL_PASSWORD = 'chenya'
        self.conn = None
        self.initialize()
        # dispatcher.connect(self.finalize, signals.engine_stopped)

    def initialize(self):
        try:
            # print "start init database"
            self.conn = MySQLdb.connect(host=self.MYSQL_SERVER, user=self.MYSQL_USERNAME, passwd=self.MYSQL_PASSWORD,
                                        db=self.MYSQL_DB, charset='utf8', use_unicode=True)
        except Exception as e:
            # print "here comes an error" + e.message
            print "error"

    def do_delete(self, id):
        sql = 'delete from db_ou where id=\'' + id + "\'"
        try:
            self.conn.cursor().execute(sql)
            self.conn.commit()
            logging.info(sql)
        except:
            logging.warning(sql + " !!!!! delete error")
            self.conn.rollback()

    # {"goodsid": 220915394, "counter": "\u52692\u592919\u5c0f\u65f6", "price": "99"}
    def do_update_counter_info(self, line):
        json_dict = json.loads(line)
        # print line
        if "goodsid" in json_dict:
            item = {}
            item['goodsid'] = json_dict['goodsid']
            item['counter'] = json_dict['counter']
            formated_str = "insert into vip_info" \
                           "(vip_goodsid,vip_counter,vip_updatetime) values('%s','%s','%s') " \
                           "on duplicate key update vip_counter='%s',vip_updatetime='%s'" % (
                               item['goodsid'],
                               item['counter'],
                               int(time.time()),

                               item['counter'],
                               int(time.time())
                           );
            # print formated_str
        try:
            self.conn.cursor().execute(formated_str)
            self.conn.commit()
            logging.info(formated_str)
        except:
            logging.warning(" !!!!! update error")
            traceback.print_exc()
            self.conn.rollback()

    def do_check_version_up(self):
        sql_select_appids="select * from appStore_version"

        formated_str = "select version from appStore_version where appId='%s'"% ("1015364140",)
        print formated_str
        cursor = self.conn.cursor()
        cursor.execute(formated_str)
        data = cursor.fetchall()

        print "test select query: " ,data


    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()


if __name__ == "__main__":
    mysqlManager = MySqlManager()
    mysqlManager.do_check_version_up()
