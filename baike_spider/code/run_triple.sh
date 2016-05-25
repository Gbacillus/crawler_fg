flag=$1
out_file=$2
echo "三元组处理"
python extract_tripe.py $1 ../baike_result.json |sort|uniq>../baike_triple.bak
#cat ../baike_triple.bak |sort|uniq| python replace3.py >../baike_triple
cat ../baike_triple.bak |python clean_data.py ../baike_triple.right ../baike_triple.error
python kill_same.py ../CoreSynonym.txt ../baike_triple.right | python kill_same2.py >../baike_words.pair
python kill_same3.py ../baike_words.pair ../baike_triple.right |uniq > ../$out_file
