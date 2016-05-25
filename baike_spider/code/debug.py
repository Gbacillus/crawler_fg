# coding:utf-8
import sys
for line in sys.stdin:
    if "\talias\t" in line:
        line = line.strip().replace("\talias\t","\t别名\t")
    print line.strip()
