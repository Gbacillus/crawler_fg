# coding:utf-8
# import unicode_tool as ut
import sys
import json
import re
reload(sys)
sys.setdefaultencoding("utf-8")
# 输出点和边文件
fnode = open(sys.argv[2], 'w')
fedge = open(sys.argv[3], 'w')
nodes = {}
n = 0
person_heat = {}

def clean_title(title):
    title = title.replace("《","").replace("》","").replace(" ","") \
        .replace(".","").replace(",","").replace("-","").lower()
    return title
def triple2graph(sub, j):
    global n, nodes
    count = n
    fnode.write(str(count) + "," + sub + ",MUSIC" + "\n")
    n += 1
    for k,v in j.iteritems():
        if k in "lyrics":
            continue
        if k == "url":
            k = "play_url"
            v = "http://music.baidu.com" + v
        if k == "tags":
            for obj in v:
                if len(obj) < 1 :
                    continue
                rel, tag = rel2tags("tags")
                if len(obj) <1:
                    continue
                if obj not in nodes:
                    nodes[obj] = n
                    fnode.write(str(n) + "," + obj + "," + tag + "\n")
                    n += 1
                if tag != "HN":
                    tag = "outE"
                fedge.write(str(count) + "," + rel + "," + str(nodes[obj]) + "," + tag + "\n")
        else:
            rel, tag = rel2tags(k)
            if rel not in["play_url", "acc_url", "download_url"]:
                obj = clean_title(str(v))
            else:
                obj = v
            if len(obj) <1:
                continue
            if obj not in nodes:
                nodes[obj] = n
                fnode.write(str(n) + "," + obj + "," + tag.replace("HN", "EVA") + "\n")
                n += 1
            if tag != "HN":
                tag = "outE"
            fedge.write(str(count) + "," + rel + "," + str(nodes[obj]) + "," + tag + "\n")
            

def rel2tags(rel):
    tag = "EVA"
    if rel in ["singers" ,"artist"]:
        rel = "歌手"
        tag = "PERSON"
    elif rel == "nums" or rel == "HN":
        rel = "hot_num"
        tag = "HN"
    elif rel == "album":
        rel = "专辑"
    elif rel == "id":
        rel = "play_url"
    elif rel in ["tags", "classify"]:
        rel = "风格"
        tag = "EVA"
    else:
        pass
    return rel, tag

def kuwo2graph(sub, j):
    global n, nodes
    count = n
    n += 1
    'Get The Party Started (Radio Mix)'
    if '(' in sub or '(' in sub:
        title = re.findall(r"[\(].*?[\)]", sub.encode('utf-8'))
        for version in title:
            sub = sub.replace(version, "")
            if version not in nodes:
                version = version.replace("(", "").replace(")","")
                nodes[version] = n
                fnode.write(str(n) + "," + version + ",EVA" + "\n")
                n += 1
            fedge.write(str(count) + ",版本," + str(nodes[version]) + ",outE" + "\n")
    fnode.write(str(count) + "," + sub + ",MUSIC" + "\n")
    rid = j["id"][6:]
    for k,v in j.iteritems():
        obj = clean_title(str(v))
        if len(obj) <1:
            continue
        rel, tag = rel2tags(k)
        if k == "HN":
            HN = int(obj)
        elif rel == "play_url":
            obj = "http://www.kuwo.cn/yinyue/" + v[6:]
        elif rel in ["acc_url", "download_url"]:
            rel = "music_id"
            obj = rid
        else:
            pass
        if rel =="歌手":
            artists = obj.split("&")
            for obj in artists:
                if obj+"PERSON" not in nodes:
                    nodes[obj+"PERSON"] = n
                    fnode.write(str(n) + "," + obj + ",PERSON" + "\n")
                    n += 1
                if tag != "HN":
                    tag = "outE"
                fedge.write(str(count) + "," + rel + "," + str(nodes[obj+"PERSON"]) + "," + tag + "\n")
        else:
            if obj not in nodes:
                nodes[obj] = n
                fnode.write(str(n) + "," + obj + "," + tag.replace("HN", "EVA") + "\n")
                n += 1
            if tag != "HN":
                tag = "outE"
            fedge.write(str(count) + "," + rel + "," + str(nodes[obj]) + "," + tag + "\n")
    # 计算歌手热度
    for artist in artists:
        person_heat.setdefault(artist, [])
        person_heat[artist].append(HN)

if __name__ == "__main__":
    for line in open(sys.argv[1], 'r'):
        try:
            j = json.loads(line.strip().replace("\\",""))
            title = j.pop('name')
            # j.pop("pay")
            title = clean_title(title)
            if len(title) < 1:
                continue
            # triple2graph(title, j)
            kuwo2graph(title, j)
        except Exception,e:
            continue
    #计算歌手热度
    for k,v in person_heat.iteritems():
        if k in nodes:
            avg = str(float(sum(person_heat[k])) / len(person_heat[k]))
            if avg not in nodes:
                nodes[avg] = n
                fnode.write(str(n) + "," + avg + ",EVA" + "\n")
                n += 1
            fedge.write(str(nodes[k]) + ",hot_num," + str(nodes[avg]) + ",HN" + "\n")
       # flag = 0
    #  for t in title.decode("utf-8"):
        # if ut.is_other(t):
            # flag = 1
            # break
    # if flag == 1:
    #      continue
    fnode.close()
    fedge.close()
