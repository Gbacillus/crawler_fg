# coding:utf-8
# 划分训练集，测试svm分类准确率
from tgrocery import Grocery
import json
import sys
import random
reload(sys)
sys.setdefaultencoding("utf-8")
def train_set(path1):
    for line in open(path1,"r"):
        try:
            j = json.loads(line.strip())
            print j["list_name"] + "\t" +j["style"]
        except:
            continue

def data2tt(path, path1, path2, theta):
    ftrain = open(path1, 'w')
    ftest = open(path2, 'w')
    for line in open(path):
        if random.random() < theta:
            ftest.write(line)
        else:
            ftrain.write(line)
    ftrain.close()
    ftest.close()

def train(path,name):
    grocery = Grocery(name)   
    grocery.train(path)
    grocery.save()

if __name__ == "__main__":
    data2tt(sys.argv[3], sys.argv[1], sys.argv[2], 0.02)
    train(sys.argv[1], "music")
    new_grocey = Grocery("music")
    new_grocey.load()
    n = 0
    for line in open(sys.argv[2],"r"):
        ls = line.strip().split("\t")
        predict = new_grocey.predict(ls[1])
        test = ls[0]
        result = 0
        if test == str(predict):
            result = 1
        n += result
        print predict,test,result
    print n
