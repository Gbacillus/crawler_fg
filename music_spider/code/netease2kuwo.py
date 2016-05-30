#coding:utf-8
'''网易歌单数据归约到酷我歌单的类别'''
import sys
dic = {}
for line in open("class_netease",'r'):
    ls = line.strip().split('\t')
    if len(ls)<2:
        continue
    dic[ls[0]] = ls[-1]

for line in sys.stdin:
    ls = line.strip().split('\t')
    if ls[0] in dic:
        ls[0] = dic[ls[0]]
    print '\t'.join(ls)
