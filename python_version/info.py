# -*- coding: utf-8 -*- 

import ConfigParser
import os
import time
import urllib2

from bs4 import BeautifulSoup


class InfoClas(object):
    # 生成config对象
    conf = ConfigParser.ConfigParser()
    # 用config对象读取配置文件
    conf.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini'))

    FETCH_URLS = conf.get('FETCH_URLS', 'URLS').strip().split(',')

    # 每次获取等待的秒数
    PAUSE_SECOND = float(conf.get('PARAM', 'PAUSE_SECOND'))
    # 获取每个小组的前多少页
    PAGE_NUM = conf.getint('PARAM', 'PAGE_NUM')

    # 爬取时的header
    HEADERS = {
        'User-Agent': conf.get('HEADER', 'User-Agent'),
        'cookie': conf.get('HEADER', 'cookie'),
    }

    # 爬取的页面
    RESULT = []

    def __init__(self):
        pass

    def __showProgress(self, data):
        total = len(self.FETCH_URLS) * self.PAGE_NUM * 25
        print "[fecth progress]------>" + str((len(data) / float(total)) * 100) + '%'

    def __fetchSingle(self, url):
        try:
            request = urllib2.Request(url, headers=self.HEADERS)
            page = urllib2.urlopen(request)
            soup = BeautifulSoup(page, "html.parser")
            collection = soup.select("table.olt td.title a")
            for link in collection:
                if type(link.attrs) == dict and link.attrs.has_key("title") and link.attrs.has_key("href"):
                    link_title = link.attrs["title"]
                    link_href = link.attrs["href"]
                    link_id = link_href.split('/')[-2]
                    item = {"title": link_title, "link": link_href, "id": link_id}
                    self.RESULT.append(item)

        except BaseException as ex:
            print url + " " + str(ex)

    def fetch(self):
        self.RESULT = [];
        for url in self.FETCH_URLS:
            for i in range(self.PAGE_NUM):
                link = url + "?start=" + str(25 * i)
                if (self.PAUSE_SECOND != 0):
                    time.sleep(self.PAUSE_SECOND)
                self.__fetchSingle(link)
                self.__showProgress(self.RESULT);
                # print sys.getsizeof(self.RESULT)
                # sorted
                result_sorted = sorted(self.RESULT, key=lambda x: x['id'], reverse=True)
        return result_sorted
