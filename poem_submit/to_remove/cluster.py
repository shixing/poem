# python cluster.py topic
# e.g.: python cluster.py civil war

import sys
import subprocess as sp
import os
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn import preprocessing

root_dir = os.path.abspath(__file__ + "/../../")
fsas_dir = os.path.join(root_dir,"fsas/")
topic_dir = os.path.join(root_dir,"topic/")
path1000 = os.path.join(fsas_dir,"1000_vector.txt")

def process_topic(topic):
    topic = topic.lower()
    for i in xrange(len(topic)):
        if not topic[i] == "_":
            if not topic[i].isalpha():
                tmp = topic[i]
                topic = topic.replace(tmp,"_")

    topic = '{}'.format(" ".join(topic.split("_")))
    return topic

def load_vector(fn):
    X = np.zeros((1001,200))
    words = []
    f = open(fn)
    i = 0
    for line in f:
        ll = line.split()
        words.append(ll[0])
        for j in xrange(200):
            v = float(ll[j+1])
            X[i,j] = v
        i += 1
    f.close()
    return X, words

def cluster(X):
    X = preprocessing.normalize(X, norm='l2')
    distance = X.dot(X.transpose())
    c = AffinityPropagation(affinity="precomputed")
    y = c.fit_predict(distance)
    return y

def main():
    topic = " ".join(sys.argv[1:])
    topic = process_topic(topic)

    cmd = ["bash", "run-for_subtopic.sh", topic, path1000]
    
    sp.call(cmd, cwd=topic_dir)
    
    X,words = load_vector(path1000)
    
    os.remove(path1000)

    labels  = cluster(X)
    
    cc = {}
    
    for i in xrange(len(labels)):
        l = labels[i]
        if not l in cc:
            cc[l] = []
        cc[l].append(words[i])

    count = []
    for l in cc:
        count.append((l,len(cc[l])))
    
    count = sorted(count,key=lambda x: -x[1])
    for l, c in count:
        for word in cc[l]:
            print word, l


main()
