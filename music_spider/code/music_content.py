# coding:utf-8
import urllib2
from pyquery import PyQuery as pq
import json
import re
import sys
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')
crawled = set()  # 已爬取


def feed(data):
    # print data
    url = re.findall(r'''<a(\s*)(.*?)(\s*)href(\s*)=(\s*)([\"\s]*)([^\"\']+?)([\"\s]+)(.*?)>(.*?)</a>''', data, re.S | re.I)
    for u in url:
        # u[6] = u[6].replace("?fromTaglist", "")
        if u[6].startswith("/tag/"):
            print u[6] + "\t" + u[9]
        # if u[6].endswith("html") or "taglist" in u[6]:#geo


def return_data(content, fout, uid):
    # print content
    pq_content = pq(
        content.replace("&nbsp;", "")
        .replace("\t", "").replace("\r\n", ""))
    # singer = pq_content('span.cover').attr("title")
    singer = uid
    names = pq_content("span.song-title")
    albums = pq_content("span.album-title")
    nums = pq_content("span.hot-num")
    if len(names) <= 0:
        return False
    # values=pq_content('.basicInfo-item.value')
    j = {}
    for i in xrange(len(names)):
        # j[pq(names[i]).text().replace('&nbsp;', '')] = pq(values[i]).text()
        target = pq(names.eq(i))
        j["title"] = target("a").text()
        j["singer"] = singer
        j["url"] = target("a").attr("href")
        #j["album"] = pq(albums.eq(i)).text()
        j["nums"] = int(nums.eq(i).text().replace(",", ""))
        j.update(get_tags("http://music.baidu.com" + j['url']))
        fout.write(json.dumps(j, ensure_ascii=False) + "\n")
        fout.flush()


def get_tags(url):
    content = urllib2.urlopen(url, timeout=10).read()
    typeEncode = sys.getfilesystemencoding()  # 系统默认编码
    infoencode = chardet.detect(content).get('encoding', 'utf-8')
    content = content.decode(infoencode, 'ignore').encode(typeEncode)
    tags = pq(content)("a.tag-list")
    album = pq(pq(content)("li.clearfix").eq(0))('a').text()
    lyric = pq(content)('#lyricCont').attr("data-lrclink")
    j = {"tags": [], "lyrics": lyric}
    for i in range(len(tags)):
        j['tags'].append(tags.eq(i).text())
    if album:
        j['album'] = album
    return j


def get_url(s, n):
    s = "http://music.baidu.com/data/user/getsongs?start=" + str(n) + "&ting_uid=" + s + "&order=hot&hotmax=0&pay="
    #s = "http://music.baidu.com/tag/" + s + "?start=" + str(n) + "&size=25&third_type=0"
    return s


if __name__ == "__main__":
    '''
    # url = "http://music.baidu.com/artist"
    url = "http://music.baidu.com/tag"
    content = urllib2.urlopen(url,timeout=10).read()
    typeEncode = sys.getfilesystemencoding()# 系统默认编码
    infoencode = chardet.detect(content).get('encoding', 'utf-8')
    content = content.decode(infoencode,'ignore').encode(typeEncode)
    feed(content)
    '''
    furl = open(sys.argv[2], 'r')
    n = 0
    for line in furl:
        # n += 1
        crawled.add(line.strip())
    # print len(line.strip())
    fout = open(sys.argv[1], 'a')
    while(len(crawled) > 0):
        try:
         #if 1:
            url, artist = crawled.pop().split("\t")
            uid = url[8:]
            #uid = '1224'
            #artist = "刘德华"
            # if url in crawled:
            #    continue
            for i in range(0, 1100, 25):
                url = get_url(uid, i)
                print url
                content = urllib2.urlopen(url, timeout = 10).read()
                typeEncode = sys.getfilesystemencoding()  # 系统默认编码
                infoencode = chardet.detect(content).get('encoding', 'utf-8')
                content = content.decode(infoencode, 'ignore') \
                    .encode(typeEncode)
                j = json.loads(content)
                content = j["data"]["html"]
                if not return_data(content, fout, artist):
                    continue
        except Exception, e:
            print e
            continue
    fout.close()
    # furl.close()
