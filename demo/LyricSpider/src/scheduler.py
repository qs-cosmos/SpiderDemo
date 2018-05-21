# coding: utf-8 

from analyser import analyse_scheduler
from fisher import fish_scheduler
from seeder import seed_scheduler
from message import MessageQueue
from multiprocessing import Pool
from logger import getLogger, Logger
import os, time, random, sys

'''
scheduler —— 总调度程序
- amount : 进程个数
- frequency : 每个进程的运行次数, 默认为1
'''
def scheduler(amount, frequency=1):
    logger = getLogger(Logger.SCHEDULER)

    logger.info('Scheduler start.')
    queue = MessageQueue()
    queue.clear()

    analyser_pool = Pool()
    fish_pool = Pool()
    seed_pool = Pool()

    for i in range(amount):
        analyser_pool.apply_async(analyse_scheduler, args=(frequency, i))
        fish_pool.apply_async(fish_scheduler, args=(frequency, i))
        seed_pool.apply_async(seed_scheduler, args=(frequency, i))
    analyser_pool.close()
    fish_pool.close()
    seed_pool.close()

    analyser_pool.join()
    fish_pool.join()
    seed_pool.join()
    logger.info('Scheduler end.')
    queue.clear()

if __name__ == '__main__':

    scheduler(2, 1000)

