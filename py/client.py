import sys
import socket
import os
import subprocess as sp
import json
import stat


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask import request, make_response
from datetime import datetime
from nltk import word_tokenize
import random
#from google_datastore import GCStore
import unicodedata

host = "localhost"
ports = [10010]
size = 10240

beams = [50]
interactive_beams = [50]
line_reverses = [1]
interactive_ports = [10020]

root_dir = os.path.abspath(__file__ + "/../../")
fsa_path_tp = os.path.join(root_dir, "fsas/poem.fsa")
source_path_tp = os.path.join(root_dir, "fsas/source.txt")
rhyme_path_tp = os.path.join(root_dir, "fsas/rhyme.txt")
encourage_path_tp = os.path.join(root_dir, "fsas/encourage.txt")
marjan_dir = os.path.join(root_dir, "sonnet-project-for-server/")
before_path_tp = os.path.join(root_dir, "fsas/before.txt")
after_path_tp = os.path.join(root_dir, "fsas/after.txt")
ngram_path = os.path.join(root_dir,"models/5grams.txt")
curse_path = os.path.join(root_dir,"models/curse.txt")
mono_path = os.path.join(root_dir,"models/mono.txt")
sentiment_path = os.path.join(root_dir,"models/sentiment.txt")
concrete_path = os.path.join(root_dir,"models/concrete.txt")

log_path = os.path.join(root_dir,"log/log.txt")

interactive_folder_tp = os.path.join(root_dir, 'fsas_interactive/data')
interactive_folder = interactive_folder_tp

#my_gcstore = GCStore()

################# Plagiarism Check ################# 

def load_ngram():
    d = {}
    #return d
    with open(ngram_path) as f:
        for line in f:
            d[line.strip()] = 1
    print "5 grams : ", len(d)
    return d

ngram = load_ngram()

def check_plagiarism(lines,ngram):
    def check_p(line):
        d = set()
        ll = line.split()
        for i in xrange(4,len(ll)):
            phrase = " ".join(ll[i-4:i+1])
            if phrase in ngram:
                d.add(phrase)
        return d
    d = set()
    for line in lines:
        d = d.union(check_p(line))
    return d

################# Status ################# 

class StatusMap:
    # 0 -> 1 -> 2 -> 3 -> 0
    # Ready -> Generating FSA -> Waiting in Queue -> Decoding by RNN -> Ready

    def __init__(self):
        self.s = {}
        self.messages = [
            "Ready", "Generating Rhyme Words/FSA", "Waiting in Queue", "Decoding by RNN"]

    def get_status(self, index):
        if not index in self.s:
            return self.messages[0]
        else:
            print index, self.s[index]
            return self.messages[self.s[index]]

    def next_status(self, index):
        if not index in self.s:
            self.s[index] = 1
        else:
            if self.s[index] == 3:
                del self.s[index]
            else:
                self.s[index] += 1

    def set_status(self, index, i):
        self.s[index] = i

    def clear_status(self, index):
        if index in self.s:
            del self.s[index]

sm = StatusMap()

################# Util Functions ################# 

def receive_all(conn):
    data = ""
    while True:
        d = conn.recv(size)
        if not d:
            break
        data += d
    return data


def post_process(lines,interactive=False):
    r = random.randint(1, 100000)
    before_path = before_path_tp + ".{}".format(r)
    after_path = after_path_tp + ".{}".format(r)

    f = open(before_path, 'w')
    nline = 0
    for line in lines:
        f.write(line.strip() + "\n")
        nline += 1
    f.close()
    
    print len(lines)
    nline = nline - 1
    if nline != 2 and nline != 4 and nline != 14:
        nline = 14
    cmd = "bash post_process.sh {} {} {}".format(before_path, after_path, nline)
    print cmd
    sp.call(cmd.split(), cwd=marjan_dir)

    f = open(after_path)
    r = ""
    iline = 0
    for line in f:
        r += line
        iline += 1
        if iline % 4 == 0:
            if not interactive:
                r += "\n"
    f.close()
    #os.remove(before_path)
    #os.remove(after_path)
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
    poem_str = poem_str.replace("\n", "<br//>")

    return poem_str,lines


