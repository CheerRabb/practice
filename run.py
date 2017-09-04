# coding:utf-8
# scrapy crawl vip -s LOG_FILE=scrapy.log

from scrapy import cmdline

cmdline.execute("scrapy crawl versionSpy -s LOG_FILE=scrapy.log".split())