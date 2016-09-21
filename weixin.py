#! /usr/bin/env  python
import requests
import json

def get_token():
    url='https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid' : 'wxe21aab1f9d39e795' ,
            'corpsecret':'n7ggwekZffKr01pDqXc7BuGOruMv4qb9jdVhCeK6T1YAG_sDz_e1vbryzGthS8vL',
             }
    req = requests.get(url, params=values)    
    data = json.loads(req.text)
    return data["access_token"]

def send_msg():
    url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+get_token()
    values = """{"touser" : "@all" ,
            "toparty":"1",
            "msgtype":"text",
            "agentid":"2",
            "text":{
                "content": "%s"
            },
            "safe":"0"
            }""" %(str("10.1.1.8 is down"))
   
    data = json.loads(values) 
    req = requests.post(url, values)    

if __name__ == '__main__':
    send_msg()
