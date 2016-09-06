# usage: python run.py civil war

import os
import sys
import random
import subprocess as sp
import multiprocessing

root_dir = os.path.abspath(__file__ + "/../../")
fsas_dir = os.path.join(root_dir,"fsas/")
topic_dir = os.path.join(root_dir,"topic/")

encourage_list = {}

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

def decorate_results(poem,encourage_dict):
    lines = []
    for line in poem.split("\n"):
        ll = line.split()
        new_ll = []
        for word in ll:
            w = word.lower()
            if w.endswith(".") or w.endswith(","):
                w = w[:-1]
            if w in encourage_dict:
                new_ll.append("*{}*".format(word))
            else:
                new_ll.append(word)
        new_line = " ".join(new_ll)
        if len(ll) == 0:
            lines.append("")
        else:
            lines.append(new_line)
    return "\n".join(lines)


def main():
    # settings
    beam_size = 50
    
    
    
    #process topic

    #load topics
    topics = []
    encourage_weights = [0.0,1.0]

    f = open(sys.argv[1])
    for line in f:
        topics.append(line.strip())
    f.close()

    fout = open(sys.argv[2],'w')
    
    for topic in topics:

        r = random.randint(1, 100000)
        fsa_path = os.path.join(fsas_dir, "fsa.{}".format(r))
        source_path = os.path.join(fsas_dir, "source.{}".format(r))
        rhyme_path = os.path.join(fsas_dir, "rhyme.{}".format(r))
        encourage_path = os.path.join(fsas_dir, "encourage.{}".format(r))
        output_path = os.path.join(fsas_dir,"kbest.{}".format(r))
        model_path = os.path.join(root_dir,"model/lyrics.tl.nn")
        rnn_path = os.path.join(root_dir,"a.out")

        topic = process_topic(topic)
    
        # generate the fsa
    
        cmd = ["bash", "run.sh", topic, fsa_path, source_path, rhyme_path, encourage_path]
        
        #print cmd

        sp.call(cmd, cwd=topic_dir)

        # load encourage_dict
        encourage_dict = {}
        with open(encourage_path) as f:
            for line in f:
                encourage_dict[line.strip()] = 1

    # generate the poem
        for encourage_weight in encourage_weights:
            cmd = [rnn_path]
            cmd += "--adjacent-repeat-penalty -2.0 --repeat-penalty -3.0".split()
            cmd += ("-L 160 -b {}".format(beam_size)).split()
            cmd += ("-k 1 {} {} {}".format(source_path,model_path,output_path)).split()
            cmd += ("--fsa {}".format(fsa_path)).split()
            cmd += ("--encourage-list {} --encourage-weight {}".format(encourage_path, encourage_weight)).split()
            cmd += "--dec-ratio 0.0 100.0".split()
            if encourage_weight > 0:
                cmd += "--encourage-partially 1".split()

            env = {}
            env["OMP_NUM_THREADS"] = str(multiprocessing.cpu_count())
            p = sp.Popen(cmd,cwd=root_dir,stdout=sp.PIPE, stderr=sp.PIPE,env=env)
            out, err = p.communicate()
            #print out
    
            # postprocess the poem
            poem = process_results(output_path)
            
            poem = decorate_results(poem,encourage_dict)
            
            
            # print the poem to STDOUT
            fout.write("========\n")
            fout.write("Topic: {}\n".format(topic))
            fout.write("Encourage Weight: {}\n".format(encourage_weight))
            if encourage_weight > 0:
                fout.write("Encourage partially\n")
            fout.write("--------\n")
            fout.write(poem)
            fout.flush()
        
        cleanup([fsa_path,source_path,rhyme_path,encourage_path])

    fout.close()
        
if __name__ == "__main__":
    main()
