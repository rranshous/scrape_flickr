#!/usr/bin/python
import json
from urllib2 import urlopen
import os
import time
import glob


SAVE_DIR = './collection/'
URL = 'http://api.flickr.com/services/feeds/photos_public.gne?format=json'
HERE = os.path.abspath(os.path.dirname(__file__))
SAVE_TO = os.path.abspath(os.path.join(HERE,SAVE_DIR))

def get_json_string():
    json_string = urlopen(URL).read().strip()
    # cut out the callback wrap
    json_string = json_string[json_string.find('(')+1:-1]
    return json_string

def get_json_data():
    try:
        return json.loads(get_json_string())
    except ValueError:
        time.sleep(1)
        return json.loads(get_json_string())

def create_index():
    # we want to create a list w/ the names of all the images in the dir
    with file(os.path.join(SAVE_TO,'inventory.txt'),'w') as fh:
        for name in glob.glob('%s/*'%SAVE_TO):
            if name.endswith('.txt'): continue
            fh.write('%s\n' % os.path.basename(name))

def scrape():
    data = get_json_data()
    # download / save our images
    for item_data in data.get('items'):
        media = item_data.get('media').get('m')
        name = media.rsplit('/',1)[-1]
        out_path = os.path.join(SAVE_TO,name)
        if os.path.exists(out_path):
            continue
        with file(out_path,'wb') as fh:
            print 'downloading: %s' % name
            fh.write(urlopen(media).read())

    create_index()

if __name__ == '__main__':
    scrape()
