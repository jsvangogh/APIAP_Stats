# APIAP_Stats

##Our Objective:
We analyzed the effects of the AP item changes on players builds. These graphs vizualize the different build paths used between patch 5.11 and 5.14. We looked to find out whether the item changes achieved the goal of increased build diversity.


##Our Analysis:
We analyzed item builds in two ways:

1. We looked at the distribution of first, second, etc item buys
2. We looked at the percentage of builds (of a certain number of items) that contained each item
3. 
These two analyses were then compared by patch, lane, and rank to get an understanding of how the patch affected each group of players. Interactive graphs were then made using Plotly.

We looked only at completed AP items (with the exception of Haunting Guise, which we felt some players stopped at without building Liandry's Torment). We also only looked at ranked games from NA, EUW, EUNE, and KR.


##Our Code and Methods:
We performed this analysis in Python by using a sequence of scripts. Our results can be replicated by executing the scripts as follows:

1. put_matches_in_dataframe reads in the match IDs given and stores this in a Pandas DataFrame along with info such as region
2. get_json_files stores match json objects for match IDs provided in the regions we selected
3. put_stats_in_dataframe reads in each match json and stores stats such as item build and kills in a CSV
4. make_figures takes the stats we stored in the CSV and makes interactive figures that can be accessed via browser

(Note: we make use of the non-standard/public libraries; Pandas, Plotly, and rawpi)

##Main Observations:
###Affect On First and Second Buys

![alt tag](http://i.imgur.com/DT3K8j6.png)
![alt tag](http://i.imgur.com/OIZmy8T.png)
