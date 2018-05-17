# coding: utf-8

import random
import time

class UserAgentPool(object):

    def __init__(self):
        self.__user_agent_pool = []
        self.__user_agent_config = './user-agent.config'
        with open(self.__user_agent_config, 'r') as config:
            for line in config.readlines():
                self.__user_agent_pool.append(line.strip())
        
    # 随机返回一个新的 User-Agent
    def getUserAgent(self):
        random.seed(int(time.time()))
        length = len(self.__user_agent_pool)
        return self.__user_agent_pool[random.randint(0, length - 1)]

if __name__ == '__main__':
    pool = UserAgentPool()
    print(pool.getUserAgent())
