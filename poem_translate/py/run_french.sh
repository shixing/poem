model=/home/nlg-05/xingshi/lstm/model/Fre_Eng_lc_d_att_4M/best.nn
#model=/home/nlg-05/xingshi/lstm/model/Fre_Eng_lc_d/best.nn.new
data=/home/nlg-05/xingshi/lstm/poem/poem_translate/data/french
fsa4=$data/fsa4
fsa3=$data/fsa3
fsa1=$data/fsa1
source=$data/source
output=$data/output
python run_french.py $model $source.single.1 $fsa1 $output.single.1 0
#python run_french.py $model $source.1 $fsa4 $output.1 1
#python run_french.py $model $fsa4 $source.2 $output.2
#python run_french.py $model $fsa3 $source.3 $output.3
#python run_french.py $model $fsa3 $source.4 $output.4

#echo "" > nl.txt
#cat $output.1 nl.txt  $output.2 nl.txt  $output.3 nl.txt  $output.4 > $output
#rm nl.txt
