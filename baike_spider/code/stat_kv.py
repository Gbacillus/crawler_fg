#coding:utf-8
import sys,json
reload(sys)
sys.setdefaultencoding('utf-8')
k_set={}
for line in open(sys.argv[1],'r'):
    try:
        j=json.loads(line.strip())
        for k,v in j.iteritems():
            if k in k_set:
                k_set[k]+=1
            else:
                k_set[k]=1 
    except:
        continue
k_sort=sorted(k_set.iteritems(),key=lambda d:d[1],reverse=True)
for k,v in k_sort:
    print k+"\t"+str(v)
