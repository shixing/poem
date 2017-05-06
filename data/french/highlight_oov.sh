model=/home/nlg-05/xingshi/lstm/model/Fre_Eng_lc_d/best.nn

python highlight_oov.py $model < test.fr.tok.lc > test.fr.tok.lc.oovhl
