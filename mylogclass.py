#! /usr/bin/env python
#coding:utf-8
import logging,os
from logging.handlers import TimedRotatingFileHandler
import time
 
class Logger:
    def __init__(self, path, clevel = logging.DEBUG,Flevel = logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        log_file_handler = TimedRotatingFileHandler(filename=path, when="M", interval=1, backupCount=10)
        log_file_handler.setFormatter(fmt)
        #设置CMD日志
        #sh = logging.StreamHandler('aaa.log')
        #sh.setFormatter(fmt)
        #sh.setLevel(clevel)
        #设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        #self.logger.addHandler(sh)
        self.logger.addHandler(log_file_handler)
        self.logger.addHandler(fh)
    
    def debug(self,message):
        self.logger.debug(message)
    
    def info(self,message):
        self.logger.info(message)
    
    def war(self,message):
        self.logger.warn(message)
    
    def error(self,message):
        self.logger.error(message)
    
    def cri(self,message):
        self.logger.critical(message)
 
if __name__ =='__main__':
    count = 0
    logyyx = Logger('yyx.log',logging.ERROR,logging.DEBUG)
    while count < 500:
        logyyx.debug('一个debug信息')
        logyyx.info('一个info信息')
        logyyx.war('一个warning信息')
        logyyx.error('一个error信息')
        logyyx.cri('一个致命critical信息')
        time.sleep(2)
        count = count + 1
