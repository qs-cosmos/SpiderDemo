# coding: utf-8 

from download.fisher import Fisher
from download.seeder import Seeder
from analyse.analyser import Analyser, LyricParser, JsonFile
from message.message import MessageQueue
from log.logger import getLogger, Logger
from multiprocessing import Pool
import os, time, random, sys

'''
seed_scheduler —— 网页下载器调度程序
- frequency : 运行频次
'''
def seed_scheduler(frequency, name=0):
    logger = getLogger(Logger.SEEDER)

    logger.info('seed_scheduler %s start.' % (name))
    queue = MessageQueue()
    seeder = Seeder()
    while frequency:
        seed = None
        while seed is None or queue.exists(seed):
            seed = seeder.seed()
        
        queue.seed = seed
        queue.repeat(seed)
        logger.info('Seeder %s get the %dth seed : %s.' % (name, frequency, seed))
        frequency = frequency - 1

    logger.info('seed_scheduler %s end.' % (name))

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
        frequency = frequency - 1
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
        logger.info('Fisher %s stop dealing the %dth seed : %s.' % (name, frequency, seed))

    logger.info('fish_scheduler %s end...' % (name))

'''
analyse_scheduler —— 解析器调度程序
- frequency : 运行频次
'''
def analyse_scheduler(frequency, name=0):
    logger = getLogger(Logger.ANALYSER)

    logger.info('analyse_scheduler %s start.' % (name))
    queue = MessageQueue()
    parser = LyricParser()
    database = JsonFile()
    analyser = Analyser(parser, database)
    while frequency:
        frequency = frequency - 1
        html = None
        while html is None:
            html = queue.html
        logger.info('Analyser %s  start parsing the %dth text.' % (name, frequency))
        analyser.resolve(html)
        logger.info('Analyser %s  stop parsing the %dth text.' % (name, frequency))
    logger.info('analyse_scheduler %s end.' % (name))




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

