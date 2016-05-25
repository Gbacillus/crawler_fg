# codingLutf-8
import sys
citys_set=set()

for line in open("city.utf8",'r'):
    citys_set.add(line.strip().split("|")[-1])

for line in open(sys.argv[1],"r"):
    ls=line.strip().split("\t")
    if len(ls)<3:
        continue
    if ls[0] in citys_set:
        print line.strip()
    elif ls[2] in citys_set:
        print line.strip() 
