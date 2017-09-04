#!/usr/bin/python
# -*-coding:utf-8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from datetime import date
from ver_project.gen_start_urls import *
from ver_project.items import *

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class VipSpider(scrapy.Spider):
    name = "versionSpy"
    start_urls = [
        "https://itunes.apple.com/cn/app/id350962117",
    ]
    http_err_list = []

    def __init__(self):
        self.start_urls = get_url_list()

    def start_requests(self):

        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)

    def parse(self, response):

        curr_url = response.url
        # print curr_url
        appId = curr_url.split("/")[-1][2:]
        print appId
        # <span itemprop="softwareVersion">7.7.1</span>
        app_version_ls = response.xpath('//span[@itemprop="softwareVersion"]/text()').extract()
        print app_version_ls[0]
        app_ver = app_version_ls[0]
        today = date.today()  # 2017-08-07
        print today
        # format_today = today.isoformat()
        # print format_today
        AS_Item = VerProjectItem()
        AS_Item["appId"] = appId
        AS_Item["date"] = today
        AS_Item["version"] = app_ver
        yield AS_Item

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            err_record = open("err_record.txt", "a")
            err_record.write(response.url + "\n")
            err_record.close()
            self.http_err_list.append(response.url)

            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

        print len(self.http_err_list)
