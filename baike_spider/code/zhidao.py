#coding:utf-8
from pyquery import PyQuery as pq
import json,chardet
import re
import sys
import threading
from threading import Condition
import Queue
reload(sys)
sys.setdefaultencoding('utf-8')
MAX_NUM=10
lock = Condition()
import urllib2
import time
furl=open(sys.argv[2],'a+')
fout=open(sys.argv[1],'a')
 
 
queue = Queue.Queue()#存放网址的队列
out_queue = Queue.Queue()#存放内容的队列
class ThreadUrl(threading.Thread):
    def __init__(self,queue,out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
 
    def run(self):
        while True:
            host = self.queue.get()
            #print host
            content=urllib2.urlopen(host,timeout=10).read()
            #print content
            typeEncode = sys.getfilesystemencoding()##系统默认编码
            infoencode = chardet.detect(content).get('encoding','utf-8')
            content = content.decode(infoencode,'ignore').encode(typeEncode)
            self.out_queue.put(content);
            #print chunk
            url = re.findall(r'''<a(\s*)(.*?)(\s*)href(\s*)=(\s*)([\"\s]*)([^\"\']+?)([\"\s]+)(.*?)>''',content,re.S|re.I)
            #urls=re.findall('<.*?href=.*?>',data,re.I) 
            for u in url:
                #print u
                #u[6]=u[6].replace("?fromTaglist","")
                #if u[6].startswith("/list"):
                if u[6].endswith("htm"):#geo
                    url="http://baike.baidu.com"+u[6]
                    print url
                    self.queue.put(url)
                    self.queue.task_done()#传入一个相当于完成一个任务
 
class DatamineThread(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
 
    def run(self):
        while True:
            content = self.queue.get()
            pq_content = pq(content.replace("&nbsp;","").replace("\n","").replace("\t",""))
            j = {}
            j['title']=pq_content('title').text().split("_")[0]
            names=pq_content(".basicInfo-item.name")
            values=pq_content('.basicInfo-item.value')
            for i in xrange(len(names)):
                j[pq(names[i]).text().replace('&nbsp;','')]=pq(values[i]).text()
            j.update({"url":url.replace("http://baike.baidu.com","")})
            if len(j)>2:
                lock.acquire()
                fout.write(json.dumps(j,ensure_ascii=False)+"\n")
                fout.flush()
                lock.release()
            self.queue.task_done()
 
start = time.time()
def main():
    for i in range(2):
        t = ThreadUrl(queue,out_queue)#线程任务就是将url存入到queue队列中
        t.setDaemon(True)#设置为守护线程
        t.start()
 
    #将网址都存放到queue队列中
    for i in range(10):
        d = DatamineThread(out_queue)#线程任务就是从源代码中解析出
        d.start()
    print url+"此种子收集完毕"

if __name__=="__main__":
    #url= "http://baike.baidu.com/view/19957.htm"
    #url="http://baike.baidu.com/view/10833222.htm"
    #url="http://baike.baidu.com/subview/5504/16348631.htm"
    url="http://baike.baidu.com/view/10559.htm"
    #url="http://zhidao.baidu.com/list?cid=105102"
    for line in furl:
        queue.put(line.strip())
    queue.put(url)
    main()
    #fout.close()
    #furl.close()
