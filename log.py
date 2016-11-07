#! coding:utf-8
import time
import datetime
import os
import signal

def handler(a, b):
    print "hahah"
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
                print "open file success"
                break 
            except IOError:
                print "open file failed"
                time.sleep(2)
                
        errCount = 0
                   
        monitorline = follow(monitorfile)
        for line in monitorline:
            print "监控开始"
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
                         errCount = 0
                         
                     if(errCount >= 5):
                         print "err!!!!!!!!!!!!!!"
                         #errCount = 0

        monitorfile.close()
        print "file closed"
