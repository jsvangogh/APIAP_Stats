# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 13:18:45 2015

@author: Jacob van Gogh
"""

import plotly.plotly as py
import pandas as pd
from plotly import tools
from plotly.graph_objs import *

# Define Methods for Easy Figure-Creating


def make_label_value_tuple(frame, value_col, other=True, 
                           other_threshold=.02, normalize=False, total=1):
    """
    Given a frame, makes a tuple of labels to values.
    Can group small representations into an 'other' group and normalize values
    on a total argument.
    
    Keyword arguments:
    frame -- the DataFrame containing values
    value_col -- column name for values to plot
    other -- whether to group small representations into 'other' group
             Default - True
    other_threshold -- threshold for which smaller values will be grouped into
                       'other' group. Default - 0.02
    normalize -- whether to normalize values to sum to 1, Default - True
    total -- total size of data set, used for normalizing
    """
    val_counts = frame[value_col].value_counts().to_dict()
    if other:
        val_entries = len(frame)
        keys = [k for k in val_counts.keys() 
                if val_counts[k]/val_entries >= other_threshold]
        other_sum = val_entries - sum([val_counts[k] for k in keys])
        val_counts['other'] = other_sum
        keys.append('other')
    else:
        keys = val_counts.keys()
    
    label = [a for a in keys]
    if normalize:
        value = [val_counts[a]/total for a in keys]
    else:
        value = [val_counts[x] for x in keys]
    
    return (label, value)
    

def make_bar(
        frame, value_col, stack_col,
        other=True, other_threshold=.02, normalize=False,
        filename='bar graph',
        layout=Layout(barmode='stack')):
    """
    Makes a bar graph with grouped data from a DataFrame
    
    Keyword arguments:
    frame -- the DataFrame containing values
    value_col -- column name for values to plot
    stack_col -- column name that groups are split on
    other -- whether to group small representations into 'other' group
             Default - True
    other_threshold -- threshold for which smaller values will be grouped into
                       'other' group. Default - 0.02
    normalize -- whether to normalize values to sum to 1, Default - True
    filename -- name of plotly file
    layout -- layout of figure, Default - stacked bar graph
    """
            
    stacks = list(pd.Series(frame[stack_col].ravel()).unique())
    total=len(frame)
    
    traces = []
    for stack in sorted(stacks):
        stack_frame = frame[frame[stack_col] == stack]
        
        (x, y) = make_label_value_tuple(frame=stack_frame,
                                        value_col=value_col, 
                                        normalize=normalize, total=total)        
        
        name = str(stack)
            
        traces.append(Bar(x=x, y=y, name=name))
    figure = Figure(data=traces, layout=layout)
    
    url = py.plot(figure, filename=(filename))
    

# stuff

stats = pd.read_csv('stats.csv')
for patch in [5.11, 5.14]:
    f = stats[stats['patch'] == patch]
    make_bar(
        frame=f[f['num AP items'] >= 1], filename=str(patch),
        value_col='item 1', stack_col='lane', normalize=True,
        layout=Layout(barmode='stack', 
                      yaxis=YAxis(range=[0, 0.18], title='Buy Percentage'),
                      title='First Item Purchased {0}'.format(patch)
               )
                     )