# coding: utf-8

import requests
import time

class ProxyPool(object):

    def __init__(self):

        # 代理池主机地址
        self.__proxy_pool_host = 'http://115.159.59.195:5010{}'
        
        # 当代理池为空时，默认代理
        self.__default_proxy = 'socks5://127.0.0.1:1084'

        # 访问代理池主机的Proxy
        self.__local_proxies = {
            'http':self.__default_proxy,
            'https':self.__default_proxy
        }

        # 访问代理池主机的User-Agent
        self.__local_headers = {
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
        
        # Try to avoid the Exception : ConnectionError: ('Connection aborted.', BadStatusLine("''",))
        self.__sleep_time = 1

    def getProxy(self):
        url = self.__proxy_pool_host.format('/get')

        try:
            time.sleep(self.__sleep_time)
            proxy = requests.get(url, proxies=self.__local_proxies, headers=self.__local_headers).content
        
        except  requests.exceptions.ConnectionError as e:
            return self.__default_proxy
        
        if (proxy == 'no proxy'):
            return self.__default_proxy
        else :
            return 'http://' + proxy

    def deleteProxy(self, proxy):
        if(proxy == self.__default_proxy or not proxy):
            return

        url = self.__proxy_pool_host.format('/delete')
        params = {'proxy':proxy.split('/')[2]}

        not_success = True
        retry_count = 20
        while(not_success and retry_count):
            try:
                time.sleep(self.__sleep_time)
                r = requests.get(url, params=params, proxies=self.__local_proxies, headers=self.__local_headers)
                not_success = False

            except requests.exceptions.ConnectionError as e:
                retry_count = retry_count - 1
            
if __name__ == '__main__':
    proxyPool = ProxyPool()
    url = proxyPool.getProxy()
    print(url)
    proxyPool.deleteProxy(url)
