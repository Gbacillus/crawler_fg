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
furl = open(sys.argv[2],'a+')
fout = open(sys.argv[1],'a')
fin = open(sys.argv[3],'r')
 
crawled = set()#存放已爬取的队列 
queue = Queue.Queue()#存放网址的队列
out_queue = Queue.Queue()#存放内容的队列
class ThreadUrl(threading.Thread):
    def __init__(self,queue,out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
 
    def run(self):
        while True:
            try:
                host = self.queue.get()
                content=urllib2.urlopen(host,timeout=10).read()
                typeEncode = sys.getfilesystemencoding()##系统默认编码
                infoencode = chardet.detect(content).get('encoding','utf-8')
                content = content.decode(infoencode,'ignore').encode(typeEncode)
                #print chunk
                url = re.findall(r'''<a(\s*)(.*?)(\s*)href(\s*)=(\s*)([\"\s]*)([^\"\']+?)([\"\s]+)(.*?)>''',content,re.S|re.I)
                #urls=re.findall('<.*?href=.*?>',data,re.I) 
                for u in url:
                    #print u
                    #u[6]=u[6].replace("?fromTaglist","")
                    #if u[6].startswith("/list"):
                    if u[6].startswith("http://www.baike.com/wiki/"):#geo
                        url=u[6]
                        lock.acquire()
                        if url in crawled:
                            lock.release()
                            continue
                        lock.release()
                        print url
                        self.out_queue.put(url);
                        self.queue.put(url)
                        self.queue.task_done()#传入一个相当于完成一个任务
                        self.out_queue.task_done()#传入一个相当于完成一个任务
            except Exception,e:
                #print e,host+"gaga"
                continue
 
class DatamineThread(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
 
    def run(self):
        while True:
            try:
                host = self.queue.get()
                lock.acquire()
                if host in crawled:
                    lock.release()
                    continue
                furl.write(host+"\n")
                crawled.add(host)
                furl.flush()
                lock.release()
                content=urllib2.urlopen(host,timeout=10).read()
                typeEncode = sys.getfilesystemencoding()##系统默认编码
                infoencode = chardet.detect(content).get('encoding','utf-8')
                content = content.decode(infoencode,'ignore').encode(typeEncode)
                pq_content = pq(content.replace("&nbsp;","").replace("\n","").replace("\t",""))
                j = {}
                j['title']=pq_content('h1').text()
                tables=pq(pq_content("div.module.zoom"))
                names=pq(tables).find("strong")
                values=pq(tables).find("span")
                for i in xrange(len(names)):
                    j[names.eq(i).text().replace("：","")]=values.eq(i).text()
                #j.update({"url":url.replace("http://baike.baidu.com","")})
                j.update({"url":host})
                if len(j)>2:
                    lock.acquire()
                    fout.write(json.dumps(j,ensure_ascii=False)+"\n")
                    fout.flush()
                    lock.release()
                self.queue.task_done()
            except Exception,e:
                #print e,host
                continue
     
def main():
    for i in range(1):
        t = ThreadUrl(queue,out_queue)#线程任务就是将url存入到queue队列中
    t.setDaemon(True)#设置为守护线程
    t.start()

    #将网址都存放到queue队列中
    for i in range(5):
        d = DatamineThread(out_queue)#线程任务就是从源代码中解析出
        d.start()
    print url+"此种子收集完毕"

if __name__=="__main__":
    #url= "http://baike.baidu.com/view/19957.htm"
    #url="http://baike.baidu.com/view/10833222.htm"
    #url="http://baike.baidu.com/subview/5504/16348631.htm"
    url="http://www.baike.com/wiki/%E5%8C%97%E4%BA%AC"
    #url="http://zhidao.baidu.com/list?cid=105102"
    for line in furl:
        crawled.add(line.strip())
    for line in fin:
        queue.put(line.strip())
        out_queue.put(line.strip())
    queue.put(url)
    main()
    #fout.close()
