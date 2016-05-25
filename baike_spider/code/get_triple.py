# coding:utf-8
import sys
triples = {}
for line in open("../baike_triple.new", "r"):
    ls = line.strip().split("\t")
    if len(ls) < 3 or ls[0] in ls[2] or ls[0] in ls[1] or ls[2] in ls[1] or len(ls[0]) < 4:
        continue
    if ls[0] in triples:
        triples[ls[0]].append(ls[1:])
    triples[ls[0]] = [ls[1:]]
n = 0
for line in sys.stdin:
    n += 1
    #if n < 133665:
    #    continue
    try:
        ls = line.strip().split("。")
        for l in ls:
            flag = 0
            for k in triples.keys():
                if k in l:
                    for vv in triples[k]:
                        for v in vv:
                            if v in l:
                                print l + "\t",
                                print k + " " + ' '.join(vv)
                                break
    except:
        continue
