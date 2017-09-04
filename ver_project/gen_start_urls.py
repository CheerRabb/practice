#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import json
import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_url_list(filename=PROJECT_DIR + '/appIdList.txt'):
    print "gen_start_urls.py dir : " + PROJECT_DIR
    if os.path.isfile(PROJECT_DIR + "/err_record.txt"):
        filename = PROJECT_DIR + "/err_record.txt"
    file = open(filename, 'r')
    start_url_list = []
    # line = file.readline()
    # print line
    for line in file:
        line = line.rstrip('\n')
        # print line
        host = "https://itunes.apple.com/cn/app/id"
        if os.path.isfile("err_record.txt"):
            url = line
        else:
            url = host + line
        # print url
        start_url_list.append(url)
    print len(start_url_list)
    # print start_url_list
    return start_url_list


if __name__ == "__main__":
    print len(get_url_list())
