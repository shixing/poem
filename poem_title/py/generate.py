import os
import sys

head = """
#!/bin/bash
#PBS -q isi
#PBS -l walltime=300:00:00
#PBS -l gpus=2

PY_FORMAT=/home/nlg-05/xingshi/lstm/single_layer_gpu_google_model/Scripts/bleu_format_valid.py
PERL_BLEU=/home/nlg-05/xingshi/workspace/tools/mosesdecoder/scripts/generic/multi-bleu.perl



id=__PREFIX__
model_folder=/home/nlg-05/xingshi/lstm/poem/poem_title/model/${id}/
output_folder=/home/nlg-05/xingshi/lstm/poem/poem_title/decode
data_folder=/home/nlg-05/xingshi/lstm/poem/poem_title/data
EXEC=/home/nlg-05/xingshi/lstm/exec/ZOPH_RNN
fe_nn=/home/nlg-05/xingshi/lstm/model/Fre_Eng_lc_d/best.nn.new
fe_nn_attention=/home/nlg-05/xingshi/lstm/model/Fre_Eng_lc_d/best.nn.new

SRC_TRN=$data_folder/train_content.txt
TGT_TRN=$data_folder/train_title.txt
SRC_DEV=$data_folder/valid_content.txt
TGT_DEV=$data_folder/valid_title.txt

TGT_TST=$data_folder/test_title.txt
SRC_TST=$data_folder/test_content.txt
LOG=$output_folder/${id}.log
OUTPUT=$output_folder/${id}.kbest
REF=$output_folder/${id}.ref
BLEU=$output_folder/${id}.bleu

mkdir $model_folder
cd $model_folder

__cmd__


"""

cmd_train = "$EXEC --logfile HPC_OUTPUT_NEW.txt -B best.nn --screen-print-rate 300 -N 2 -M 0 0 1 -n 20 -A 0.5 -w 5 --attention-model true --feed-input true -m 64 -a $SRC_DEV $TGT_DEV -t $SRC_TRN $TGT_TRN model.nn"

cmd_decode = """$EXEC -k 1 $model_folder/best.nn $OUTPUT --decode-main-data-files $SRC_TST -L 100 -b 12 --dec-ratio 0.0 0.5
python $PY_FORMAT $OUTPUT $TGT_TST $REF
perl $PERL_BLEU -lc $REF < $OUTPUT.bleu > $BLEU
"""

def train_decode():
    
    def h(val):
        return "h{}".format(val), "-H {}".format(val)

    def d(val):
        return "d{}".format(val), "-d {}".format(val)

    def l(val):
        return "l{}".format(val), "-l {}".format(val)
    
    def vocab(val):
        if val == 'full':
            return "Full", '-v 50000 -V 50000'
        elif val == 'freq':
            return "Freq", '-v 50000 -V 9000'

    funcs = [h,d,l,vocab]
    template = [256,0.8,1.0,'full']
    params = []

    _hs = [256,512,1024]
    _ds = [0.5,0.8]
    _ls = [0.5,1.0]
    _vocabs = ["full","freq"]

    gen = ((x,y,z,w) for x in _hs for y in _ds for z in _ls for w in _vocabs)

    for _h,_d,_l,_vocab in gen:
        temp = list(template)
        temp[0] = _h
        temp[1] = _d
        temp[2] = _l
        temp[3] = _vocab
        params.append(temp)

    
    def get_name_cmd(paras):
        name = ""
        cmd = [cmd_train]
        for func, para in zip(funcs,paras):
            n, c = func(para)
            name += n
            cmd.append(c)

        name = name.replace(".",'')

        cmd = " ".join(cmd)
        return name, cmd

    # train
    for para in params:
        name, cmd = get_name_cmd(para)
        fn = "../sh/{}.sh".format(name)
        f = open(fn,'w')
        content = head.replace("__cmd__",cmd).replace("__PREFIX__",name)
        f.write(content)
        f.close()

    # decode
    for para in params:
        name, cmd = get_name_cmd(para)
        fn = "../sh/{}.decode.sh".format(name)
        f = open(fn,'w')
        content = head.replace("__cmd__",cmd_decode).replace("__PREFIX__",name)
        f.write(content)
        f.close()

            

if __name__ == "__main__":
    train_decode()

    

    
    
