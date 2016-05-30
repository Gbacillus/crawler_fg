# coding:utf-8
# 爬取酷我音乐的acc流
import sys
import json
import chardet
import urllib2
reload(sys)
sys.setdefaultencoding('utf-8')
crawled = set()  # 已爬取
def getAcc(sid):
    url = "http://antiserver.kuwo.cn/anti.s?rid=" + sid + "&format=aac%7Cmp3&response=url&type=convert%5Furl"
    flag = 0
    while(flag != 1):
        try:
            content = urllib2.urlopen(url,  timeout = 10).read()
            flag = 1
        except:
            continue
    return content
if __name__ == "__main__":
    n = 0
    for line in open(sys.argv[1], 'r'):
        n += 1
        #if n <211814:
        #    continue
        j = json.loads(line.strip())
        sid = j['id']
        #typeEncode = sys.getfilesystemencoding()  # 系统默认编码
        #infoencode = chardet.detect(content).get('encoding', 'utf-8')
        #content = content.decode(infoencode, 'ignore') \
        #    .encode(typeEncode)
        j['download_url'] = getAcc(sid)
        print json.dumps(j,ensure_ascii = False)
