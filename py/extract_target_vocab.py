import sys

def load(fn):
    vocab = set()
    f = open(fn)

    ll = f.readline().split()
    f.readline()

    lm = True

    if len(ll) == 4:
        lm = False

    if not lm:
        while True:
            line = f.readline()
            if line.startswith('===='):
                break

    while True:
        line = f.readline()
        if line.startswith("===="):
            break
        ll = line.split()
        word = ll[1]
        vocab.add(word)
    return vocab

d = set()
for i in xrange(1,len(sys.argv)):
    vocab = load(sys.argv[i])
    if len(d) == 0:
        d = vocab
    else:
        d = d.intersection(vocab)
    
for word in d:
    print word
    
