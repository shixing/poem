import os
import sys

fn_model = sys.argv[1] # the model file

def load_vocab(fn):
    d = {}
    f = open(fn)
    f.readline()
    f.readline()
    for line in f:
        if line.startswith("===="):
            break
        ll = line.decode('utf8').split()
        word = ll[1]
        d[word] = int(ll[0])
    f.close()
    print len(d)
    return d

def highlight(d):
    n = 0
    nunk = 0
    for line in sys.stdin:
        line = line.decode("utf8").strip()
        ll = line.split()
        newll = []
        for word in ll:
            if not word in d:
                word = "<UNK>:" + word
                nunk += 1
            newll.append(word)
            n +=1
        print " ".join(newll).encode("utf8")
    print "UNK/Total = {}/{} = {}".format(nunk,n,nunk*1.0/n)

d = load_vocab(fn_model)
highlight(d)



