#coding:utf-8
import urllib
import urllib2
from pyquery import PyQuery as pq
import json
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
urls=set()#待爬取
crawled=set()#已爬取
def feed(data):
    #print data
    #url = re.findall(r'''<a(\s*)(.*?)(\s*)href(\s*)=(\s*)([\"\s]*)([^\"\']+?)([\"\s]+)(.*?)>''',data,re.S|re.I)
    #url = d('a').map(lambda i,e: pq(e)('a').attr('href'))
    url=re.findall(r"<a href=\"/view/.*?\?fromTaglist",data,re.I|re.S) 
    for u in url:
        u=re.sub("<a.*?href","",u).replace('"',"").replace("=","").replace("target","").replace(" ","").replace("?fromTaglist","")
        #print u
        #if u[6].endswith("htm"):
        #print u[6]
        if u.endswith("html"):#geo
        #if "taglist" in u:#geo
            urls.add("http://baike.baidu.com"+u)
def return_data(content):
    pq_content=pq(content.replace("&nbsp;",""))
    j={}
    j['title']=pq_content('title').text().split("_")[0]
    names=pq_content(".basicInfo-item.name")
    values=pq_content('.basicInfo-item.value')
    for i in xrange(len(names)):
        j[pq(names[i]).text().replace('&nbsp;','')]=pq(values[i]).text()
    return j

def crawl_word(url_t,f):
    num=10
    for i in range(num,100000,10):
        url_target=url_t+"&offset="+str(i)
        print url_target
        content=urllib2.urlopen(url_target).read()
        content = content.decode('gb2312','ignore').encode('UTF-8')
        url = re.findall(r'''<a(\s*)(.*?)(\s*)href(\s*)=(\s*)([\"\s]*)([^\"\']+?)([\"\s]+)(.*?)>''',content,re.S|re.I)
        #url=re.findall(r"<a.*?href=.*?\?fromTaglist.*?</a>",content,re.I|re.S) 
        flag=0
        for u in url:
            u=u[6]
            u=re.sub("<a.*?href","",u).replace('"',"").replace("=","").replace("target","").replace(" ","").replace("?fromTaglist","")
            #print u
            #if u[6].endswith("htm"):
            #print u[6]
            if u.endswith("html") and "help" not in u:#geo
                if u not in urls:
                    urls.add(u)
                    f.write(u+"\n")
                    flag=1
        if flag==0:
           return 

if __name__=="__main__":
    #url= "http://baike.baidu.com/view/19957.htm"
    #url="http://baike.baidu.com/view/10833222.htm"
    #url="http://baike.baidu.com/subview/5504/16348631.htm"
    #url="http://baike.baidu.com/class/15.html"
    #urls.add(url)
    furl=open(sys.argv[2],'a+')
    n=0
    for line in furl:
        n+=1
        #if n<34303:
        #    continue
        crawled.add(line.strip())
    fout=open(sys.argv[1],'a')
    #fout_url=open(sys.argv[3],'w')
    while(len(crawled)>0):
        try:
        #if 1:
            #url=urls.pop()
            url=crawled.pop()
            #if url in crawled:
            #    continue
            #crawl_word(url,fout_url)
            url_target="http://baike.baidu.com"+url
            print url_target
            content=urllib2.urlopen(url_target,timeout=10).read()
            #content = content.decode('gb2312','ignore').encode('UTF-8')
            j=return_data(content)
            if len(j)>1:
                j.update({"url":url})
                #print json.dumps(j,ensure_ascii=False)
                fout.write(json.dumps(j,ensure_ascii=False)+"\n")
                fout.flush()
        except Exception,e:
           print e
           #time.sleep(5)
           continue
    fout.close()
    furl.close()
    #fout_url.close()
    print url+"此种子收集完毕"
