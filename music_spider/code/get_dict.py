# coding:utf-8
'''输出词库'''
import sys
for line in sys.stdin:
    ls = line.strip().split(",")
    if ls[-1] in ["MUSIC", "PERSON"]:
        print ls[1]
