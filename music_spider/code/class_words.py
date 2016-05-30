# coding:utf-8
# 利用jieba分词提取关键词
# 输入歌单名文件，输出关键词
import sys
import jieba.analyse
reload(sys)
sys.setdefaultencoding('utf-8')
style_dic = {}

def jieba_words():
    for line in open(sys.argv[1], 'r'):
        try:
            style,sentence = line.strip().split('\t')
        except Exception, e:
            continue
        style_dic.setdefault(style, [])
        style_dic[style].append(sentence)
    for k, v in style_dic.iteritems():
        sentence = '\n'.join(v)
        words = jieba.analyse.extract_tags(sentence,30)
        print k + "\t" + " ".join(words)

def pyltp_words():
    from pyltp import Segmentor, Postagger
    segmentor = Segmentor()
    segmentor.load("/home/fredgan/github/pyltp/ltp_data/cws.model")
    # postagger = Postagger()    
    # postagger.load("~/github/pyltp/ltp_data/cpos.model")
    for line in open(sys.argv[1], 'r'):
        try:
            style,sentence = line.strip().split('\t')
        except:
            continue
        style_dic.setdefault(style, {})
        words = segmentor.segment(sentence)
        # postags = postagger.postag(words)
        for w in words:
            if w in style_dic[style]:
                style_dic[style][w] += 1
            else:
                style_dic[style][w] = 1

    for k,v in style_dic.iteritems():
        v_list = sorted(v.iteritems(), key = lambda d:d[1], reverse = True)
        print k+ "\t" + " ".join(map(lambda i:i[0] + ":" +str(i[1]), v_list[0:min(50,len(v_list))]))

if __name__ == "__main__":
    jieba_words()
