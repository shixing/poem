# python read.py datastore_backup_datastore_backup_2017_01_31_poem

import os
import sys,datetime
sys.path.append('/usr/local/google_appengine/')
sys.path.append('/usr/local/google_appengine/lib/yaml/lib/')
if 'google' in sys.modules:
    del sys.modules['google']
from google.appengine.api.files import records
from google.appengine.datastore import entity_pb
from google.appengine.api import datastore
import json

def str_to_entity(s,ep = None):
    entity_proto = entity_pb.EntityProto(contents=s)
    if ep:
        entity_proto.key_.app_ = ep.key_.app_
        entity_proto.key_.path_ = ep.key_.path_
    entity = datastore.Entity.FromPb(entity_proto)
    return entity_proto, entity
    

def record_to_dict(record, embed_name = ['style','time']):
    entity_proto, entity = str_to_entity(record)

    d = {}
    # add id
    d['poem_id'] =  entity_proto.key_.path_.element_[0].id_
    
    #
    for key in entity: 
        if key in embed_name:
            s = entity[key]
            _, e = str_to_entity(s,entity_proto)
            temp_d = {}
            for temp_key in e:
                temp_d[temp_key] = e[temp_key]
            d[key] = temp_d
        else:
            if key == 'created_at':
                d[key] = str(entity[key])
            else:
                d[key] = entity[key]

        
    return d
    

def iter_entity(folder):
    for d, _, files in os.walk(folder):
        for fn in files:
            path = os.path.join(d, fn)
	    raw = open(path,'r')
	    reader = records.RecordsReader(raw)
	    for record in reader:
                entity = record_to_dict(record)
		yield entity
	    raw.close()


def main():
    folder = sys.argv[1]
    i = 0 
    if folder.endswith('/'):
        folder = folder[:-1]
    dump_json_path = folder + ".json"
    f = open(dump_json_path,'w')
    for poem in iter_entity(folder):
        i += 1
        #print poem
        f.write(json.dumps(poem)+"\n")
    f.close()
    print i 
if __name__ == "__main__":
    main()
