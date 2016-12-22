# encoding=utf8
import threading
import requests
import sys
reload(sys)

sys.setdefaultencoding('utf8')

def save(html, file_absolute_path):
    with open(file_absolute_path, 'wb+') as file:
        file.write(html)
        file.flush()

def crawl(req):
    d = requests.get(req["host"])
    return d.text

class MyCrawler(threading.Thread):
    def __init__(self, req, file_path):
        threading.Thread.__init__(self, name="Crawler-{}".format(req["host"]))
        self.req = req
        self.file_path = file_path
    def run(self):
        html = crawl(self.req)
        save(html, self.file_path)

def __main__():
    continue_input = True
    threads = []
    while continue_input:
        host = raw_input("host: ")
        file_path = raw_input("output file absolute path: ")
        req = {"host": host}
        threads.append(MyCrawler(req, file_path))
        continue_input = raw_input("add another? (y/N) ") == "y"
    for t in threads:
        t.start()

__main__()
