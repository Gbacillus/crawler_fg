# coding:utf-8
'''爬取网易风格分类信息'''
import urllib2
from pyquery import PyQuery as pq
import json
import re
import sys
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')
uniq = set()

def url2content(url):
    flag = 5
    content = ""
    while flag:
        try:
            content = urllib2.urlopen(url, timeout = 10).read()
            typeEncode = sys.getfilesystemencoding()  # 系统默认编码
            infoencode = chardet.detect(content).get('encoding', 'utf-8')
            content = content.decode(infoencode, 'ignore') \
                .encode(typeEncode)
            content = content.decode('utf-8')
            break
        except:
            flag -= 1
            continue
    return content

def cra_list(cat):
    base_url = "http://music.163.com/discover/playlist/?order=hot&cat=" + cat + "&limit=35&offset="
    lists = []
    for i in xrange(0,1500,35):
        url = base_url + str(i)
        content = url2content(url)
        names = pq(content)("a.tit.f-thide.s-fc0")
        for i in xrange(len(names)):
            name = names.eq(i).text()
            url = "http://music.163.com" + names.eq(i).attr("href")
            lists.append((name, url, cat))
            print "\t".join((name, url, cat))
    return lists

def cra_song(content):
    json_str = re.search(ur"jsonm = (.*)\}\;", content).group()
    json_str = json_str.replace("jsonm = ","").replace(";","")
    j = json.loads(json_str)
    if len(j)<1 or "musiclist" not in j:
        return []
    songs = j["musiclist"]
    return songs

if __name__ == "__main__":
    #fout = open(sys.argv[2], "w")
    print url2content('http://music.163.com/#/playlist?id=377315799')
    exit(0)
    n = 0
    for line in open(sys.argv[1], "r"):
        n += 1
        # if n < 18:
        #    continue
        try:
        # if 1:
            cat = line.strip()
            lists = cra_list(cat)
        except:
            continue
