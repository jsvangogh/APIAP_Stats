# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 17:20:13 2015

@author: Jacob van Gogh

This script is used to download the JSON files for match IDs provided in the
Riot Api 2.0 Challenge zipfile. Only ranked matches from NA, EUW, EUNE, and KR
are downloaded. Files are sorted by region and then by patch. Also organizes
match IDs into a pandas DataFrame and saves this as a csv for future reference.
"""

import json
import pandas as pd
import rawpi
from time import sleep
import requests
import os

GOOD_RESPONSE = 200
RATE_LIMIT_RESPONSE = 429
KEY = '67097ca5-5400-4b53-86d1-fde4a4b4004a'

rawpi.set_api_key(KEY)


# Method Definitions: save_jsons()


def save_jsons(data_frame, region, patch):
    """
    Given a DataFrame with a column, 'match id', obtains the json for each
    match ID and saves it in the appropriate file.
    
    Keyword arguments:
    data_frame -- DataFrame containing match IDs in 'match id' column
    region -- region matches were played in
    patch -- patch matches were played on
    """
    # Figures out starting point (assumes data_frame
    # iterated through similarly each time)
    count = 0
    while (str(data_frame['match id'].iloc[count]) + '.json') in \
            os.listdir('JSONs/' + region + '/' + patch):
        count += 1
        if count % 100 == 0:
            print('finding start point: {0}'.format(count))
        if count >= len(data_frame.index):
            break

    print('starting at: {0}'.format(count))

    # save each json
    for match_id in data_frame['match id'][count:]:
        # attempt request until a successful response is received
        code = 0
        while code != GOOD_RESPONSE:
            # ignore connection errors and try again in 5 minutes
            match = None
            while match is None:
                try:
                    match = rawpi.get_match(region, match_id, True)
                except requests.ConnectionError as e:
                    print(e)
                    sleep(300)

            code = match.status_code
            # if rate limit response received, wait retry time
            if code == RATE_LIMIT_RESPONSE:
                if 'retry-after' in match.headers.keys():
                    wait_time = int(match.headers['retry-after']) + 0.1
                    print('waiting {0} seconds'.format(wait_time))
                    sleep(wait_time)
                else:
                    sleep(1.2)
            # if other bad response received, wait 5 minutes and try again
            elif code != GOOD_RESPONSE:
                print('error: {0}'.format(code))
                sleep(300)

        # update the count, save the json file, and wait 1.2 seconds to avoid
        # making too many requests
        count += 1
        filename = 'JSONs/{0}/{1}/{2}.json'.format(region, patch, str(match_id))
        with open(filename, 'w') as outfile:
            json.dump(match.json(), outfile)
        if count % 100 == 0:
            print('{0}: working...'.format(count))
        sleep(1.2)


#Save JSONs for Matches of Big 4 Regions' Ranked Matches


REGION_DICT = {'NA': 1, 'EUW': 2, 'EUNE': 3, 'KR': 4}
REVERSE_DICT = {1: 'NA', 2: 'EUW', 3: 'EUNE', 4: 'KR'}
REGIONS = ['KR']
PATCHES = [5.11, 5.14]

region_ranked_matches = pd.read_csv('filtered_matches.csv')

for region in REGIONS:
    for patch in PATCHES:
        working_frame = \
            region_ranked_matches[(
                region_ranked_matches['region'] == REGION_DICT[region]) &
                (region_ranked_matches['patch'] == patch)]
        print('Now on {0} {1}'.format(region, str(patch)))
        save_jsons(working_frame, region.lower())
