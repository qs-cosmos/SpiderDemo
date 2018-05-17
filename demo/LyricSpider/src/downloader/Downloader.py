# coding: utf-8
import requests
from ProxyPool import ProxyPool
from UserAgentPool import UserAgentPool
import codecs

# 下载网页资源
class Downloader(object):

    def __init__(self):
        self.__proxy_pool = ProxyPool()
        self.__user_agent_pool = UserAgentPool()
        self.__max_mask_count = 30
        self.__mask_count = self.__max_mask_count
        self.__config()

    def __config(self):
        self.__proxies = {
            'http':self.__proxy_pool.getProxy(),
            'https':self.__proxy_pool.getProxy()
        }
        self.__headers = {
            'User-Agent':self.__user_agent_pool.getUserAgent()
        }

    def getHTML(self, seed):
        if (self.__mask_count):
            self.__mask_count = self.__mask_count - 1
        else:
            self.__mask_count = self.__max_mask_count
            self.__config()
        
        r = requests.get(seed, proxies=self.__proxies, headers=self.__headers)
        
        return r.text

if __name__ == '__main__':
    seed = 'https://www.lyrics.com/lyric/14054763'
    download = Downloader()
    download.getHTML(seed)
