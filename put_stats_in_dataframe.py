# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 20:11:37 2015

@author: Jacob van Gogh

This script is used to gather end-of-game stats for matches and place them in
a DataFrame, which is saved as a csv. It gathers the number of FULL_AP_ITEMS
(see util) each champ has purchased as well as:
kills, deaths, assists, lane, role, winner, match duration, region, and patch.
"""

import json
import pandas as pd
import rawpi
import os

KEY = "67097ca5-5400-4b53-86d1-fde4a4b4004a"
rawpi.set_api_key(KEY)

SAVE_FILENAME = 'stats.csv'

FULL_AP_ITEMS = ['Abyssal Scepter',
                 'Archangel\'s Staff',
                 'Athene\'s Unholy Grail',
                 'Haunting Guise',
                 'Liandry\'s Torment',
                 'Lich Bane',
                 'Luden\'s Echo',
                 'Mejai\'s Soulstealer',
                 'Morellonomicon',
                 'Nashor\'s Tooth',
                 'Rabadon\'s Deathcap',
                 'Rod of Ages',
                 'Rylai\'s Crystal Scepter',
                 'Seraph\'s Embrace',
                 'Void Staff',
                 'Will of the Ancients',
                 'Zhonya\'s Hourglass']
                 
REGIONS = ['NA', 'EUW', 'EUNE', 'KR']
REGION_DICT = {'NA': 1, 'EUW': 2, 'EUNE': 3, 'KR': 4}
REVERSE_REGION_DICT = {1: 'NA', 2: 'EUW', 3: 'EUNE', 4: 'KR'}
PATCHES = [5.11, 5.14]


# Create dictionaries from codes to names and vice-versa for items and champs.


item_data = rawpi.get_item_list('na').json()['data']
ITEM_DICT = {i: item_data[i]['name'] for i in item_data.keys()}
REVERSE_ITEM_DICT = {ITEM_DICT[i]: i for i in ITEM_DICT}

champ_data = rawpi.get_champion_list('na').json()['data']
CHAMP_DICT = {champ_data[name]['id']: name for name in champ_data}


# Define methods for creating DataFrame rows. These are structured as dicts
# with keys being column names and values being DataFrame values. These methods
# function by passing a dictionary and adding to them. This dictionary can then
# be added to a list that a DataFrame can be created from.


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


def add_ordered_items(item_purchases, col_dict):
    """
    Adds stats for completed AP item purchase order
    
    Keyword arguments:
    item_purchases -- list of items purchased in chronological order
    col_dict -- column dictionary
    """
    num = 1
    for item in item_purchases:
        if item in FULL_AP_ITEMS:
            col_dict['item {0}'.format(num)] = item
            num += 1
            if num >= 6:
                break


def add_end_game_items(stats_json, col_dict):
    """
    Adds stats for items at the end of the game to the column dictionary
    
    Keyword arguments:
    stats_json -- participant's ['stats'] object
    col_dict -- dictionary for column: value pairs
    """
    participant_item_codes = [stats_json['item' + str(i)] for i in range(6)]
    items = [ITEM_DICT[str(i)] for i in participant_item_codes if str(i) in ITEM_DICT]
    AP_item_count = 0
    for i in items:
        if i in FULL_AP_ITEMS:
            AP_item_count += 1
            if i in col_dict:
                col_dict[i] = col_dict[i] + 1
            else:
                col_dict[i] = 1
    col_dict['num AP items'] = AP_item_count
    

def add_stats(stats_json, col_dict):
    """
    Adds basic stats to the column dictionary
    
    Keyword arguments:
    stats_json -- participant's ['stats'] object
    col_dict -- dictionary for column: value pairs
    """
    col_dict['winner'] = stats_json['winner']
    col_dict['kills'] = stats_json['kills']
    col_dict['deaths'] = stats_json['deaths']
    col_dict['assists'] = stats_json['assists']

           
def add_participant_row(
    participant_json, patch, region, duration, item_purchases_dict, row_list):
    """
    Adds a row dictionary to the given list
    
    Keyword arguments:
    participant_json -- participant object
    patch -- patch the match was played on
    region -- region the match was played in
    duration -- duration of the match
    item_purchases_dict -- dictionary of participant id: [item purchases list]
    row_list -- list of columnd dictionaries
    """
    col_dict = {}
    col_dict['patch'] = patch
    col_dict['region'] = REGION_DICT[region]
    col_dict['champ'] = CHAMP_DICT[participant_json['championId']]
    col_dict['lane'] = participant_json['timeline']['lane'].lower()
    col_dict['role'] = participant_json['timeline']['role'].lower()
    col_dict['rank'] = participant_json['highestAchievedSeasonTier'].lower()
    col_dict['duration'] = duration
    
    add_end_game_items(participant_json['stats'], col_dict)
    add_ordered_items(
        item_purchases_dict[participant_json['participantId']], col_dict)
    add_stats(participant_json['stats'], col_dict)
    
    row_list.append(col_dict)
    
           
def add_match_rows(match_json, patch, region, row_list):
    """
    Given a json for a match, creates column dictionaries for all participants
    that went MIDDLE and adds these dictionaries to the given list
    
    Keyword arguments:
    match_json -- match object
    patch -- patch the match was played on
    region -- region the match was played in
    row_list -- list of column dictionaries
    """
    duration = match_json['matchDuration']
    item_purchases_dict = get_item_purchases(match_json['timeline'])
    
    for p_json in match_json['participants']:
        add_participant_row(
            p_json, patch, region, duration, item_purchases_dict, row_list)


#%% Put Stats for Each Match in DataFrame
stats_rows_list = []

for r in REGIONS:
    for p in PATCHES:
        path_front = 'JSONs/{0}/{1}'.format(r, p)
        
        count = 0
        for j in os.listdir(path_front):
            if count % 1000 == 0: print('Currently On:{0}'.format(count + 1))
            count += 1
            
            with open(path_front + '/' + j) as file:
                match_json = json.load(file)
                
            add_match_rows(match_json, p, r, stats_rows_list)

stats_frame = pd.DataFrame(stats_rows_list)
stats_frame = stats_frame.fillna(0)
stats_frame.to_csv(SAVE_FILENAME, index=False)