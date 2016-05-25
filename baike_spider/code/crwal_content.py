#coding:utf-8
import urllib2
from pyquery import PyQuery as pq
import json
import re
#import time
import sys
import class_baike
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')
urls=set()#待爬取
crawled=set()#已爬取
def feed(data):
    #print data
    url = re.findall(r'''<a(\s*)(.*?)(\s*)href(\s*)=(\s*)([\"\s]*)([^\"\']+?)([\"\s]+)(.*?)>''',data,re.S|re.I)
    #urls=re.findall('<.*?href=.*?>',data,re.I) 
    for u in url:
        #print u
        #u[6]=u[6].replace("?fromTaglist","")
        if u[6].endswith("htm"):
        #print u[6]
        #if u[6].endswith("html") or "taglist" in u[6]:#geo
            urls.add("http://baike.baidu.com"+u[6])
def return_data(content):
    pq_content=pq(content.replace("&nbsp;",""))
    j={}
    j['title']=pq_content('title').text().split("_")[0]
    names=pq_content(".basicInfo-item.name")
    values=pq_content('.basicInfo-item.value')
    for i in xrange(len(names)):
        j[pq(names[i]).text().replace('&nbsp;','')]=pq(values[i]).text()
    tags = pq_content("span.taglist")
    j['tags'] = []
    for i in xrange(len(tags)):
        j['tags'].append(tags.eq(i).text())
    return j

if __name__=="__main__":
    #url= "http://baike.baidu.com/view/19957.htm"
    #url="http://baike.baidu.com/view/10833222.htm"
    #url="http://baike.baidu.com/subview/5504/16348631.htm"
    #url="http://baike.baidu.com/view/10559.htm"
    url="http://baike.baidu.com/view/360982.htm"
    #url="http://baike.baidu.com/subview/1758/18233157.htm"
    #url="http://baike.baidu.com/view/10766.htm"
    #url="http://baike.baidu.com/view/1267983.htm"
    #url="http://baike.baidu.com/subview/3208/5954155.htm"
    urls.add(url)
    furl=open(sys.argv[2],'a+')
    for line in furl:
        crawled.add(line.strip())
    fout=open(sys.argv[1],'a')
    while(len(urls)>0):
        try:
            url=urls.pop()
            if url in crawled:
                continue
            content=urllib2.urlopen(url,timeout=10).read()
            typeEncode = sys.getfilesystemencoding()##系统默认编码
            infoencode = chardet.detect(content).get('encoding','utf-8')
            content = content.decode(infoencode,'ignore').encode(typeEncode)
            j=class_baike.return_data(content)
            feed(content)
            j=return_data(content)
            j.update({"url":url.replace("http://baike.baidu.com","")})
            if len(j)>2:
                fout.write(json.dumps(j,ensure_ascii=False)+"\n")
                fout.flush()
            furl.write(url+"\n")
            crawled.add(url)
            furl.flush()
        except Exception,e:
            print e
            #time.sleep(5)
            continue
    fout.close()
    furl.close()
    print url+"此种子收集完毕"
