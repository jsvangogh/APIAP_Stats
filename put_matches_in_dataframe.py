# -*- coding: utf-8 -*-
'''
Created on Wed Aug 19 12:51:57 2015

@author: Innerfunk
'''

#%% Initialize

import json
import pandas as pd
import rawpi

TOP_FOLDER = 'AP_ITEM_DATASET'
PATCHES = ['5.11', '5.14']
QUEUE_DICT = {'NORMAL_5X5': 'normal', 'RANKED_SOLO': 'ranked'}

REGIONS = ['NA', 'EUW', 'EUNE', 'KR', 'BR', 'LAN', 'LAS', 'OCE', 'RU', 'TR']
REGION_DICT = {'NA':1, 'EUW':2, 'EUNE':3, 'KR':4, 'BR':5, 'LAN':6, 'LAS':7, 'OCE':8, 'RU':9, 'TR':10}
REVERSE_DICT = {1:'NA', 2:'EUW', 3:'EUNE', 4:'KR', 5:'BR', 6:'LAN', 7:'LAS', 8:'OCE', 9:'RU', 10:'TR'}

ALL_SAVE_FILENAME = 'all_matches.csv'
FILTERED_SAVE_FILENAME = 'filtered_matches.csv'

GOOD_RESPONSE = 200
RATE_LIMIT_RESPONSE = 429

COLUMNS = ['match id', 'patch', 'queue', 'region']

KEY = '67097ca5-5400-4b53-86d1-fde4a4b4004a'
rawpi.set_api_key(KEY)

#%% Define DataFrame Creation Method
def put_matches_in_dataframe(patch, queue_type, region):
    filename = TOP_FOLDER + '/' + patch + '/' + queue_type + '/' + region + '.json'
    print(filename)
    
    with open(filename) as data_file:
        data = json.loads(data_file.read())
        
    matches_frame = pd.DataFrame(index=range(len(data)), columns=COLUMNS)
    queue = QUEUE_DICT[queue_type]
    matches_frame['match id'] = data
    matches_frame['patch'] = patch
    matches_frame['queue'] = queue
    matches_frame['region'] = REGION_DICT[region]
    
    return matches_frame
    
#%% Get All File into One Frame and Save
frame_list = []
for match_properties in [(patch, queue_type, region) for patch in PATCHES \
for queue_type in QUEUE_DICT.keys() for region in REGIONS]:
    frame_list.append(put_matches_in_dataframe(*match_properties))

all_frames = pd.concat(frame_list, ignore_index=True)

#%% Filter Matches
region_frames = all_frames[all_frames['region'].isin([1, 2, 3, 4])]
region_ranked_frames = region_frames[region_frames['queue'] == 'ranked']

all_frames.to_csv(ALL_SAVE_FILENAME, index=False)
region_ranked_frames.to_csv(FILTERED_SAVE_FILENAME, index=False)