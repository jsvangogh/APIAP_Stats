# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 13:18:45 2015

@author: Jacob van Gogh
"""

import plotly.plotly as py
import pandas as pd
from plotly import tools
from plotly.graph_objs import *
import util


# Define Methods for Easy Figure-Creating
# Using Both Column Value Counts and Item Column Sums


def make_data_tuple_value_counts(frame, value_col, normalize=False,
                                 by_group=True, total=1):
    """
    Given a frame, makes a tuple of labels to values for a column's value
    counts. Can group small representations into an 'other' group and normalize
    values on a total argument.

    Keyword arguments:
    frame -- the DataFrame containing values
    value_col -- column name for values to plot
    normalize -- whether to normalize values to sum to 100, Default - True
    by_group -- when normalizing, should each group sum to 100, Default - True
    total -- total size of data set, used for normalizing
    """
    val_counts = frame[value_col].value_counts().to_dict()
    keys = val_counts.keys()

    label = [a for a in keys]
    if normalize:
        if by_group:
            total = len(frame)
        value = [val_counts[a]/total*100 for a in keys]
    else:
        value = [val_counts[x] for x in keys]

    return (label, value)


def make_bar_value_counts(frame, value_col, split_col, normalize=False,
                          by_group=True, filename='bar graph',
                          layout=Layout(barmode='stack')):
    """
    Makes a bar graph with grouped data from a DataFrame using a column's
    value counts

    Keyword arguments:
    frame -- the DataFrame containing values
    value_col -- column name for values to plot
    split_col -- column name that groups are split on
    normalize -- whether to normalize values to sum to 1, Default - True
    by_group -- when normalizing, should each group sum to 100, Default - True
    filename -- name of plotly file
    layout -- layout of figure, Default - stacked bar graph
    """

    groups = list(pd.Series(frame[split_col].ravel()).unique())
    total = len(frame)

    traces = []
    for group in sorted(groups):
        split_frame = frame[frame[split_col] == group]

        (x, y) = make_data_tuple_value_counts(frame=split_frame,
                                              value_col=value_col,
                                              normalize=normalize,
                                              by_group=by_group, total=total)

        name = str(group)

        traces.append(Bar(x=x, y=y, name=name))
    figure = Figure(data=traces, layout=layout)

    return py.plot(figure, filename=(filename))


def make_data_tuple_sums(frame, col_list, normalize=False,
                         by_group=True, total=1):
    """
    Given a frame, makes a tuple of labels to values a list of columns' sums.
    Can group small representations into an 'other' group and normalize
    values on a total argument.

    Keyword arguments:
    frame -- the DataFrame containing values
    col_list -- list of columns to sum to get data
    normalize -- whether to normalize values to sum to 100, Default - True
    by_group -- when normalizing, should each group sum to 100, Default - True
    total -- total size of data set, used for normalizing
    """
    x = col_list
    if normalize:
        if by_group:
            total = len(frame)
        y = [frame[l].sum()/total*100 for l in col_list]
    else:
        y = [frame[l].sum() for l in col_list]

    return (x, y)


def make_bar_sums(frame, col_list, split_col, normalize=False, by_group=True,
                  filename='bar graph', layout=Layout(barmode='stack')):
    """
    Makes a bar graph with grouped data from a DataFrame using column sums

    Keyword arguments:
    frame -- the DataFrame containing values
    col_list -- list of columns to sum to get data
    split_col -- column name that groups are split on
    normalize -- whether to normalize values to sum to 1, Default - True
    by_group -- when normalizing, should each group sum to 100, Default - True
    filename -- name of plotly file
    layout -- layout of figure, Default - stacked bar graph
    """
    groups = list(pd.Series(frame[split_col].ravel()).unique())
    total = len(frame)

    traces = []
    for group in sorted(groups):
        split_frame = frame[frame[split_col] == group]

        (x, y) = make_data_tuple_sums(frame=split_frame, col_list=col_list,
                                      normalize=normalize,
                                      by_group=by_group, total=total)
        traces.append(Bar(x=x, y=y, name=str(group)))

    figure = Figure(data=traces, layout=layout)
    return py.plot(figure, filename=filename)

# make figures

# Graphs for AP Items Purchased by Lane
stats = pd.read_csv('stats.csv')
for patch in [5.11, 5.14]:
    f = stats[stats['patch'] == patch]
    plot_title = 'First AP Item Purchased by Lane, Patch {0}'.format(patch)
    make_bar_value_counts(
        frame=f[f['num AP items'] >= 1], filename=plot_title,
        value_col='item 1', split_col='lane', normalize=True, by_group=False,
        layout=Layout(barmode='stack',
                      yaxis=YAxis(range=[0, 18], title='Buy Percentage'),
                      title=plot_title))

# Graphs for Item Purchases for First, Second, etc Purchases
for num in range(1, 6):
    f = stats
    plot_title = 'AP Item #{0} Purchased by Patch'.format(num)
    value_col = 'item {0}'.format(num)
    make_bar_value_counts(
        frame=f[f[value_col] != '0'],
        filename=plot_title,
        value_col=value_col, split_col='patch', normalize=True,
        layout=Layout(barmode='group',
                      yaxis=YAxis(title='Buy Percentage'),
                      title=plot_title))

# Graphs Showing the Percentage of #-item Builds That Contain Each Item
FULL_AP_ITEMS = util.FULL_AP_ITEMS

PATCHES = util.PATCHES


for i in range(2, 6):
    i_frame = stats[stats['num AP items'] == i]

    # Grouped Bar Graphs to Easily Compare Patches
    plot_title = 'Percentage of {0}-AP-Item Builds Each Item Present In'.format(i)
    layout = Layout(barmode='group',
                    yaxis=YAxis(title='Percentage of Builds Item is Present In'),
                    title=plot_title)
    make_bar_sums(frame=i_frame, col_list=FULL_AP_ITEMS, split_col='patch',
                  normalize=True, filename=plot_title, layout=layout)

    for patch in PATCHES:
        p_frame = i_frame[i_frame['patch'] == patch]

        # Stacked Bar Graphs Showing Lane Distribution
        lane_plot_title = 'Percentage of {0}-AP-Item Builds Each Item Present In By Lane, Patch {1}'.format(i, patch)
        lane_layout = Layout(barmode='stack',
                             yaxis=YAxis(title='Percentage of Builds Item is Present In'),
                             title=lane_plot_title)
        make_bar_sums(frame=p_frame, col_list=FULL_AP_ITEMS, split_col='lane',
                      normalize=True, by_group=False, filename=lane_plot_title,
                      layout=lane_layout)

        # Grouped Bar Graphs to Compare by Rank
        rank_plot_title = 'Percentage of {0}-AP-Item Builds Each Item Present In By Rank, Patch {1}'.format(i, patch)
        rank_layout = Layout(barmode='group',
                             yaxis=YAxis(title='Percentage of Builds Item is Present In'),
                             title=rank_plot_title)
        make_bar_sums(frame=p_frame, col_list=FULL_AP_ITEMS, split_col='rank',
                      normalize=True, by_group=True, filename=rank_plot_title,
                      layout=rank_layout)
