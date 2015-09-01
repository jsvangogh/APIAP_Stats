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
                 
REGIONS = ['NA', 'EUW', 'EUNE', 'KR']
REGION_DICT = {'NA': 1, 'EUW': 2, 'EUNE': 3, 'KR': 4}
REVERSE_REGION_DICT = {1: 'NA', 2: 'EUW', 3: 'EUNE', 4: 'KR'}
PATCHES = [5.11, 5.14]