def process_results(data):
    # there is no html tags in poems
    ll = data.split("\n")
    poems = []
    times = []
    for line in ll:
        if line.startswith("<START>"):
            poems.append(process_poem(line))

        if line.startswith("expand :") or line.startswith("forward_target :") or line.startswith("total :"):
            print sys.stderr.write(line + "\n")
            times.append(line)

    return poems, times


def process_poem_interactive(poem, line_reverse=1):
    lines = []
    if line_reverse == 1:
        ll = poem.split()[1:-1][::-1]

        newline = "\n"
        newll = []
        for w in ll:
            if w in ['?', '!', '.', ',']:
                w += newline
            newll.append(w)

        lines = ' '.join(newll).split(newline)[::-1]
        temp_lines = []
        for x in lines:
            if x != "":
                temp_lines.append(x)
        lines = temp_lines
        lines = [x.strip() for x in lines]
    else:
        ll = poem.split()[1:-1]
        newline = "\n"
        newll = []
        for w in ll:
            if w in ['?', '!', '.', ',']:
                w += newline
            newll.append(w)

        lines = ' '.join(newll).split(newline)
        temp_lines = []
        for x in lines:
            if x != "":
                temp_lines.append(x)
        lines = temp_lines
        lines = [x.strip() for x in lines]

    poem_str = post_process(lines,True)
    return poem_str.split('\n')


def process_results_interactive(data, line_reverse=1):
    ll = data.split("\n")
    poems = []
    times = []
    for line in ll:
        if line.startswith("<START>"):
            poems.append(process_poem_interactive(line, line_reverse))
        if line.startswith("expand :") or line.startswith("forward_target :") or line.startswith("total :"):
            print sys.stderr.write(line + "\n")
            times.append(line)

    return poems, times


def read_from_stdin():
    while True:
        line = sys.stdin.readline()
        # <model-type> <k-best> <topic_phrase_or_word>
        ll = line.split()
        model_type = int(ll[0])
        k = int(ll[1])
        topic = ll[2]
        poems, times = get_poem(k, model_type, topic)
        for poem in poems:
            print poem
        for t in times:
            print t


def tokenize(words):
    words = words.strip()
    if words == "":
        return [""]
    words = word_tokenize(words)
    words = [x.lower() for x in words]
    return words

def to_table_html_2(tables):
    html = "<table class=\"table table-bordered\">"
    titles = ["Rhyme Type", "Candidates"]
    html += "<thead><tr>{}</tr></thead>".format(
        " ".join(["<th>{}</th>".format(x) for x in titles]))

    html += "<tbody>"
    for line in tables:
        temp_ll = line.split()
        ll = [temp_ll[0][:-1], " ".join(temp_ll[1:])]
        html += "<tr>{}</tr>".format(" ".join(["<td>{}</td>".format(x)
                                     for x in ll]))

    html += "</tbody>"
    html += "</table>"
    return html

def to_table_html(tables):
    html = "<table class=\"table table-bordered\">"
    titles = ["Word/phrase"]
    html += "<thead><tr>{}</tr></thead>".format(
        " ".join(["<th>{}</th>".format(x) for x in titles]))

    html += "<tbody>"
    for line in tables:
        ll = line.split()
        html += "<tr>{}</tr>".format(" ".join(["<td>{}</td>".format(x)
                                     for x in ll]))

    html += "</tbody>"
    html += "</table>"
    return html


def get_rhyme(fn):
    f = open(fn)
    words = []
    exact_rhyme_candidate = []
    tables = []
    slant_rhymes = []

    while True:
        title = f.readline()
        if not title:
            break
        content = []
        while True:
            line = f.readline()
            if line.strip() == "":
                break
            content.append(line)

        if title.startswith("##Slant Rhyme Candidates"):
            for line in content:
                slant_rhymes.append(line.strip())
        
        
        if title.startswith('##Rhyme Words'):
            for line in content:
                words.append(line.strip())
        
        if title.startswith("##Exact Rhyme Candidates"):
            for line in content:
                exact_rhyme_candidate.append(line.strip())
        
        if title.startswith("##Rhyme info"):
            for line in content:
                tables.append(line.strip())
        
    rhyme_table_html = to_table_html_2(exact_rhyme_candidate)
    table_html = to_table_html(tables)
    return words, (table_html,rhyme_table_html,slant_rhymes)

