# coding: utf-8

from downloader import Downloader
from message import MessageQueue
from logger import getLogger, Logger

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

'''
seed_scheduler —— 网页下载器调度程序
- frequency : 运行频次
'''
def seed_scheduler(frequency, name=0):
    logger = getLogger(Logger.SEEDER)

    logger.info('seed_scheduler %s start.' % (name))
    queue = MessageQueue()
    queue.clear()
    seeder = Seeder()
    while frequency:
        seed = None
        while seed is None or queue.exists(seed):
            seed = seeder.seed()
        
        queue.seed = seed
        queue.repeat(seed)
        frequency = frequency - 1
        logger.info('Seeder %s get the %dth seed : %s.' % (name, frequency, seed))

    logger.info('seed_scheduler %s end.' % (name))


if __name__ == '__main__':
    seed_scheduler(10)
