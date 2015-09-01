# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 22:46:27 2015

@author: Jacob van Gogh
This utility sript stores constants for the items, regions, and patches tracked
in this project. It also provides functions for getting item and champ data.
"""

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

REGIONS_SHORT = ['NA', 'EUW', 'EUNE', 'KR']
REGIONS = ['NA', 'EUW', 'EUNE', 'KR', 'BR', 'LAN', 'LAS', 'OCE', 'RU', 'TR']
REGION_DICT = {'NA': 1, 'EUW': 2, 'EUNE': 3, 'KR': 4, 'BR': 5,
               'LAN': 6, 'LAS': 7, 'OCE': 8, 'RU': 9, 'TR': 10}
REVERSE_REGION_DICT = {1: 'NA', 2: 'EUW', 3: 'EUNE', 4: 'KR', 5: 'BR',
                       6: 'LAN', 7: 'LAS', 8: 'OCE', 9: 'RU', 10: 'TR'}

PATCHES = [5.11, 5.14]

QUEUE_DICT = {'NORMAL_5X5': 'normal', 'RANKED_SOLO': 'ranked'}
