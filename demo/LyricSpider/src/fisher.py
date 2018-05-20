# coding: utf-8

from downloader import Downloader
from logger import getLogger, Logger
from message import MessageQueue
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
fish_scheduler —— 网页下载器调度程序
- frequency : 运行频次
'''
def fish_scheduler(frequency, name=0):
    logger = getLogger(Logger.FISHER)

    logger.info('fish_scheduler %s start...' % (name))
    queue = MessageQueue()
    fisher = Fisher()
    while frequency:
        seed = None
        html = None
        while seed is None:
            seed = queue.seed
        if seed == '':
            html = ''
        else :
            seed = ('http://www.lyrics.com'  + seed).encode('utf-8')
            logger.info('Fisher %s start dealing the %dth seed : %s.' % (name, frequency, seed))
            html = fisher.fish(seed)
            if html is None:
                html = ''
        queue.html = html
        frequency = frequency - 1
        logger.info('Fisher %s stop dealing the %dth seed : %s.' % (name, frequency, seed))

    logger.info('fish_scheduler %s end...' % (name))


if __name__ == '__main__':
    # url = 'https://www.lyrics.com/lyric/15459687'
    # fish = Fisher()
    # print fish.fish(url)
    fish_scheduler(10)
