# coding:utf-8
'''按歌单爬取酷我歌曲，有风格信息'''
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
    '''通过url返回网页内容'''
    flag = 5
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

def cra_list(content, style):
    '''按风格爬取酷我歌单列表'''
    lists = []
    names = pq(content)("a.m_name")
    for i in xrange(len(names)):
        name = names.eq(i).text()
        url = "http://yinyue.kuwo.cn" + names.eq(i).attr("href")
        if "cate_" in url:
            lists_more = cra_list(url2content(url), name)
            lists += lists_more
        else:
            lists.append((name, url, style))
    return lists

def cra_song(content):
    '''爬取歌单中的歌曲信息'''
    json_str = re.search(ur"jsonm = (.*)\}\;", content).group()
    json_str = json_str.replace("jsonm = ","").replace(";","")
    j = json.loads(json_str)
    if len(j)<1 or "musiclist" not in j:
        return []
    songs = j["musiclist"]
    return songs

if __name__ == "__main__":
    # url = "http://yinyue.kuwo.cn/yy/cinfo_24007.htm"
    poplist =["formats", "new", "nsig1", "nsig2", "mp3sig2", "mp3sig1", "mp3rid", "mkvnsig1", "mkvnsig2", "mkvrid", "hasecho"]
    fout = open(sys.argv[2], "w")
    n = 0
    for line in open(sys.argv[1], "r"):
        n += 1
        # if n < 18:
        #    continue
        url, style = line.strip().split("\t")
        print url
        lists = cra_list(url2content(url), style)
        for name, url, style in lists:
            print url
            try:
                songs = cra_song(url2content(url))
                for j in songs:
                    try:
                        for k in poplist:
                            if k in j:
                                j.pop(k)
                        j["style"] = style
                        j["list_name"] = name
                        if (style + j["musicrid"]) in uniq:
                            continue
                        uniq.add(style + j["musicrid"])
                        fout.write(json.dumps(j, ensure_ascii = False) + "\n")
                    except:
                        continue
            except:
                continue
    fout.close()
