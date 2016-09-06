import sys
import socket
import os
import subprocess as sp
import json

from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource
from flask import request, make_response
from datetime import datetime
from nltk import word_tokenize
import random
host = "holst.isi.edu"
ports = [10030]
size = 10240

root_dir = os.path.abspath(__file__ + "/../../")
fsa_path_tp = os.path.join(root_dir, "fsas/poem.fsa")
source_path_tp = os.path.join(root_dir, "fsas/source.txt")
rhyme_path_tp = os.path.join(root_dir, "fsas/rhyme.txt")
encourage_path_tp = os.path.join(root_dir, "fsas/encourage.txt")
marjan_dir = os.path.join(root_dir, "sp-topic/")
before_path_tp = os.path.join(root_dir, "fsas/before.txt")
after_path_tp = os.path.join(root_dir, "fsas/after.txt")
ngram_path = os.path.join(root_dir,"models/5grams_es.txt")

interactive_folder_tp = os.path.join(root_dir, 'fsas_interactive/data')
interactive_folder = interactive_folder_tp

beams = [50]
interactive_beams = [50]
line_reverses = [1]
interactive_ports = [10030]

def load_ngram():
    d = {}
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
    for line in lines:
        f.write(line.strip() + "\n")
    f.close()
    
    cmd = "bash post_process.sh {} {}".format(before_path, after_path)
    sp.call(cmd.split(), cwd=marjan_dir)

    f = open(after_path)
    r = ""
    iline = 0
    for line in f:
        r += line
        iline += 1
        if iline == 4 or iline == 8 or iline == 11:
            if not interactive:
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
        if line.startswith("Total:") or line.startswith("Forward:") or line.startswith("Expand:"):
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
        if line.startswith("Total:") or line.startswith("Forward:") or line.startswith("Expand:"):
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


def to_table_html(tables):
    html = "<table class=\"table table-bordered\">"
    titles = ["Word/phrase",
              "LM", "Chosen for rhyme", "Weight"]
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
    # [TODO]

    f = open(fn)
    words = []
    tables = []

    for i in xrange(14):
        line = f.readline()
        words.append(line.strip())
    f.readline()
    f.readline()
    f.readline()
    while True:
        line = f.readline()
        if not line:
            break
        tables.append(line.strip())

    table_html = to_table_html(tables)
    return words, table_html


def process_topic(topic):
    # [TODO]
    if type(topic) == str:
        topic = topic.decode("utf8")
    
    topic = topic.lower()

    topic = u'{}'.format(u" ".join(topic.split(u"_")))
    return topic.encode('utf8')


def get_poem_compare(topic, c1, c2, index=0):
    # return times, poems, rhyme_words, rhyme_info_html.

    r = random.randint(1, 100000)

    def rf(path):
        return '{}.{}'.format(path, r)

    fsa_path = rf(fsa_path_tp)
    source_path = rf(source_path_tp)
    rhyme_path = rf(rhyme_path_tp)

    cmd = ["bash", "run.sh", topic, fsa_path, source_path, rhyme_path]
    print cmd
    sys.stderr.write("generating fsa!\n")
    sm.next_status(index)

    sp.call(cmd, cwd=marjan_dir)

    sys.stderr.write("fsa generated! start decoding!\n")

    def _t_(model_type):

        sm.set_status(index, 2)
        port = ports[model_type]
        data = ""

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((host, port))
        message = s.recv(1024)
        print host, port, message
        assert(message == 'Accept')
        sm.set_status(index, 3)
        k = 1
        s.send("{} {} {}\n".format(k, source_path, fsa_path))
        data = receive_all(s)

        s.close()

        poems, times = process_results(data)
        rhyme_words, table_html = get_rhyme(rhyme_path)
        return times, poems, rhyme_words, table_html

    r1 = _t_(c1['model'])
    r2 = _t_(c2['model'])

    os.remove(fsa_path)
    os.remove(source_path)
    os.remove(rhyme_path)
    sm.next_status(index)

    return r1, r2


def get_poem(k, model_type, topic, index=0, check=False):
    # return times, poems, rhyme_words, rhyme_info_html.

    r = random.randint(1, 100000)

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

        return [], [], rhyme_words, table_html

    cmd = ["bash", "run.sh", topic, fsa_path, source_path, rhyme_path, encourage_path]
    print cmd
    sys.stderr.write("generating fsa!\n")
    sm.next_status(index)

    sp.call(cmd, cwd=marjan_dir)

    sys.stderr.write("fsa generated! start decoding!\n")
    sm.next_status(index)

    port = ports[model_type]
    data = ""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if model_type <= 2:  # translation
        s.connect((host, port))
        message = s.recv(1024)
        print host, port, message
        assert(message == 'Accept')
        sm.next_status(index)
        s.send("{} {} {} {} {}\n".format(k, source_path, fsa_path, encourage_path, 1.0))
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
    rhyme_words, table_html = get_rhyme(rhyme_path)
    sm.next_status(index)

    os.remove(fsa_path)
    os.remove(source_path)
    os.remove(rhyme_path)

    new_poems = []
    lines = []
    for p,l in poems:
        new_poems.append(p)
        lines.append(l)

    if check:
        return times, new_poems, rhyme_words, table_html, lines
    else:
        return times, new_poems, rhyme_words, table_html

