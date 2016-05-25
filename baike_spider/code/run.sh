#!/bin/bash
flag=$1
out_file=$2
if [ $flag = "alias" ];then
    echo "别名处理"
    python extract_tripe.py $1 ../baike_result.json ../baike_words.same >../baike_triple.bak
    cat ../baike_triple.bak |sort|uniq| python replace3.py >../baike_triple
    cat ../baike_triple |python clean_data.py ../baike_triple.right ../baike_triple.error
    python kill_same.py ../CoreSynonym.txt ../baike_triple.right  >../baike_words.pair
    python kill_same3.py ../baike_words.pair ../baike_triple.right |uniq>../$out_file

elif [ $flag = "triple" ];then
    echo "三元组处理"
    #python extract_tripe.py $1 ../baike_result.json |sort|uniq>../baike_triple.bak
    cat ../baike_triple.bak |python clean_data.py ../baike_triple.right ../baike_triple.error
    python kill_same.py ../CoreSynonym.txt ../baike_triple.right >../baike_words.pair
    python kill_same3.py ../baike_words.pair ../baike_triple.right |uniq>../$out_file
    cat ../$out_file | python data2graph.py ../vertex ../edge
else
    echo "参数输入错误"
fi

