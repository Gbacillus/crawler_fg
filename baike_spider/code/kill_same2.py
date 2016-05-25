# coding:utf-8
import sys
uniq= set()
'''输出替换词'''
for line in sys.stdin:
    ls = line.strip().split(" ")
    key = ls[0]
    for l in ls[1:]:
        if l in uniq:
            continue
        uniq.add(l)
        print l + " " + key
