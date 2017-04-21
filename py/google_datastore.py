from google.cloud import datastore
import google.cloud.exceptions
import sys
import time 
from retrying import retry

class GCStore:
    def __init__(self):
        self.client = datastore.Client()
    
    @retry(wait_exponential_multiplier=100, wait_exponential_max=2000)
    def get_npoem(self):
        key = self.client.key("counter",'npoem')
        counter = self.client.get(key)
        if counter == None:
            key = self.client.key("counter",'npoem')
            counter = datastore.Entity(key = key)
            counter['value'] = 0
            self.client.put(counter)
        return counter['value']

    @retry(wait_exponential_multiplier=100, wait_exponential_max=2000)
    def get_npoem_key(self,counter_key):
        key = self.client.key("counter",counter_key)
        counter = self.client.get(key)
        if counter == None:
            key = self.client.key("counter",counter_key)
            counter = datastore.Entity(key = key)
            counter['value'] = 0
            self.client.put(counter)
        return counter['value']


    @retry(wait_exponential_multiplier=100, wait_exponential_max=2000)
    def increase_npoem(self):
        value = -1
        key = self.client.key("counter",'npoem')
        counter = self.client.get(key)
        if not "value" in counter:
            counter['value'] = 0
        counter['value'] += 1
        value = counter['value']
        self.client.put(counter)
        return value


    @retry(wait_exponential_multiplier=100, wait_exponential_max=2000)
    def increase_npoem_key(self,counter_key):
        value = -1
        key = self.client.key("counter",counter_key)
        counter = self.client.get(key)
        if not "value" in counter:
            counter['value'] = 0
        counter['value'] += 1
        value = counter['value']
        self.client.put(counter)
        return value


    @retry(wait_exponential_multiplier=100, wait_exponential_max=2000)
    def set_score(self,poem_id, score):
        with self.client.transaction():
            key = self.client.key("poem",poem_id)
            poem = self.client.get(key)
            poem['score'] = score
            self.client.put(poem)


    @retry(wait_exponential_multiplier=100, wait_exponential_max=2000)
    def set_score_key(self,poem_id, score,key):
        with self.client.transaction():
            key = self.client.key(key,poem_id)
            poem = self.client.get(key)
            poem['score'] = score
            self.client.put(poem)


        
    @retry(wait_exponential_multiplier=100, wait_exponential_max=2000)
    def log_poem(self, topic_str, date, poem_str, beam_size, time_dict, weights_dict = None):
        # return id
        npoem = self.increase_npoem()
        if "source" in weights_dict and weights_dict['source'] == "alexa":
            npoem_alexa = self.increase_npoem_key("alexa")
        else:
            npoem_alexa = self.get_npoem_key("alexa")

        with self.client.transaction():
            key = self.client.key("poem")
            poem = datastore.Entity(key=key)
            poem['topic'] = topic_str
            poem['created_at'] = date

            temp = datastore.Entity()
            temp.update(weights_dict)
            poem['style'] = temp

            poem['beam_size'] = beam_size
            poem['content'] = poem_str.decode("utf8")

            temp = datastore.Entity()
            temp.update(time_dict)
            poem['time'] = temp
            
            self.client.put(poem)

        return poem.key.id, npoem, npoem_alexa


    @retry(wait_exponential_multiplier=100, wait_exponential_max=2000)
    def log_rhyme(self, topic_str, date, rhyme_str, source = "interactive"):
        # return id

        with self.client.transaction():
            key = self.client.key("rhyme")
            rhyme = datastore.Entity(key=key)
            rhyme['topic'] = topic_str
            rhyme['created_at'] = date
            rhyme['rhyme'] = rhyme_str.decode("utf8")
            rhyme['source'] = source

            self.client.put(rhyme)

        return rhyme.key.id
        
    @retry(wait_exponential_multiplier=100, wait_exponential_max=2000)
    def log_poem_interactive(self, topic, nline, rhyme_id, poems, discourage_words, hme_flags, date, source = "interactive"):
        # poems json str of these things

        with self.client.transaction():
            key = self.client.key("interactive")
            poem = datastore.Entity(key=key)
            poem['topic'] = topic
            poem['created_at'] = date
            poem['rhyme_id'] = rhyme_id
            poem['poems'] = poems
            poem['discourage_words'] = discourage_words
            poem['hme_flags'] = hme_flags
            poem['nline'] = nline
            poem['source'] = source

            self.client.put(poem)

        return poem.key.id
        
        

