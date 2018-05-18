#G coding: utf-8
import requests
from configure import ProxyPool
from configure import UserAgentPool
import codecs
import time

'''
Downloader —— 爬虫下载器

下载策略 : 
    - 设置 代理 和 客户端类型 模拟正常用户的访问操作
        - proxy : https://github.com/jhao104/proxy_pool
        - user-agent : user-agent.config
        - 每个 proxy 和 user-agent 使用超过预值时, 重新进行选取
    - 网页下载 : requests
'''
class Downloader(object):

    def __init__(self):
        self.__proxy_pool = ProxyPool()
        self.__user_agent_pool = UserAgentPool()

        self.__max_mask_count = 10
        self.__mask_count = self.__max_mask_count
        self.__config()

    def __config(self):
        self.__proxy = self.__proxy_pool.proxy()
        self.__user_agent = self.__user_agent_pool.user_agent()

        self.__proxies = {
            'http':self.__proxy,
            'https':self.__proxy
        }
        self.__headers = {
            'User-Agent':self.__user_agent
        }

    def request(self, seed, allow_redirects=True):
        
        if not isinstance(seed, str):
            raise ValueError("The seed must be a string!")

        if (self.__mask_count):
            self.__mask_count = self.__mask_count - 1
        else:
            self.__mask_count = self.__max_mask_count
            self.__config()

        '''
        - 若retry_count == 0, 说明当前 proxy 和 user-agent可能存在问题
        - 重置 proxy
            - 从 proxy_pool 中删除当前 proxy
            - 从 proxy_pool 中获取一个 新的proxy
        - 重置 user-agent
        - 重置 proxy 和 user-agent 使用计数
        - 再进行一次 retry 
        '''
        retry_count = 5
        while (retry_count) :
            try:
                return requests.get(seed, proxies=self.__proxies, \
                        headers=self.__headers, allow_redirects=allow_redirects)

            except requests.exceptions.RequestException:
                retry_count  = retry_count - 1

        self.__proxy_pool.delete(self.__proxy)
        self.__config
        self.__mask_count = self.__max_mask_count
        
        try:
            time.sleep(2)
            return requests.get(seed, proxies=self.__proxies, \
                    headers=self.__headers, allow_redirects=allow_redirects)

        except requests.exceptions.RequestException:
            return None

'''
Fisher —— 网页抓取
'''
class Fisher(Downloader):

    def fish(self, seed):
        r = self.request(seed)
        if r is None:
            return None
        else:
            return r.text

'''
Seeder —— 种子下载器
'''
class Seeder(Downloader):
    
    def __init__(self, seed='https://www.lyrics.com/random.php'):
        super(Seeder, self).__init__()
        self.__origin_seed = seed

    def seed(self):
        
        r = self.request(self.__origin_seed, False)
        if r is None:
            return None
        else:
            return r.headers['location']
        

if __name__ == '__main__':
    seeder = Seeder()
    print(seeder.seed())
