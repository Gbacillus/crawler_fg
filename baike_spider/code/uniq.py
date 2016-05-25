#coding:utf-8
import sys
import json
import class_baike
import urllib2
import chardet
crawled=set()
for line in open(sys.argv[1],'r'):
    j=json.loads(line.strip())
    try:
        crawled.add(j['url'])
    except:
        continue

urls=set()
for line in open(sys.argv[2],'r'):
    url=line.strip()
    if url not in crawled:
        urls.add(url)
fout=open(sys.argv[3],'a')
for u in urls:
    try:
        target_url="http://baike.baidu.com"+u
        print target_url
        content=urllib2.urlopen(target_url,timeout=10).read()
        typeEncode = sys.getfilesystemencoding()##系统默认编码
        infoencode = chardet.detect(content).get('encoding','utf-8')
        content = content.decode(infoencode,'ignore').encode(typeEncode)
        j=class_baike.return_data(content)
        if len(j)>0:
            j.update({"url":u})
        #print json.dumps(j,ensure_ascii=False)
            fout.write(json.dumps(j,ensure_ascii=False)+"\n")
            fout.flush()
    except Exception,e:
        continue
fout.close()
