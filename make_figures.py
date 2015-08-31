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


def make_bar(
        frame, value_col, stack_col,
        other=True, other_threshold=.02, normalize=True,
        filename='bar graph',
        layout=Layout(barmode='stack')):
    """
    Makes a bar graph from a DataFrame
    
    Keyword arguments:
    frame -- the DataFrame containing values
    value_col -- column name for values to plot
    stack_col -- column name that stacked bars are split on
    other -- whether to group small representations into 'other' group
             Default - True
    other_threshold -- threshold for which smaller values will be grouped into
                       'other' group. Default - 0.02
    normalize -- whether to normalize values to sum to 1, Default - True
    filename -- name of plotly file
    layout -- layout of figure, Default - stacked bar graph
    """
            
    stacks = list(pd.Series(frame[stack_col].ravel()).unique())
    
    traces = []
    for stack in sorted(stacks):
        stack_frame = frame[frame[stack_col] == stack]
        x_y_dict = stack_frame[value_col].value_counts().to_dict()
        
        if other:
            stack_entries = len(stack_frame)
            keys = [k for k in x_y_dict.keys() 
                    if x_y_dict[k]/stack_entries >= other_threshold]
            other_sum = stack_entries - sum([x_y_dict[k] for k in keys])
            x_y_dict['other'] = other_sum
            keys.append('other')
        else:
            keys = x_y_dict.keys()
        
        x = [a for a in keys]
        if normalize:
            total_entries = len(frame)
            y = [x_y_dict[a]/total_entries for a in keys]
        else:
            y = [x_y_dict[x] for x in keys]
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
        value_col='item 1', stack_col='lane',
        layout=Layout(barmode='stack', 
                      yaxis=YAxis(range=[0, 0.18], title='Buy Percentage'),
                      title='First Item Purchased {0}'.format(patch)
               )
                     )