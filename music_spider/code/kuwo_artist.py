# coding:utf-8
'''酷我音乐爬虫'''
import urllib2
from pyquery import PyQuery as pq
import json
import re
import sys
import chardet
from AccUrl import getAcc
reload(sys)
sys.setdefaultencoding('utf-8')
crawled = set()  # 已爬取
uniq = set()


def feed(data, fout):
    '''爬取url'''
    # print data
    url = re.findall(r'''<a(\s*)(.*?)(\s*)href(\s*)=(\s*)([\"\s]*)([^\"\']+?)([\"\s]+)(.*?)>(.*?)</a>''', data, re.S | re.I)
    for u in url:
        # u[6] = u[6].replace("?fromTaglist", "")
        if u[6].startswith("/artist/"):
            if u[6] in crawled:
                continue
            crawled.add(u[6])
            fout.write(u[6] + "\n")
            fout.flush()
        # if u[6].endswith("html") or "taglist" in u[6]:#geo

def find_id(url):
    '''爬取歌手id'''
    content = urllib2.urlopen(url, timeout=10).read()
    typeEncode = sys.getfilesystemencoding()  # 系统默认编码
    infoencode = chardet.detect(content).get('encoding', 'utf-8')
    content = content.decode(infoencode, 'ignore').encode(typeEncode)
    pq_content = pq(
        content.replace("&nbsp;", "")
        .replace("\t", "").replace("\r\n", ""))
    uid = pq_content(".artistTop").attr("data-artistid")
    #print url,uid
    return uid
def return_data(url, fout, uid):
    '''解析歌单页面爬取的数据'''
    content = urllib2.urlopen(url, timeout = 10).read()
    typeEncode = sys.getfilesystemencoding()  # 系统默认编码
    infoencode = chardet.detect(content).get('encoding', 'utf-8')
    content = content.decode(infoencode, 'ignore') \
        .encode(typeEncode)
    content = content.decode('utf-8')
    #print content
    pq_content = pq(
        content.replace("&nbsp;", "")
        .replace("\t", "").replace("\r\n", ""))
    # singer = pq_content('span.cover').attr("title")
    jsons = pq_content(".tools")
    hots =pq_content(".heatValue")
    # 判定是否重复 
    flag = 0
    if len(jsons) <= 0:
        return False
    for i in xrange(len(jsons)):
        out_str = jsons.eq(i).attr('data-music')
        hot = hots.eq(i).attr("style")[6:-1]
        j = json.loads(out_str.encode("utf-8"))
        j.pop("pay")
        j["HN"] = int(hot)
        if artist != "" :
            j["风格"] = artist
        #print j['name'].decode("utf-8")
        if j["id"] in uniq:
            flag += 1
            continue
        uniq.add(j['id'])
        j['acc_url'] = getAcc(j['id'])
        fout.write(json.dumps(j,ensure_ascii = False) + "\n")
        fout.flush()
    if flag ==len(jsons):
        return False

def get_url(s):
    '''组装url'''
    s = "http://www.kuwo.cn/artist/contentMusicsAjax?artistId="+ s + "&pn=0&rn=5000"
    #s = "http://music.baidu.com/data/user/getsongs?start=" + str(n) + "&ting_uid=" + s + "&order=hot&hotmax=0&pay="
    #s = "http://music.baidu.com/tag/" + s + "?start=" + str(n) + "&size=25&third_type=0"
    return s

def get_artist(fout):
    '''爬取歌手页面'''
    for i in xrange(5555):
        try:
            url = "http://www.kuwo.cn/artist/indexAjax?pn="
            content = urllib2.urlopen(url + str(i), timeout = 10).read()
            typeEncode = sys.getfilesystemencoding()  # 系统默认编码
            infoencode = chardet.detect(content).get('encoding', 'utf-8')
            content = content.decode(infoencode, 'ignore') \
                .encode(typeEncode)
            feed(content,fout)
        except:
            continue


if __name__ == "__main__":
    # url = "http://music.baidu.com/artist"
    fout = open(sys.argv[1], 'a')
    fartist = open(sys.argv[3], 'w')
    get_artist(fartist)
    fartist.close()
    n=0
    for line in open(sys.argv[2], 'r'):
        n+=1
        #if n < 25874 :
        #    continue
        try:
            url = "http://www.kuwo.cn/" + line.strip()
            uid = find_id(url)
            #artist = line.strip().split("=")[-1]
            artist = ""
            url = get_url(uid)
            #print uid, artist
            #print url
            #url = "http://www.kuwo.cn/bang/content?name=" + line.strip()
            #artist = line.strip().replace("榜","").replace("酷我","")
            return_data(url, fout, artist)
        except Exception, e:
            print e
            continue
    fout.close()
