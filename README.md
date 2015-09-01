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

1. put\_matches\_in\_dataframe reads in the match IDs given and stores this in a Pandas DataFrame along with info such as region
2. get\_json\_files stores match json objects for match IDs provided in the regions we selected
3. put\_stats\_in\_dataframe reads in each match json and stores stats such as item build and kills in a CSV
4. make_figures takes the stats we stored in the CSV and makes interactive figures that can be accessed via browser

(Note: we make use of the non-standard/public libraries; Pandas, Plotly, and rawpi)

##Main Observations:
###Effect On First and Second Buys

![alt tag](http://i.imgur.com/DT3K8j6.png)
Interactive Figure: https://plot.ly/~jsvangogh/157/ap-item-1-purchased-by-patch/

The three most popular first buys in 5.11, though still dominant, are less popular in 5.14. Zhonya's, Haunting Guise, Lich Bane, and Nashor's Tooth have all risen to take their place.
![alt tag](http://i.imgur.com/OIZmy8T.png)
Interactive Figure: https://plot.ly/~jsvangogh/160/ap-item-2-purchased-by-patch/

The reduction of AP on Luden's Echo decreased its popularity as a second item buy as well. The other Needlessly Large Rod items have risen in its place. In particular, the Rylai's changes have nearly doubled its popularity in both the first and second buy spots.

###Effect on Late Game Builds
![alt tag](http://i.imgur.com/W4bfSPe.png)
Interactive Figure: https://plot.ly/~jsvangogh/228/ap-item-4-purchased-by-patch/

The way players choose 4 completed AP items has changed as well. Specifically, Luden's Echo and Void Staff see large drops in purchases, while Rylai's Crystal Scepter continues to show increased popularity thanks to its remake. Core items, however, have remained fairly constant. Rabadon's Deathcap and Zhonya's Hourglass continue to be staples.

###Which Items do Each Lane Buy?
![alt tag](http://i.imgur.com/5dTTUjv.png)
Interactive Figure: https://plot.ly/~jsvangogh/223/first-ap-item-purchased-by-lane-patch-511/

![alt tag](http://i.imgur.com/8x4FJOj.png)
Interactive Figure: https://plot.ly/~jsvangogh/225/first-ap-item-purchased-by-lane-patch-514/

Rod of Ages is the most popular first AP item buy, but if you look only at midlane mages there's not contest: Morellonomicon is the most common rush item. Additionally, the rise in popularity of Nashor's Tooth seems to be due to junglers (Jungle Kayle hype? Jungle AP Xin hype?).

###Effect of Rank on Build Adaptations
![alt tag](http://i.imgur.com/7Sk2PtH.png)
Interactive Figure: https://plot.ly/~jsvangogh/534/percentage-of-4-ap-item-builds-each-item-present-in-by-rank-patch-511/

![alt tag](http://i.imgur.com/bKiSK5u.png)
Interactive Figure: https://plot.ly/~jsvangogh/536/percentage-of-4-ap-item-builds-each-item-present-in-by-rank-patch-514/

(Interactive figures highly recommended for these plots. Also note, the number of late-game challenger and master games was very small, so their statistics should not be analyzed too heavily. We recommend comparing diamond to bronze and silver.)

Void staff saw less presence in builds for all ranks, but the decrease was sharpest in higher ranks (12% decrease in diamond. 4% decrease in bronze). This, however, is due mainly to the low percentage of builds that made use of it in lower ranks even before the item changes. The opposite effect is seen in Rylai's Crystal Scepter. Lower ranked players purchased it more often in 5.11, but higher ranked players favor it more in 5.14. These discrepancies seem to highlight a higher-ranked player's ability to identify the strongest items and willingness to alter their builds.
