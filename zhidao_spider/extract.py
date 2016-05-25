#coding:utf-8
import sys
from pyquery import PyQuery as pq
content = open(sys.argv[1]).read()
pq_content = pq(content.replace("&nbsp;","").replace("\n","").replace("\t","").replace("：",""))
j = {}
j['title']=pq_content('h1').text()
tables=pq(pq_content("div.module.zoom"))
names=pq(tables).find("strong")
values=pq(tables).find("span")
for i in xrange(len(names)):
    print names.eq(i).text(),values.eq(i).text()
for i in xrange(len(names)):
    j[pq(names[i]).text().replace('&nbsp;','')]=pq(values[i]).text()
