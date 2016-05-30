# coding:utf-8
'''输出音乐风格同义词库'''
import sys
for line in sys.stdin:
    ls = line.strip().split("\t")
    for l in ls[1].strip().split(" "):
        print l + " " + ls[0]
