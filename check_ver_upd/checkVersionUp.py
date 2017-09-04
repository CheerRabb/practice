# -*- coding: utf-8 -*-

import datetime
import MySQLdb.cursors
import json
import codecs
import logging
import time
import traceback
import sys

from datetime import date
today = date.today()

reload(sys)
sys.setdefaultencoding('utf8')

import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

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
        print PROJECT_DIR
        if os.path.isfile(PROJECT_DIR + "/updateList_" + str(today) + ".txt"):
            os.remove(PROJECT_DIR + "/updateList_" + str(today) + ".txt")
            print "remove older updateList.txt"
            # dispatcher.connect(self.finalize, signals.engine_stopped)

    def initialize(self):
        try:
            # print "start init database"
            self.conn = MySQLdb.connect(host=self.MYSQL_SERVER, user=self.MYSQL_USERNAME, passwd=self.MYSQL_PASSWORD,
                                        db=self.MYSQL_DB, charset='utf8', use_unicode=True)
        except Exception as e:
            # print "here comes an error" + e.message
            print "error"

    def do_check_version_up(self):
        cursor = self.conn.cursor()

        sql_select_appids = "SELECT appId FROM appStore_version GROUP BY appId"
        cursor.execute(sql_select_appids)
        # appid_tuple=cursor.fetchall()
        """This is the standard Cursor class that returns rows as tuples
        and stores the result set in the client."""
        # print "appid_tuple: ", appid_tuple

        update_appid_list = []
        update_appid_tup = []
        # for appid in appid_tuple:
        for (appId) in cursor:
            # print appId
            curr_appid = appId[0]
            sql_version_list = "SELECT version,date FROM appStore_version WHERE appId='%s' ORDER BY date DESC LIMIT 2" % (
            curr_appid)
            # print "sql_version_list: " + sql_version_list
            cursor.execute(sql_version_list)
            data = cursor.fetchall()
            # print "data: ", data

            if len(data) > 1:
                if data[0][0] != data[1][0]:
                    # sql_query_appname = "SELECT appName FROM appDict WHERE iosAppStoreID='%s' " % (curr_appid)

                    sql_query_appname = "SELECT appName FROM appStore_version " \
                                        "left JOIN appStoreTopFreeList on appStore_version.appId=appStoreTopFreeList.appId " \
                                        "where appStore_version.appId='%s' GROUP BY appStore_version.appId " % (
                                        curr_appid)
                    cursor.execute(sql_query_appname)
                    appname = cursor.fetchall()[0][0]
                    print appname
                    print curr_appid + ": version updated!!!"
                    # update_appid_list.append(curr_appid)

                    file = open(PROJECT_DIR + "/updateList_" + str(today) + ".txt", "a")

                    if appname!=None:
                        file.write(curr_appid + ' ' + appname + '\n')
                    else:
                        file.write(curr_appid + '\n')
                    file.close()
                    # update_appid_tup.append((curr_appid,appname))
                    # print update_appid_tup


                    # # test
                    # appid1 = "385919493"
                    # appid2 = "1033387365"
                    # sql_version_list = "SELECT version,date FROM appStore_version WHERE appId='%s' ORDER BY date DESC LIMIT 2" % (
                    # appid1)
                    # print "sql_version_list: " + sql_version_list
                    # cursor.execute(sql_version_list)
                    # data = cursor.fetchall()
                    # print "data: ", data
                    # if data[0][0] != data[1][0]:
                    #     print appid1 + ": version updated!!!"

    def do_delete(self, id):
        sql = 'delete from db_ou where id=\'' + id + "\'"
        try:
            self.conn.cursor().execute(sql)
            self.conn.commit()
            logging.info(sql)
        except:
            logging.warning(sql + " !!!!! delete error")
            self.conn.rollback()

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()


if __name__ == "__main__":
    mysqlManager = MySqlManager()
    mysqlManager.do_check_version_up()
