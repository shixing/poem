# usage:
# LM:
# -s -k 1 <LM_path> <output_path>
    
# Translation
# -k 1 <source_path> <Translation_Model_path> <output_path>

# common things:
# -b <beam_size>
# --fsa <fsa_path>
# --encourage-list <list_path> --encourage-weight <weight>
# --encourage-partially <1/0>
# --adjacent-repeat-penalty <-2.0>
# --repeat-penalty <-3.0>
#
# example:
# Translation:
# python RunMe_custom.py --adjacent-repeat-penalty -2.0 --repeat-penalty -3.0 -b 50 -k 1 /auto/nlg-05/xingshi/workspace/misc/lstm/poem_submit/fsas/source.64155 /auto/nlg-05/xingshi/workspace/misc/lstm/poem_submit/model/lyrics.tl.nn /auto/nlg-05/xingshi/workspace/misc/lstm/poem_submit/fsas/kbest.64155 --fsa /auto/nlg-05/xingshi/workspace/misc/lstm/poem_submit/fsas/fsa.64155 --encourage-list /auto/nlg-05/xingshi/workspace/misc/lstm/poem_submit/fsas/encourage.64155 --encourage-weight 0.5 --encourage-partially 1
#
# LM:
#
# python RunMe_custom.py --adjacent-repeat-penalty -2.0 --repeat-penalty -3.0 -b 50 -s -k 1 /auto/nlg-05/xingshi/workspace/misc/lstm/poem_submit/model/lyrics.lm.nn /auto/nlg-05/xingshi/workspace/misc/lstm/poem_submit/fsas/kbest.64155 --fsa /auto/nlg-05/xingshi/workspace/misc/lstm/poem_submit/fsas/fsa.64155 --encourage-list /auto/nlg-05/xingshi/workspace/misc/lstm/poem_submit/fsas/encourage.64155 --encourage-weight 0.5 --encourage-partially 1


import os
import sys
import random
import subprocess as sp
import multiprocessing


root_dir = os.path.abspath(__file__ + "/../")
fsas_dir = os.path.join(root_dir,"fsas/")
topic_dir = os.path.join(root_dir,"topic/")


def process_topic(topic):
    topic = topic.lower()
    for i in xrange(len(topic)):
        if not topic[i] == "_":
            if not topic[i].isalpha():
                tmp = topic[i]
                topic = topic.replace(tmp,"_")

    topic = '{}'.format(" ".join(topic.split("_")))
    return topic

def post_process(lines):
    r = random.randint(1, 100000)
    before_path_tp = os.path.join(root_dir, "fsas/before.txt")
    after_path_tp = os.path.join(root_dir, "fsas/after.txt")
    before_path = before_path_tp + ".{}".format(r)
    after_path = after_path_tp + ".{}".format(r)

    f = open(before_path, 'w')
    for line in lines:
        f.write(line.strip() + "\n")
    f.close()
    
    cmd = "bash post_process.sh {} {}".format(before_path, after_path)
    sp.call(cmd.split(), cwd=topic_dir)

    f = open(after_path)
    r = ""
    iline = 0
    for line in f:
        r += line
        iline += 1
        if iline % 4 == 0:
            r += "\n"
    f.close()
    os.remove(before_path)
    os.remove(after_path)
    return r


def process_poem(poem):
    ll = poem.split()[1:-1][::-1]
    newline = "\n"
    newll = []
    for w in ll:
        if w in ['?', '!', '.', ',']:
            w += newline
        newll.append(w)

    lines = ' '.join(newll).split(newline)
    lines = [x.strip() for x in lines]
    poem_str = post_process(lines)
    return poem_str

def process_results(fn):
    f = open(fn)
    poem = "Empty Poem!"
    for line in f:
        if line.startswith("<START>"):
            poem = process_poem(line)
    f.close()
    return poem

def cleanup(fns):
    for fn in fns:
        os.remove(fn)

def cleanup_lstm():
    for name in os.listdir(root_dir):
        if len(name) == 19 and name[4] == "-" and name[9] == "-" and name[14] == "-":
            path = os.path.join(root_dir,name)
            if os.path.isdir(path):
                for name2 in os.listdir(path):
                    path2 = os.path.join(path,name2)
                    os.remove(path2)
                os.removedirs(path)
        
def main():
    # LM:
    # -s -k 1 <LM_path> <output_path>
    
    # Translation
    # -k 1 <source_path> <Translation_Model_path> <output_path>
    
    # common things:
    # -b <beam_size>
    # --fsa <fsa_path>
    # --encourage-list <list_path> --encourage-weight <weight>
    # --encourage-partially <1/0>
    # --adjacent-repeat-penalty <-2.0>
    # --repeat-penalty <-3.0>


    default_cmd = "./a.out -L 160 --dec-ratio 0.0 100.0 "
    addition_cmd = " ".join(sys.argv[1:])
    cmd = default_cmd + addition_cmd
    cmd = cmd.split()

    # generate the poem

    #print " ".join(cmd)
    
    env = {}
    env["OMP_NUM_THREADS"] = str(multiprocessing.cpu_count())
    #print env
    p = sp.Popen(cmd,cwd=root_dir,stdout=sp.PIPE, stderr=sp.PIPE,env=env)
    out, err = p.communicate()
    #print out
    
    # postprocess the poem
    offset = 1
    if '-s' in cmd:
        offset = 0
    index = cmd.index("-k")
    output_path = cmd[index + 3 + offset]
    poem = process_results(output_path)

    # print the poem to STDOUT
    print poem.encode("utf8")

    # clean up the temp files
    #cleanup([fsa_path,source_path,rhyme_path,encourage_path,output_path])
   
    # rm
    cleanup_lstm()

if __name__ == "__main__":
    main()
