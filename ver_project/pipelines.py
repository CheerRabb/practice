# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb.cursors
import time
import MySQLdb
import logging


    # appId = scrapy.Field()
    # date = scrapy.Field()
    # version = scrapy.Field()
class VerProjectPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self):
        self.MYSQL_SERVER = '101.201.41.164'
        self.MYSQL_DB = 'spider'
        self.MYSQL_USERNAME = 'root'
        self.MYSQL_PASSWORD = 'chenya'
        try:
            ##用户名和密码
            self.dbpool = adbapi.ConnectionPool('MySQLdb', host=self.MYSQL_SERVER, db=self.MYSQL_DB,
                                                user=self.MYSQL_USERNAME, passwd=self.MYSQL_PASSWORD,
                                                cursorclass=MySQLdb.cursors.DictCursor, charset='utf8',
                                                use_unicode=True)
        except Exception as e:
            print "ERROR(SQLStorePipeline): %s" % (str(e),)

    def process_item(self, item, spider):
        # run db query in thread pool
        try:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        except Exception as e:
            self.dbpool = adbapi.ConnectionPool('MySQLdb', host=self.MYSQL_SERVER, db=self.MYSQL_DB,
                                                user=self.MYSQL_USERNAME, passwd=self.MYSQL_PASSWORD,
                                                cursorclass=MySQLdb.cursors.DictCursor, charset='utf8',
                                                use_unicode=True)
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        tx.execute( \
            "insert into appStore_version"
            "(appId,date,version) "
            "values(%s,%s,%s) "
            "on duplicate key update version=%s",
            (
                item['appId'],
                item['date'],
                item['version'],
                # int(time.time())
                item['version']
            )
        )
        # log.msg("vip_info stored in db: %s" % item, level=log.DEBUG)
        logging.info("appStore version info stored in db: %s" % item)

    def handle_error(self, e):
        pass
        # log.err(e)
        logging.error(e)