def strip_accents(string):
    return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode('utf8')


def process_topic(topic):
    topic = topic.lower()
    for i in xrange(len(topic)):
        if not topic[i] == "_":
            if not topic[i].isalpha():
                tmp = topic[i]
                topic = topic.replace(tmp,"_")
    topic = u'{}'.format(u" ".join(topic.split(u"_")))
    topic = strip_accents(topic)
    return topic


def get_poem(k, model_type, topic, index=0, check=False, nline = None, no_fsa=False, style = None, withRhymeTable=True):
    # return times, poems, rhyme_words, rhyme_info_html.

    r = random.randint(1, 100000)
    if index!=0:
        r = index

    def rf(path):
        return '{}.{}'.format(path, r)

    fsa_path = rf(fsa_path_tp)
    source_path = rf(source_path_tp)
    rhyme_path = rf(rhyme_path_tp)
    encourage_path = rf(encourage_path_tp)

    topic = process_topic(topic)

    if model_type == -1:  # Rhyme words only
        cmd = ["bash", "run_rhyme.sh", topic, rhyme_path]
        print cmd
        sys.stderr.write("generating rhyme!\n")

        sm.next_status(index)

        print cmd
        sp.call(cmd, cwd=marjan_dir)

        rhyme_words, table_html = get_rhyme(rhyme_path)

        sm.clear_status(index)
        os.remove(rhyme_path)

        return [], [], rhyme_words, table_html, rhyme_table_html
    
    if not no_fsa:
        cmd = ["bash", "run.sh", topic, fsa_path, source_path, rhyme_path, encourage_path]
        if nline != None:
            if withRhymeTable:
                cmd = ["bash", "run-different-line-numbers.sh", topic, fsa_path, source_path, rhyme_path, encourage_path, str(nline)]
            else:
                cmd = ["bash", "run-different-line-numbers.sh", topic, fsa_path, source_path, encourage_path, str(nline)]
        print cmd
        sys.stderr.write("generating fsa!\n")
        sm.next_status(index)

        sp.call(cmd, cwd=marjan_dir)

        sys.stderr.write("fsa generated! start decoding!\n")
    else:
        sm.next_status(index)

    sm.next_status(index)

    port = ports[model_type]
    data = ""


    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if model_type <= 2:  # translation
        message = "k:{} source_file:{} fsa_file:{}".format(k,source_path,fsa_path)
        #s.send("{} {} {} {} {}\n".format(k, source_path, fsa_path, encourage_path, 1.0))
        
        encourage_files = [encourage_path]
        encourage_weights = [1.0]
        args = style
        if args != None:
            print "Here"
            
            if "topical" in args and args['topical']:
                topical = float(args['topical'])
                encourage_weights[0] = topical

            if "encourage_words" in args:
                encourage_words = args['encourage_words'].lower().split()
                if len(encourage_words) > 0:
                    user_encourage_path = rf(encourage_path_tp+".user")
                    f =  open(user_encourage_path,'w')
                    for word in encourage_words:
                        f.write(word+"\n")
                    f.flush()
                    f.close()
                    encourage_files.append(user_encourage_path)
                    encourage_weights.append(float(args['enc_weight']))
                    
            if "disencourage_words" in args:
                disencourage_words = args['disencourage_words'].lower().split()
                if len(disencourage_words) > 0:
                    user_disencourage_path = rf(encourage_path_tp+".dis.user")
                    f =  open(user_disencourage_path,'w')
                    for word in disencourage_words:
                        f.write(word+"\n")
                    f.flush()
                    f.close()
                    encourage_files.append(user_disencourage_path)
                    encourage_weights.append(-float(args['enc_weight']))
                
            if "cword" in args and args["cword"]:
                cword = float(args['cword'])
                encourage_files.append(curse_path)
                encourage_weights.append(cword)
            
            print args
            if "mono" in args and args["mono"]:
                mono_weight = float(args['mono'])
                if mono_weight != 0.0:
                    encourage_weights.append(mono_weight)
                    encourage_files.append(mono_path)

            if "sentiment" in args and args["sentiment"]:
                sentiment_weight = float(args["sentiment"])
                if sentiment_weight != 0.0:
                    encourage_weights.append(sentiment_weight)
                    encourage_files.append(sentiment_path)
            
            if "concrete" in args and args["concrete"]:
                concrete_weight = float(args["concrete"])
                if concrete_weight != 0.0:
                    encourage_weights.append(concrete_weight)
                    encourage_files.append(concrete_path)
                
            message += " encourage_list_files:{} encourage_weights:{}".format(",".join(encourage_files), ",".join([str(x) for x in encourage_weights]))
                
            if "reps" in args and args["reps"]:
                reps = float(args['reps'])
                message += " repetition:{}".format(reps)
            if "allit" in args and args["allit"]:
                allit = float(args['allit'])
                message += " alliteration:{}".format(allit)
                # not support now .. 
            if "wordlen" in args and args["wordlen"]:
                wordlen = float(args['wordlen'])
                message += " wordlen:{}".format(wordlen)

        s.connect((host, port))
        message_old = s.recv(1024)
        print host, port, message_old
        assert(message_old == 'Accept')
        sm.next_status(index)

        sys.stderr.write(message+'\n')
        s.send(message+"\n")
        data = receive_all(s)
    else:
        s.connect((host, port))
        message = s.recv(1024)
        print host, port, message
        assert(message == 'Accept')
        sm.next_status(index)
        s.send("{} {}\n".format(k, fsa_path))
        data = receive_all(s)

    s.close()

    poems, times = process_results(data)
    if withRhymeTable:
        rhyme_words, table_html = get_rhyme(rhyme_path)
    else:
        rhyme_words, table_html = "",["","",""]
    sm.next_status(index)

    #os.remove(fsa_path)
    #os.remove(source_path)
    #os.remove(rhyme_path)

    new_poems = []
    lines = []
    for p,l in poems:
        new_poems.append(p)
        lines.append(l)

    if check:
        return times, new_poems, rhyme_words, table_html, lines
    else:
        return times, new_poems, rhyme_words, table_html


