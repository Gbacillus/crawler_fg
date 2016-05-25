from tgrocery import Grocery
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
def train_set(path1):
    for line in open(path1,"r"):
        try:
            j = json.loads(line.strip())
            print j["list_name"] + "\t" +j["style"]
        except:
            continue

def train(path,name):
    grocery = Grocery(name)   
    grocery.train(path)
    grocery.save()

if __name__ == "__main__":
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
