#! coding:utf-8
import time
import datetime
import os
import signal
import logging
import mylogclass

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='mylog.log',
                filemode='a')
    
logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')

ryxlog = mylogclass.Logger('ryx.log',logging.ERROR,logging.DEBUG)
def handler(a, b):
    print "Ctrl + C can't kill me!"
    return 0

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            if(datetime.datetime.now().strftime('%H%M%S') == '195800'):
                time.sleep(2)
                os.system('echo 123 >> /home/redhat/src/prap/py_using/aaa')
                break
            continue
        yield line

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    while(1):

        now = datetime.datetime.now()
        logTime = now.strftime('%Y%m%d')
        filename = '/home/redhat/src/prap/py_using/RYXLOG.' + logTime
        print filename
        while(1):
            try:
                monitorfile = open(filename, "r")
                #logging.info('Open file:%s success.' % filename)
                ryxlog.info('Open file:%s success.' % filename)
                print "open file success"
                break 
            except IOError:
                ryxlog.error('Open file:%s error.' % filename)
                print "open file failed"
                time.sleep(2)
                
        errCount = 0
                   
        monitorline = follow(monitorfile)
        for line in monitorline:
            print "监控开始"
            #logging.info('监控开始')
            ryxlog.info('监控开始')
            if "应答报文接受失败" in line:
                 if(0 == errCount):
                     #获取起始时间
                     startTime = datetime.datetime.now()
                     errCount = errCount + 1
                     print "startTime:", startTime
                 else:
                     #获取当前时间
                     errTime = datetime.datetime.now()
                     print "errTime:", errTime
                     print "-:", str((errTime - startTime).seconds)
                     if((errTime - startTime).seconds <= 20):
                         errCount = errCount + 1
                         print "err++: ", errCount
                     else:
                         print "超出时间段"
                         #logging.info('超出监控时段')
                         ryxlog.info('超出监控时间段')
                         errCount = 0
                         
                     if(errCount >= 5):
                         #logging.info('条件被触发')
                         ryxlog.info('条件被触发')
                         print "err!!!!!!!!!!!!!!"
                         #errCount = 0

        monitorfile.close()
        print "file closed"
        ryxlog.info('file is closed!')
