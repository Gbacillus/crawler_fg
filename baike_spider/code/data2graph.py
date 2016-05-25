# coding:utf-8
import sys
nodes = {}
n = 0
fnode = open(sys.argv[1], 'w')
fedge = open(sys.argv[2], 'w')
for line in sys.stdin:
    ls = line.strip().split("\t")
    if len(ls) < 3:
        continue
    if ls[0] not in nodes:
        nodes[ls[0]] = n
        fnode.write(str(n) + "," + ls[0] +  ",EVA" + "\n")
        n += 1
    if ls[2] not in nodes:
        nodes[ls[2]] = n
        fnode.write(str(n) + "," + ls[2] + ",EVA" + "\n")
        n += 1
    fedge.write(str(nodes[ls[0]]) + "," + ls[1] + "," + str(nodes[ls[2]]) + ",outE" + "\n")
fnode.close()
fedge.close()