def log_it(beamsize,topic,poems,times):
    flog = open(os.path.join(root_dir, 'py/log_es.txt'), 'a')
    flog.write("Time: " + datetime.now().isoformat() + "\n")
    if type(topic) == unicode:
        topic = topic.encode("utf8")
    flog.write("Beam_size: {}\nTopic: {}\n".format(beamsize, topic))
    flog.write('\n'.join(times) + "\n")
    flog.write("----------------------\n")
    for x in poems:
        if type(x) is str:
            x = x.decode('utf8')
        x = x.replace("<br//>", '\n')
        flog.write(x.encode('utf8') + "\n")
    flog.write('\n')
    flog.close()

## app and api

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

# need to reserve, daniel is using this one
class POEM(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('k')
        parser.add_argument('model')
        parser.add_argument('topic')
        parser.add_argument('id')

        args = parser.parse_args()
        k = int(args['k'])
        model_type = int(args['model'])
        topic = args['topic']
        index = 'default'
        if "id" in args:
            index = args['id']

        assert(k > 0)
        assert(model_type == 0 or model_type ==
               1 or model_type == 2 or model_type == -1)
        assert(len(topic) > 0)

        print model_type, k, topic
        times, poems, rhyme_words, table_html = get_poem(
            k, model_type, topic, index)

        # log it
        if model_type >= 0:
            log_it(beams[model_type],topic,poems,times)

        poem_str = "<br//><br//>".join(poems)

        rhyme_words_html = "<br//>".join(rhyme_words)

        config_str = ""

        f = open(os.path.join(root_dir, 'py/config_es.txt'))
        for line in f:
            config_str += line.strip() + "<br//>"
        f.close()

        d = {}
        d['poem'] = poem_str
        d['config'] = config_str
        d['rhyme_words'] = rhyme_words_html
        d['rhyme_info'] = table_html
        json_str = json.dumps(d, ensure_ascii=False)
        r = make_response(json_str)

        return r


################### Interactive ####################

class Rhyme(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('topic')
        parser.add_argument('id')

        args = parser.parse_args()
        topic = args['topic']
        index = 'default'
        if "id" in args:
            index = args['id']

        times, poems, rhyme_words, table_html = get_rhyme_interactive(
            topic, index)
        d = {}
        d['rhyme_words'] = rhyme_words

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


def mymkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_rhyme_interactive(topic, index, line_reverse=1):
    def rf(path, r):
        return '{}.{}'.format(path, r)

    interactive_folder = rf(interactive_folder_tp, index)
    mymkdir(interactive_folder)
    source_path = os.path.join(interactive_folder, "source.txt")
    rhyme_path = os.path.join(interactive_folder, "rhyme.txt")

    topic = process_topic(topic)

    cmd = ["bash", "run-interactive.sh", topic,
           str(line_reverse), interactive_folder, source_path, rhyme_path]

    sys.stderr.write("generating rhyme!\n")

    sm.next_status(index)

    print cmd
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


def get_poem_interactive(model_type, action, index, iline, words=[], line_reverse=1):
    # return times, poems, rhyme_words, rhyme_info_html.
    def rf(path, r):
        return '{}.{}'.format(path, r)

    interactive_folder = rf(interactive_folder_tp, index)
    mymkdir(interactive_folder)
    source_path = os.path.join(interactive_folder, "source.txt")
    rhyme_path = os.path.join(interactive_folder, "rhyme.txt")

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
        fsa_path = os.path.join(interactive_folder, "fsa{}".format(iline - 1))
        ins = "fsaline {}\n".format(fsa_path)
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
        parser.add_argument('id')

        args = parser.parse_args()

        model_type = int(args['model'])

        action = args['action']
        assert(action == "words" or action == "fsa" or action == "fsaline")

        index = 'default'
        if "id" in args:
            index = args['id']

        iline = int(args['line'])
        assert(iline <= 14 and iline >= 1)

        words = args['words']
        words = tokenize(words)

        line_reverse = 1
        if line_reverse == 1:
            words = words[::-1]

        if action == "words" and len(words) == 1 and words[0] == "":
            words = ["<UNK>"]

        print "poem_interactive", model_type, action, iline, words, index
        times, poems, rhyme_words, table_html = get_poem_interactive(
            model_type, action, index, iline, words)

        rhyme_words_html = "<br//>".join(rhyme_words)

        config_str = ""

        f = open(os.path.join(root_dir, 'py/config_es.txt'))
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

def load_random_topic():
    topics = []
    f = open('random_topic_es.txt')
    for line in f:
        topics.append(line.strip())
    r = random.randint(0, len(topics) - 1)
    f.close()
    return process_topic(topics[r])


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w


def load_compare(fn):
    f = open(fn)
    line = f.readline()

    def get_config(line):
        c = [x.split("=") for x in line.split()]
        poem1 = {}
        for k, v in c:
            poem1[k] = int(v)
        return poem1
    c1 = get_config(line)
    line = f.readline()
    c2 = get_config(line)
    f.close()
    return (c1, c2)


def load_random_config():
    f = open(os.path.join(root_dir, 'compare/random_compare_es.txt'))
    choices = []
    for line in f:
        ll = line.split()
        choices.append((ll[0], float(ll[1])))
    config_file = weighted_choice(choices)
    config_path = os.path.join(root_dir, "compare/" + config_file)
    f.close()
    c1, c2 = load_compare(config_path)
    return c1, c2, config_file


class POEM_compare(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('topic')
        parser.add_argument('id')

        args = parser.parse_args()

        topic = args['topic']
        if topic == "-1":
            # choose from random topic
            topic = load_random_topic()

        index = 'default'
        if "id" in args:
            index = args['id']

        c1, c2, config_file = load_random_config()

        print "poem_compare", index, topic, c1, c2, config_file
        r1, r2 = get_poem_compare(topic, c1, c2, index)

        


        pome1 = ""
        poem2 = ""
        if len(r1[1]) > 0:
            poem1 = r1[1][0][0]
        if len(r2[1]) > 0:
            poem2 = r2[1][0][0]


        log_it(beams[c1['model']], topic, [poem1], r1[0])
        log_it(beams[c2['model']], topic, [poem2], r2[0])


        reverse = random.randint(0, 1)

        print reverse, poem1

        if reverse == 1:
            poem1, poem2 = poem2, poem1

        d = {}
        d['poem1'] = poem1
        d['poem2'] = poem2
        d['reverse'] = reverse
        d['config_file'] = config_file
        d['topic'] = topic
        json_str = json.dumps(d, ensure_ascii=False)
        r = make_response(json_str)

        return r


class POEM_submit(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('topic')
        parser.add_argument('result')
        parser.add_argument('poem1')
        parser.add_argument('poem2')
        parser.add_argument('config_file')

        args = parser.parse_args()
        d = args
        d['time'] = datetime.now().isoformat()
        json_str = json.dumps(d, ensure_ascii=False)
        json_str.replace('\n', "\\n")
        f = open(os.path.join(root_dir, 'py/compare_result_es.txt'), 'a')
        f.write(json_str + "\n")
        f.close()

        r = make_response("Done")

        return r

class POEM_check(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('k')
        parser.add_argument('model')
        parser.add_argument('topic')
        parser.add_argument('id')

        args = parser.parse_args()
        k = int(args['k'])
        model_type = int(args['model'])
        topic = args['topic']
        index = 'default'
        if "id" in args:
            index = args['id']

        assert(k > 0)
        assert(model_type == 0 or model_type ==
               1 or model_type == 2 or model_type == -1)
        assert(len(topic) > 0)

        print model_type, k, topic.encode('utf8')
        times, poems, rhyme_words, table_html,lines = get_poem(
            k, model_type, topic, index, check=True)
        
        
        # log it
        if model_type >= 0:
            log_it(beams[model_type],topic,poems,times)

        phrases = []
        if len(lines) > 0:
            phrases = list(check_plagiarism(lines[0],ngram))
        phrase_str = "<br//>".join(phrases)

        poem_str = "<br//><br//>".join(poems)

        rhyme_words_html = "<br//>".join(rhyme_words)

        config_str = ""

        f = open(os.path.join(root_dir, 'py/config_es.txt'))
        for line in f:
            config_str += line.strip() + "<br//>"
        f.close()

        d = {}
        d['poem'] = poem_str
        d['config'] = config_str
        d['rhyme_words'] = rhyme_words_html
        d['rhyme_info'] = table_html
        d['pc'] = phrase_str
        json_str = json.dumps(d, ensure_ascii=False)
        r = make_response(json_str)

        return r


# add endpoint
api.add_resource(POEM, '/api/poem')
api.add_resource(Rhyme, "/api/rhyme")
api.add_resource(Confirm, "/api/confirm")
api.add_resource(Status, '/api/poem_status')
api.add_resource(POEMI, '/api/poem_interactive')
api.add_resource(POEM_submit, '/api/poem_submit')
api.add_resource(POEM_compare, '/api/poem_compare')
api.add_resource(POEM_check, '/api/poem_check')

if __name__ == '__main__':
    # read_from_stdin()
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(threaded=True, debug=True, host='cage.isi.edu', port=8081)