def log_it(beamsize,topic,poems,times, weights = None):
    # log in google datastore
    date = datetime.now()
    date_str = date.isoformat()
    poem_str = "\n".join([x.replace("<br//>", '\n') for x in poems])
    time_dict = {}
    for t in times:
        if t.startswith("expand :"):
            t = float(t[8:-4])
            time_dict['expand'] = t
        elif t.startswith("forward_target :"):
            t = float(t[16:-4])
            time_dict['forward_target'] = t
        elif t.startswith("total :"):
            t = float(t[7:-4])
            time_dict['total'] = t
    poem_id, n_poem, n_poem_alexa = my_gcstore.log_poem(topic, date, poem_str, beamsize, time_dict, weights)

    return poem_id, n_poem, n_poem_alexa

def get_perm(path):
    return stat.S_IMODE(os.lstat(path).st_mode)


def mymkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        os.chmod(path, get_perm(path) | stat.S_IWOTH | stat.S_IWGRP)



################# API ################# 

app = Flask(__name__)
api = Api(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


class Status(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        index = 'default'
        if "id" in args:
            index = args['id']

        return make_response(sm.get_status(index))

################### Interactive ####################

class Rhyme(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('topic')
        parser.add_argument('id')
        parser.add_argument('nline')
        parser.add_argument('source')


        args = parser.parse_args()
        topic = args['topic']
        source = args['source']
        index = 'default'
        nline = None
        if "id" in args:
            index = args['id']
        if "nline" in args:
            nline = int(args['nline'])

        times, poems, rhyme_words, table_html = get_rhyme_interactive(
            topic, index, nline = nline)

        date = datetime.now()
        rhyme_id = my_gcstore.log_rhyme(topic, date, " ".join(rhyme_words), source = source)

        d = {}
        d['rhyme_words'] = rhyme_words
        d['rhyme_info'] = table_html
        d['rhyme_id'] = rhyme_id

        json_str = json.dumps(d, ensure_ascii=False)
        r = make_response(json_str)
        sm.clear_status(index)

        return r


class Confirm(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('words')
        parser.add_argument('id')

        args = parser.parse_args()
        words_json = args['words']
        index = 'default'
        if "id" in args:
            index = args['id']

        r = make_response("Got It")
        sm.clear_status(index)

        return r

def get_rhyme_auto(topic, index=0, line_reverse=1, nline = None):

    r = random.randint(1, 100000)
    if index!=0:
        r = index

    def rf(path):
        return '{}.{}'.format(path, r)

    fsa_path = rf(fsa_path_tp)
    source_path = rf(source_path_tp)
    rhyme_path = rf(rhyme_path_tp)
    encourage_path = rf(encourage_path_tp)

    topic = process_topic(topic)
    
    cmd = ["bash", "run-different-line-numbers.sh", topic, fsa_path, source_path, rhyme_path, encourage_path, str(nline)]

    print cmd

    sp.call(cmd, cwd=marjan_dir)

    rhyme_words, table_html = get_rhyme(rhyme_path)

    sm.clear_status(index)

    return [], [], rhyme_words, table_html






def get_rhyme_interactive(topic, index, line_reverse=1, nline = None):
    print "In get_rhyme_interactive"

    def rf(path, r):
        return '{}.{}'.format(path, r)

    interactive_folder = rf(interactive_folder_tp, index)
    mymkdir(interactive_folder)
    source_path = os.path.join(interactive_folder, "source.txt")
    rhyme_path = os.path.join(interactive_folder, "rhyme.txt")
    encourage_path = os.path.join(interactive_folder, "topical.txt")

    topic = process_topic(topic)

    #cmd = ["bash", "run-interactive.sh", topic,
    #       str(line_reverse), interactive_folder, source_path, rhyme_path]
    
    if nline == 14 or nline == 4 or nline == 2:
        cmd = ["bash", "run-interactive-different-line-numbers.sh", topic, interactive_folder, source_path, rhyme_path, encourage_path, str(nline)]

    sys.stderr.write("generating rhyme!\n")

    sm.next_status(index)

    sys.stderr.write("CMD: {}\n".format(" ".join(cmd)))
    sp.call(cmd, cwd=marjan_dir)

    rhyme_words, table_html = get_rhyme(rhyme_path)

    sm.clear_status(index)

    return [], [], rhyme_words, table_html


def send_receive(host, port, ins):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    message = s.recv(1024)
    print host, port, message
    assert(message == 'Accept')
    s.send(ins)
    data = receive_all(s)
    s.close()
    return data


def get_poem_interactive(model_type, action, index, iline, words=[],encourage_path = None, encourage_weight = None,  line_reverse=1, args = None):
    # return times, poems, rhyme_words, rhyme_info_html.
    def rf(path, r):
        return '{}.{}'.format(path, r)

    interactive_folder = rf(interactive_folder_tp, index)
    mymkdir(interactive_folder)
    source_path = os.path.join(interactive_folder, "source.txt")
    rhyme_path = os.path.join(interactive_folder, "rhyme.txt")
    topical_path = os.path.join(interactive_folder, "topical.txt")

    port = interactive_ports[model_type]
    data = ""

    if iline == 1:  # the first line
        ins = "source {}\n".format(source_path)
        print ins
        data = send_receive(host, port, ins)

    sm.set_status(index, 3)

    ins = "default"
    if action == "fsa":
        fsa_path = os.path.join(
            interactive_folder, "fsa_start-{}".format(iline - 1))
        ins = "fsa {}\n".format(fsa_path)
    elif action == "fsaline":
        fsa_path = os.path.join(interactive_folder, "fsa_line{}".format(iline - 1))

        encourage_files = []
        encourage_weights = []

        if encourage_path != None:
            encourage_files.append(encourage_path)
            encourage_weights.append(encourage_weight)


        if args != None:
            
            if "topical" in args and args['topical']:
                topical = float(args['topical'])
                encourage_weights.append(topical)
                encourage_files.append(topical_path)
                
            if "cword" in args and args["cword"]:
                cword = float(args['cword'])
                encourage_files.append(curse_path)
                encourage_weights.append(cword)
            
            if "mono" in args and args["mono"]:
                mono_weight = float(args['mono'])
                if mono_weight != 0.0:
                    encourage_weights.append(mono_weight)
                    encourage_files.append(mono_path)

            if "sentiment" in args and args["sentiment"]:
                sentiment_weight = float(args["sentiment"])
                if sentiment_weight != 0.0:
                    encourage_weights.append(sentiment_weight)
                    encourage_files.append(sentiment_path)
            
            if "concrete" in args and args["concrete"]:
                concrete_weight = float(args["concrete"])
                if concrete_weight != 0.0:
                    encourage_weights.append(concrete_weight)
                    encourage_files.append(concrete_path)
            
            message = "encourage_list_files:{} encourage_weights:{}".format(",".join(encourage_files), ",".join([str(x) for x in encourage_weights]))

            if "reps" in args and args["reps"]:
                reps = float(args['reps'])
                message += " repetition:{}".format(reps)
            if "allit" in args and args["allit"]:
                allit = float(args['allit'])
                message += " alliteration:{}".format(allit)
                # not support now .. 
            if "wordlen" in args and args["wordlen"]:
                wordlen = float(args['wordlen'])
                message += " wordlen:{}".format(wordlen)

            
        ins = "fsaline {} {}\n".format(fsa_path,message)

    elif action == "words":
        words_str = " ".join(words)
        ins = "words {}\n".format(words_str)

    print ins
    data = send_receive(host, port, ins)

    poems, times = process_results_interactive(data, line_reverse)
    rhyme_words, table_html = get_rhyme(rhyme_path)
    sm.clear_status(index)

    return times, poems, rhyme_words, table_html


class POEMI(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('model')
        parser.add_argument('action')
        parser.add_argument('line')
        parser.add_argument('words')
        parser.add_argument('discourage_words')
        parser.add_argument('discourage_weight')
        parser.add_argument('id')
        #style
        parser.add_argument('cword')
        parser.add_argument('reps')
        parser.add_argument('allit')
        parser.add_argument('wordlen')        
        parser.add_argument('topical')
        parser.add_argument('mono')
        parser.add_argument('sentiment')
        parser.add_argument('concrete')


        args = parser.parse_args()

        model_type = int(args['model'])

        action = args['action']
        assert(action == "feed_history" or action == "words" or action == "fsa" or action == "fsaline")

        index = 'default'
        if "id" in args:
            index = args['id']

        iline = int(args['line'])
        assert(iline <= 14 and iline >= 1)

        line_reverse = 1
        
        poems, rhyme_words, table_html = [""],[""],""

        if action == 'feed_history':
            words_list = json.loads(args['words'])
            for i, words in enumerate(words_list):
                words = tokenize(words)
                if line_reverse == 1:
                    words = words[::-1]

                if len(words) == 1 and words[0] == "":
                    words = ["<UNK>"]
                
                print "poem_interactive", model_type, action, i+1, words, index

                sub_action = "words"
                _, poems, rhyme_words, table_html = get_poem_interactive(model_type, sub_action, index, i+1, words, args = args)

        else:
            words = args['words']
            words = tokenize(words)

            discourage_path = None
            discourage_weight = 0.0
            if 'discourage_words' in args and args['discourage_words']:
                discourage_words = args['discourage_words']
                discourage_words = tokenize(discourage_words)
                
                if len(discourage_words) == 1 and discourage_words[0] == '':
                    pass
                else:
                    interactive_folder = "{}.{}".format(interactive_folder_tp, index)
                    discourage_path = os.path.join(interactive_folder,'line_enc.txt')
                    f = open(discourage_path,'w')
                    for word in discourage_words:
                        f.write(word+"\n")
                    f.flush()
                    f.close()

            if 'discourage_weight' in args:
                discourage_weight = args['discourage_weight']

            if line_reverse == 1:
                words = words[::-1]

            if action == 'words' and len(words) == 1 and words[0] == "":
                words = ["<UNK>"]

            print "poem_interactive", model_type, action, iline, words, index
            _, poems, rhyme_words, table_html = get_poem_interactive(
                model_type, action, index, iline, words, encourage_path = discourage_path, encourage_weight = discourage_weight, args = args)

        rhyme_words_html = "<br//>".join(rhyme_words)

        config_str = ""

        f = open(os.path.join(root_dir, 'models/config.txt'))
        for line in f:
            config_str += line.strip() + "<br//>"
        f.close()

        if len(poems) > 0:
            poems = poems[0]

        d = {}
        d['poem'] = poems
        d['config'] = config_str
        d['rhyme_words'] = rhyme_words_html
        d['rhyme_info'] = table_html
        json_str = json.dumps(d, ensure_ascii=False)
        r = make_response(json_str)

        return r

class LogI(Resource): # log the interactive steps
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rhyme_id')
        parser.add_argument('poems')
        parser.add_argument('discourage_words')
        parser.add_argument('hme_flags')
        parser.add_argument('topic')
        parser.add_argument('nline')
        parser.add_argument('source')
        

        args = parser.parse_args()

        def convert_to_utf8(ss):
            new_ss = []
            for s in ss:
                new_ss.append(s.decode("utf8"))
            return new_ss

        topic = args['topic']
        nline = int(args['nline'])
        rhyme_id = int(args['rhyme_id'])
        poems = args['poems']
        discourage_words = args['discourage_words']
        hme_flags = args['hme_flags']
        source = args['source']
        date = datetime.now()

        my_gcstore.log_poem_interactive(topic, nline, rhyme_id, poems, discourage_words, hme_flags,date, source = source)
        
        r = make_response("Thanks")
        return r


################### Auto mode ####################
class Feedback(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('poem_id')
        parser.add_argument('score')
        
        args = parser.parse_args()
        print args

        poem_id = int(args['poem_id'])
        score = float(args['score'])
        my_gcstore.set_score(poem_id, score)
        
        r = make_response("Thanks")
        return r

class Feedback_rhyme(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rhyme_id')
        parser.add_argument('score')
        
        args = parser.parse_args()
        print args

        rhyme_id = int(args['rhyme_id'])
        score = float(args['score'])
        my_gcstore.set_score_key(rhyme_id, score,'rhyme')
        
        r = make_response("Thanks")
        return r

        
class NPOEM(Resource):
    def get(self):
        #n = my_gcstore.get_npoem()
        #n_alexa = my_gcstore.get_npoem_key("alexa")
        n = 0
        n_alexa = 0
        d = {}
        d['value'] = n
        d['value_alexa'] = n_alexa
        print "npoem/n_poem_alexa", n, n_alexa
        json_str = json.dumps(d, ensure_ascii=False)
        r = make_response(json_str)
        return r

class Rhyme_Auto(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('topic')
        parser.add_argument('id')
        parser.add_argument('nline')

        args = parser.parse_args()
        topic = args['topic']
        index = 'default'
        nline = None
        if "id" in args:
            index = args['id']
        if "nline" in args:
            nline = int(args['nline'])

        times, poems, rhyme_words, table_html = get_rhyme_auto(
            topic, index, nline = nline)

        rhyme_words_html = "<br//>".join(rhyme_words)

        date = datetime.now()
        rhyme_id = my_gcstore.log_rhyme(topic, date, " ".join(rhyme_words), source = 'rhyme')


        d = {}
        d['rhyme_words'] = rhyme_words_html
        d['rhyme_info'] = table_html[1]
        d['rhyme_id'] = rhyme_id

        json_str = json.dumps(d, ensure_ascii=False)
        r = make_response(json_str)
        sm.clear_status(index)

        return r




class POEM_check(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('k')
        parser.add_argument('model')
        parser.add_argument('topic')
        parser.add_argument('nline')
        parser.add_argument('id')
        # style
        parser.add_argument("encourage_words")
        parser.add_argument("disencourage_words")
        parser.add_argument("enc_weight")
        parser.add_argument('cword')
        parser.add_argument('reps')
        parser.add_argument('allit')
        parser.add_argument('wordlen')
        
        parser.add_argument('topical')
        parser.add_argument('mono')
        parser.add_argument('sentiment')
        parser.add_argument('concrete')
        # no_fsa for adjust style
        parser.add_argument('no_fsa')
        
        parser.add_argument("is_default")
        parser.add_argument("source")

        args = parser.parse_args()
        print args

        # parse the tags
        k = int(args['k'])
        model_type = int(args['model'])
        topic = args['topic']
        index = 'default'
        if "id" in args:
            index = args['id']

        nline = 14
        if "id" in args:
            index = args['id']
        if "nline" in args:
            nline = int(args['nline'])        
        if not (nline == 2 or nline == 4 or nline == 14):
            nline = 14

        # no_fsa
        no_fsa = False
        if "no_fsa" in args and args['no_fsa'] == "1":
            no_fsa = True
        

        assert(k > 0)
        assert(model_type == 0 or model_type == -1)
        assert(len(topic) > 0)

        print model_type, k, topic.encode('utf8')
        times, poems, rhyme_words, table_html,lines = get_poem(
            k, model_type, topic, index, check=True, nline = nline, no_fsa = no_fsa, style = args)
        
        
        # log it
        if model_type >= 0:
            poem_id, n_poem, n_poem_alexa = random.randint(0,100000), 0, 0
            #poem_id, n_poem, n_poem_alexa = log_it(beams[model_type],topic,poems,times,weights = args)
            print poem_id, n_poem, n_poem_alexa

        phrases = []
        if len(lines) > 0:
            phrases = list(check_plagiarism(lines[0],ngram))
        phrase_str = "<br//>".join(phrases)

        poem_str = "<br//><br//>".join(poems)

        rhyme_words_html = "<br//>".join(rhyme_words)

        config_str = ""

        f = open(os.path.join(root_dir, 'models/config.txt'))
        for line in f:
            config_str += line.strip() + "<br//>"
        f.close()

        d = {}
        d['poem'] = poem_str
        d['config'] = config_str
        d['rhyme_words'] = rhyme_words_html
        d['rhyme_info'] = table_html[0]
        d['exact_rhyme_candidates'] = table_html[1]
        d['slant_rhyme_candidates'] = "<br//>".join(table_html[2])
        d['pc'] = phrase_str
        d['poem_id'] = poem_id
        d['n_poem'] = n_poem
        d['n_poem_alexa'] = n_poem_alexa
        json_str = json.dumps(d, ensure_ascii=False)
        r = make_response(json_str)

        return r

################### Add Endpoint ####################
api.add_resource(POEM_check, '/api/poem_check')
api.add_resource(NPOEM, '/api/npoem')
#api.add_resource(Feedback, '/api/feedback')
#api.add_resource(Feedback_rhyme, '/api/feedback_rhyme')
#api.add_resource(Rhyme_Auto, "/api/rhyme_auto")

# for interactive model
#api.add_resource(Rhyme, "/api/rhyme")
#api.add_resource(Confirm, "/api/confirm")
api.add_resource(Status, '/api/poem_status')
#api.add_resource(POEMI, '/api/poem_interactive')
#api.add_resource(LogI, '/api/log_interactive')





if __name__ == '__main__':
    # read_from_stdin()
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(threaded=True, debug=True, host='0.0.0.0', port=8080)
