# coding:utf-8
import sys
import json
import re
reload(sys)
sys.setdefaultencoding("utf-8")
##提取三元组，加别名
r = re.compile(ur"[\(\[\（\【\{\{].*?[\)\]\）\】\}\}]")
name_list = [u"别称", u"别名", u"又名", u"又称", u"外文名", u"别字", u"别号", u"中文别名", u"小名", u"幼名", u"简称", u"尊号", u"字号", u"谥号", u"另名", u"曾用名", u"尊称", u"外号", u"外文别名", u"亦名"]
def extract_alias():    
    fout = open(sys.argv[3],'w')
    for line in open(sys.argv[2], 'r'):
        try:
            j = json.loads(line.strip().replace("\\n", "，").replace("\\t", "").replace(';','，').replace("\\","，").replace("、","，").replace("；","，").replace(" ","").replace("/","，"))

            if len(j) < 3:
                continue
            first = j.pop('title').replace(",","，")
            j.pop("url")
            first = re.sub(r, "", first)
            for n in name_list:
                if n in j and j[n] != "":
                    names = re.sub(re.compile(ur"[\\、；，/]"),";",j[n])
                    if len(names.strip()) <2:
                        continue
                    if ',;' in first:
                        first += names + ";"
                    else:
                        first += ",;" + names +";"
            if ',;' in first:
                fout.write(first+"\n")
            for k, v in j.iteritems():
                k = k.encode("utf-8").replace(" ","").replace(",","")
                v = v.encode("utf-8").replace(" ","").replace(",","")
                if "，" in v:
                    for vv in v.strip().split("，"):
                        print first.strip() + "\t" + k.strip() + "\t" + vv.strip()
                # elif  ";" in v:
                    # for vv in v.strip().split(";"):
                        # print first.strip() + "\t" + k.strip() + "\t" + vv.strip()
                # elif "," in v:
                    # for vv in v.strip().split(","):
                        # print first.strip() + "\t" + k.strip() + "\t" + vv.strip()
                # elif "；" in v:
                    # for vv in v.strip().split("；"):
                        # print first.strip() + "\t" + k.strip() + "\t" + vv.strip()
                # elif '\\' in v:
                    # for vv in v.strip().split("\\"):
                     #    print first.strip() + "\t" + k.strip() + "\t" + vv.strip()
                else:
                    print first.strip() + "\t" + k.strip() + "\t" + v.strip()
        except Exception,e:
            #print e
            continue
    fout.close()
#直接提取三元组
def extract_triple():
    for line in open("../city.utf8", 'r'):
        city = line.strip().split("|")[-1]
        print  city + "\t天气\tweather_service"
    for line in open(sys.argv[2], 'r'):
        try:
            j = json.loads(line.strip().replace("\\n", "，").replace("\\t", "").replace(';','，').replace("\\","，").replace("、","，").replace("；","，").replace(" ","").replace("/","，"))

            if len(j) < 3:
                continue
            first = j.pop('title').replace(",","，")
            j.pop("url")
            first = re.sub(r, "", first)
            for k, v in j.iteritems():
                k = k.encode("utf-8").replace(" ","").replace(",","")
                v = v.encode("utf-8").replace(" ","").replace(",","")
                if k in name_list:
                    k = "别名"
                if "，" in v:
                    for vv in v.strip().split("，"):
                        print first.strip() + "\t" + k.strip() + "\t" + vv.strip()
                # elif  ";" in v:
                    # for vv in v.strip().split(";"):
                        # print first.strip() + "\t" + k.strip() + "\t" + vv.strip()
                # elif "," in v:
                    # for vv in v.strip().split(","):
                        # print first.strip() + "\t" + k.strip() + "\t" + vv.strip()
                # elif "；" in v:
                    # for vv in v.strip().split("；"):
                        # print first.strip() + "\t" + k.strip() + "\t" + vv.strip()
                # elif '\\' in v:
                    # for vv in v.strip().split("\\"):
                     #    print first.strip() + "\t" + k.strip() + "\t" + vv.strip()
                else:
                    print first.strip() + "\t" + k.strip() + "\t" + v.strip()
        except Exception,e:
            #print e
            continue

if __name__ == "__main__":
    flag = sys.argv[1]
    if flag == "alias":
        extract_alias()
    elif flag == "triple":
        extract_triple()
