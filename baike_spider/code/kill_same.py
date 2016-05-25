# coding:utf-8
import sys
'''提取三元组中包含同义词林的词'''
# parm1 同义词林
# parm2 三元组
word_dict = {}
for line in open(sys.argv[1], 'r'):
    ls = line.strip().split(" ")
    if "=" not in ls[0]:
        continue
    for l in ls[1:]:
        if l in word_dict:
            word_dict[l] = []
        else:
            word_dict[l] = ls[1:]
uniq = set()
for line in open(sys.argv[2], 'r'):
    ls = line.strip().split("\t")
    try:
        l = ls[1]
        if l in word_dict and len(word_dict[l]) > 0:
            key = ""
            for ll in word_dict[l]:
                if len(ll)<=3:
                    continue
                if key == "":
                    key = ll
                if ll in uniq:
                    continue
                print ll + " " + key
                uniq.add(ll)
            # print l + " " + " ".join(word_dict[l]) 
    except:
        continue
