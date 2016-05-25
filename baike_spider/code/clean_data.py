# coding:utf-8
import sys
import re
import string
import unicode_tool as ut
fright = open(sys.argv[1], 'w')
ferror = open(sys.argv[2], 'w')
#r = re.compile(ur'[\u4e00-\u9fa5a-zA-Z0-9]')
for line in sys.stdin:
    line = line.strip().replace(" ", "").replace('“', "").replace("”", "").replace("《", "").replace("》", "").replace("：", "")
    line = re.sub(re.compile(ur"\[\d+\]"), "", line, re.S | re.I)
    line = re.sub(re.compile(ur"（.*?）"), "", line, re.S | re.I)
    identify = string.maketrans('', '')
    delEStr = string.punctuation.replace(',','').replace(';','').replace(".","").replace("_","")
    line = line.translate(identify, delEStr) 
    ls = line.split("\t")
    flag = 0
    for l in ls:
        if l == "alias":
            flag = 0
            break
        if len(ls)!=3:
            flag = 1
            break
        if l == "括号":
            flag = 1
            break
        if len(ls[0]) > 24:
            flag = 1
            break
        try:# 纯数字关系不要
            float(ls[1])
            flag = 1
            break
        except:
            pass
        l = l.decode("utf-8")
        alphabet = 0
        for t in ls[0].decode("utf-8"):
            if not ut.is_chinese(t):
                flag = 1
                break
            if ut.is_alphabet(t):
                alphabet +=1
            # if ut.is_other(t):# 有各种符号的不要
                # flag = 1
            #     break
        if alphabet == len(l) and len(l) > 3:
            flag = 1
            break
        if flag == 1:
            break
    if flag == 1:
        ferror.write(line+"\n")
    if flag == 0:
        fright.write(line+"\n")
fright.close()
ferror.close()
