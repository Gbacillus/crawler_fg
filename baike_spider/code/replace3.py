# coding:utf-8
import sys
words = {}
for line in open("../baike_words.same", 'r'):
    key = line.strip().split(",;")[0]
    words[key] = line.strip()

for line in open("../city.utf8", 'r'):
    city = line.strip().split("|")[-1]
    if city in words:
        print  words[city] + "\t天气\tweather_service"
    else:
        print  city + "\t天气\tweather_service"
for line in sys.stdin:
    ls = line.strip().split("\t")
    try:
        if ls[2] in words:
            ls[2] = words[ls[2]]
        print "\t".join(ls)
    except:
        continue



