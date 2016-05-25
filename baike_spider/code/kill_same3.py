# coding:utf-8
import sys
'''替换三元组中的同义词'''
# parm1 同义词库
# parm2 三元组
words_map = {}
for line in open(sys.argv[1], 'r'):
    ls = line.strip().split(" ")
    words_map[ls[0]] = ls[1]

for line in open(sys.argv[2], 'r'):
    ls = line.strip().split("\t")
    flag = 0
    try:
        l = ls[1]
        if l in words_map:
            ls[1] = words_map[l]
            flag = 1
    # print line.strip()
    # if flag == 1:
    except:
        continue
    print "\t".join(ls)
