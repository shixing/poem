import sys
import requests
import random
url = "http://vivaldi.isi.edu:8080/api/poem_check"
data = {}
data['topic'] = 'love'
data['k'] = '1'
data['model'] = '0'
data['id'] = '123'
data['nline'] = '4'
data['encourage_words'] = ''
data['disencourage_words'] = ''
data['enc_weight'] = '5'
data['cword'] = '-5'
data['reps'] = '0'
data['allit'] = '0'
data['wordlen'] = '0'
data['topical'] = '1.0'
data['mono'] = '-5'
data['sentiment'] = '0'
data['concrete'] = '0'
data['no_fsa'] = '0'
data['is_default'] = '1'
data['source'] = "other"

new_data = dict(data)
new_data['no_fsa'] = '1'
new_data['topical'] = '1.71'
new_data['concrete'] = '-2.82'
new_data['sentiment'] = '5'
new_data['reps'] = '-2.84'
data['is_default'] = '0'

def process_poem(poem):
    poem = poem.replace("<br//>",'\n')
    poem = poem[:-3]
    return poem

def generate_pair(topic):
    data['topic'] = topic
    new_data['topic'] = topic
    r1 = requests.get(url, params=data)
    r2 = requests.get(url, params=new_data)
    r1 = r1.json()
    r2 = r2.json()
    
    p1 = process_poem(r1['poem'])
    p2 = process_poem(r2['poem'])
    return p1,p2

def main():
    fn = sys.argv[1]
    f = open(fn)
    topics = []
    for line in f:
        topics.append(line.strip())
    f.close()
    topics = random.sample(topics,50)
    f = open(sys.argv[2],'w')
    for i,topic in enumerate(topics):
        p1,p2 = generate_pair(topic)
        print i, topic
        f.write(topic + "\n")
        f.write("\n")
        f.write(p1 + "\n")
        f.write("\n")
        f.write(p2 + "\n")
        f.write("\n")
    f.close()

main()
    



