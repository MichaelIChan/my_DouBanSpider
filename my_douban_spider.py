#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
一个简单的Python爬虫, 
用于抓取豆瓣电影Top前100的电影的名称和图片，
获取后以名称作为图片文件名保存在本地文件夹中。
Anthor: Michael
Version: 0.0.1
Date: 2016-8-11
Language: Python2.7.12
Editor: Sublime Text3
Operate: 具体操作请看README.md介绍
"""

import string
import re
import urllib2

class DouBanSpider(object):
    def __init__(self) :
        self._top_num = 0
        self.page = 1
        self.cur_url = "http://movie.douban.com/top250?start={page}&filter=&type="
        self.data_titles = []
        self.data_jpgs = []
        print "DoubanSpider is ready, preparing to get data..."

    def get_page(self, cur_page):
        url = self.cur_url
        try :
            my_page = urllib2.urlopen(url.format(page = (cur_page - 1) * 25)).read().decode("utf-8")
        except urllib2.URLError, e :
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request."
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason
        return my_page

    def find_title(self, my_page):
        titles = []
        movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)
        for index, item in enumerate(movie_items):
            if item.find("&nbsp") == -1:
                titles.append("Top" + str(self._top_num + 1) + " " + item)
                self._top_num += 1
        self.data_titles.extend(titles)

    def find_jpg(self, my_page):
        movie_jpgs = re.findall(r'https:.+\.jpg', my_page)
        self.data_jpgs.extend(movie_jpgs)

    def start_spider(self):
        while self.page <= 4:
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.find_jpg(my_page)
            self.page += 1

    def downloader(self):
        for i in range(self._top_num):
            f = open(self.data_titles[i] + '.jpg', 'wb')
       	    buf = urllib2.urlopen(self.data_jpgs[i]).read()
       	    f.write(buf)

if __name__ == '__main__':
    my_spider = DouBanSpider()
    my_spider.start_spider()
    my_spider.downloader()
    print "Done..."