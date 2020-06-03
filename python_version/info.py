# -*- coding: utf-8 -*- 

import socket
import time
import urllib2

from bs4 import BeautifulSoup


class InfoClas(object):
    FETCH_URLS = [
        "http://www.douban.com/group/beijingzufang/discussion",
        "http://www.douban.com/group/fangzi/discussion",
        "http://www.douban.com/group/262626/discussion",
        "http://www.douban.com/group/276176/discussion",

        # �����ⷿ����
        "http://www.douban.com/group/26926/discussion",
        # �����ⷿ����̽��
        "http://www.douban.com/group/sweethome/discussion",
        # �����ⷿ���Ұ��һ��סһ�����䣡
        "http://www.douban.com/group/242806/discussion",
        # �����ⷿ��������(�н�����) 
        "http://www.douban.com/group/257523/discussion",
        # �����ⷿ�����н飩 
        "http://www.douban.com/group/279962/discussion",
        # �����ⷿ���ⷿ
        "http://www.douban.com/group/334449/discussion",
        "https://www.douban.com/group/opking/discussion",
        "https://www.douban.com/group/276176/discussion",
        "https://www.douban.com/group/465554/discussion",
        "https://www.douban.com/group/zhufang/discussion",
        "https://www.douban.com/group/625354/discussion"
    ]

    RESULT = []
    PAUSE_SECOND = 0
    # 获取每个小组的前多少页
    PAGE_NUM = 5

    def __init__(self):
        pass

    def __showProgress(self, data):
        total = len(self.FETCH_URLS) * self.PAGE_NUM * 25
        print "[fecth progress]------>" + str((len(data) / float(total)) * 100) + '%'

    def __fetchSingle(self, url):
        try:
            socket.setdefaulttimeout(6000)
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            request = urllib2.Request(url, headers=headers)
            page = urllib2.urlopen(request, timeout=60000)
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
