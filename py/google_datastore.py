from google.cloud import datastore
import google.cloud.exceptions
import sys

class GCStore:
    def __init__(self):
        self.client = datastore.Client()
        
    def get_npoem(self):
        key = self.client.key("counter",'npoem')
        counter = self.client.get(key)
        if counter == None:
            key = self.client.key("counter",'npoem')
            counter = datastore.Entity(key = key)
            counter['value'] = 0
            self.client.put(counter)
        return counter['value']

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

    def set_score(self,poem_id, score):
        with self.client.transaction():
            key = self.client.key("poem",poem_id)
            poem = self.client.get(key)
            poem['score'] = score
            self.client.put(poem)
        

    def log_poem(self, topic_str, date, poem_str, beam_size, time_dict, weights_dict = None):
        # return id
        npoem = self.increase_npoem()
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

        return poem.key.id, npoem
        
        
        

