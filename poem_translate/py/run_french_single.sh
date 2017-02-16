model=/home/nlg-05/xingshi/lstm/model/Fre_Eng_lc_d_att_4M/best.nn
data=/home/nlg-05/xingshi/lstm/poem/data/french
fsa1=$data/fsa1
source=$data/source
output=$data/output

for i in 1 2 3 4; do
echo $i
python run_french.py $model $source.single.${i} $fsa1 $output.single.${i} 1
cat $output.single.${i} >> $output.single.fsa
done

for i in 1 2 3 4; do
echo $i
python run_french.py $model $source.single.${i} $fsa1 $output.single.${i} 0
cat $output.single.${i} >> $output.single.wofsa
done

#i=1

#python run_french.py $model $source.nopunk.${i} $fsa4 $output.nopunck.${i}.fsa 1

#python run_french.py $model $source.nopunk.${i} $fsa4 $output.nopunck.${i} 0





#python run_french.py $model $fsa4 $source.2 $output.2
#python run_french.py $model $fsa3 $source.3 $output.3
#python run_french.py $model $fsa3 $source.4 $output.4

#echo "" > nl.txt
#cat $output.1 nl.txt  $output.2 nl.txt  $output.3 nl.txt  $output.4 > $output
#rm nl.txt
