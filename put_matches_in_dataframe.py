# -*- coding: utf-8 -*-
'''
Created on Wed Aug 19 12:51:57 2015

@author: Innerfunk
'''

#%% Initialize

import json
import pandas as pd
import rawpi
import util

TOP_FOLDER = 'AP_ITEM_DATASET'
PATCHES = [str(p) for p in util.PATCHES]
QUEUE_DICT = util.QUEUE_DICT

REGIONS = util.REGIONS
REGION_DICT = util.REGION_DICT
REVERSE_DICT = util.REVERSE_REGION_DICT

ALL_SAVE_FILENAME = 'all_matches.csv'
FILTERED_SAVE_FILENAME = 'filtered_matches.csv'

GOOD_RESPONSE = 200
RATE_LIMIT_RESPONSE = 429

COLUMNS = ['match id', 'patch', 'queue', 'region']

KEY = 'PUT RIOT API KEY HERE'
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