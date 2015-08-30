# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 21:17:25 2015

@author: Innerfunk
"""

import json
import pandas as pd
import rawpi
from pprint import pprint
from time import sleep
import pickle
import shutil

"""
KEY = "67097ca5-5400-4b53-86d1-fde4a4b4004a"

test_id = 1179606416
test_region = 'eune'

rawpi.set_api_key(KEY)

match = rawpi.get_match(test_region, test_id, includeTimeline=True)
if (match.status_code == 200):
    match_json = match.json()
    with open('json_size_test.txt', 'w') as outfile:
        json.dump(match_json, outfile)

match2 = rawpi.get_match(test_region, test_id, includeTimeline=False)
if (match2.status_code == 200):
    match_json2 = match2.json()
    with open('json_size_test2.txt', 'w') as outfile:
        json.dump(match_json2, outfile)



#%%
filename = 'JSONs/NA/1852538938.json'
with open(filename) as data_file:
        test = json.loads(data_file.read())

        
#%%
item_data = rawpi.get_item_list('na').json()['data']
item_dict = {i: item_data[i]['name'] for i in item_data.keys()}
reverse_item_dict = {item_dict[i]: i for i in item_dict}

champ_data = rawpi.get_champion_list('na').json()['data']
reverse_champ_dict = {i: champ_data[i]['id'] for i in champ_data.keys()}
champ_dict = {reverse_champ_dict[i]: i for i in reverse_champ_dict}


#%% Move Files
REVERSE_DICT = {1:'NA', 2:'EUW', 3:'EUNE', 4:'KR'}

matches_df = pd.read_csv('filtered_matches.csv')
for i in matches_df.index:
    region = REVERSE_DICT[matches_df.loc[i, 'region']]
    patch = matches_df.loc[i, 'patch']
    match_id = matches_df.loc[i, 'match id']
    
    old_path = 'JSONs/{0}/{1}.json'.format(region, match_id)
    new_path = 'JSONs/{0}/{1}/{2}.json'.format(region, patch, match_id)
    
    shutil.move(old_path, new_path)

"""
#%%
filename = 'JSONs/NA/5.14/1900736616.json'

with open(filename) as file:
    j = json.load(file)
    j_p = j['participants'][0]
    j_t = j['timeline']
    
    #events = [f['events'] for f in j_t_f]
    
item_data = rawpi.get_item_list('na').json()['data']
ITEM_DICT = {i: item_data[i]['name'] for i in item_data.keys()}
REVERSE_ITEM_DICT = {ITEM_DICT[i]: i for i in ITEM_DICT}
        
def get_item_purchases(timeline):
    """
    Given a timeline json object, returns a dictionary of
    participant ID: [list of item purchases] pairs.
    List will be sorted in chronological order.
    
    Keyword argument:
    timeline -- match's timeline json object
    """
    item_purchases = {i: [] for i in range(1, 11)}
    frames_list = timeline['frames']
    
    for frame in frames_list:
        if 'events' in frame:
            events = frame['events']
            item_events = [e for e in events \
                if e['eventType'] == 'ITEM_PURCHASED']
            for ie in item_events:
                item = str(ie['itemId'])
                if item in ITEM_DICT:
                    item_purchases[ie['participantId']].append(ITEM_DICT[item])
    
    return item_purchases
    
ip = get_item_purchases(j_t)    
    
    
    
    
    
    
    