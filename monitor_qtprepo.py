#! coding:utf-8
import time
import datetime
import os
import signal
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='.qt_prepo.log',
                filemode='a')
   

def handler(a, b):
    print "Ctrl + C can't kill me!"
    return 0

file_size=0
def follow(thefile):
    global file_size
    thefile.seek(0,2)
    while True:
        dt = datetime.datetime.now().strftime("%H%M%S")
        if (dt >= "223000" or dt <= "080000"):
            logging.info("当前时间:%s, 不予监控!", dt)
            time.sleep(30)
            continue
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            try:
                size = os.stat(r'/home/weblogic/logs/qt_prepo/info/qtpay_prepo_info.log').st_size
                #logging.info('get file size success!')
            except OSError:
                #logging.info('get file size error!')
                break
            #logging.info('nowsize:%d, oldsize:%d' % (size, file_size))
            if size >= file_size:
                file_size = size
            else:
		break
            continue
        yield line

if __name__ == '__main__':
    global file_size 
    signal.signal(signal.SIGINT, handler)
    while(1):

        #now = datetime.datetime.now()
        #logTime = now.strftime('%Y%m%d')
        filename = '/home/weblogic/logs/qt_prepo/info/qtpay_prepo_info.log'
        while(1):
            try:
                monitorfile = open(filename, "r")
                #logging.info('Open file:%s success.' % filename)
                break 
            except IOError:
                logging.info('Open file:%s error.' % filename)
                #print "open file failed"
                time.sleep(2)
        try:        
            file_size = os.stat(r'/home/weblogic/logs/qt_prepo/info/qtpay_prepo_info.log').st_size
            #logging.info('get file:%s size success!' % filename)
        except OSError:
            monitorfile.close()
            logging.error('get file:%s size error!' % filename)
            time.sleep(2)
            continue
            
        errCount = 0
                   
        monitorline = follow(monitorfile)
        for line in monitorline:
            #logging.info('监控开始')
            if "调用服务发生异常" in line:
                 if(0 == errCount):
                     startTime = datetime.datetime.now()
                     errCount = errCount + 1
                     logging.info("此次监控周期开始")
                 else:
                     #获取当前时间
                     errTime = datetime.datetime.now()
                     #logging.info("errTime:%s", errTime)
                     if((errTime - startTime).seconds <= 60):
                         errCount = errCount + 1
                         logging.info("err count: %d" % errCount)
                     else:
                         logging.info('此次监控周期结束，重新计算')
                         errCount = 1
                         startTime = datetime.datetime.now()
                         logging.info("此次监控周期开始")
                         
                     if(errCount >= 20):
                         errCount = 0
                         logging.info('条件被触发')
                         os.system('curl -d "message=20140903|130954|616978|18516180631|prepo get servie error|00899999" http://197.68.88.105:8028/zc19/qtPaySendMessage.do')

        monitorfile.close()
        logging.info('file is closed!')
