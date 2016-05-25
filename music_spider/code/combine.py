# coding:utf-8
import sys
artist = {}
for line in open(sys.argv[1], 'r'):
    ls = line.strip().split("\t")
    uid = ls[0][8:]
    art = ls[1]
    artist[uid] = art

for line in open(sys.argv[2], 'r'):
    ls = line.strip().split("\t")
    if ls[1] in artist:
        print ls[0] + "\t" + artist[ls[1]]
