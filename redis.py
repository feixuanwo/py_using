#!/usr/bin/env python
import sys
import os
import socket 
try:
    port=sys.argv[2]
except IndexError:
    port=6379

key_dick={}
status_data_arra={}

def get_local_ip():  #获取本机ip
    s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    (addr,port) = s.getsockname()
    s.close()
    return addr

def get_curr_connections():
    return float(key_dick['connected_clients'])

def get_qps():
    return float(key_dick['total_commands_processed'])

def get_mem_fragmentation_ratio():
    return float(key_dick['mem_fragmentation_ratio'])

def get_usage():
    return float(key_dick['used_memory'])
    return usage

if __name__ == '__main__':
    local_ip=get_local_ip()
    cmd='/root/soft/redis-2.8.3/src/redis-cli -h ' + local_ip+ ' -p ' + str(port) + ' info' #注意redis-cli的路径
    for i in os.popen(cmd):               #popen运行命令并返回命令的返回内容
        #print i[0]
        if not i.split() or i[0] == '#':  #处理redis info信息中的空行和以#开头的无用行
            continue
        #print '================='
        key=i.split(':')[0].strip()
        value=i.split(':')[1].strip()
        key_dick[key]=value
        status_data_array={               #定义一个字典，其中每个key对应想要取得的信息，key对应的value则对应相对应的函数
            'usage':'get_usage()',
            'curr_connections':'get_curr_connections()',
            'qps':'get_qps()',
            'mem_fragmentation_ratio':'get_mem_fragmentation_ratio()'
        }
    print"%.2f" % eval(status_data_array[sys.argv[1]])
