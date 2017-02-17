# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 11:24:51 2017

Extracts key data from Pixhawk flight logs
Works with .log files exports from APM Planner

CURR, 11297961, 0, 2471, 55, 5135, 0, 0
label, time, -, voltage, current, current total, -,-

@author: Silas
"""
import matplotlib.pyplot as plt
import numpy as np
from pandas import read_csv
#import json
import os
import time
#from collections import OrderedDict
import sys



## Take input as log file
if __name__ == '__main__':
    args = sys.argv
    """
    print '\n'
    print 'sys.argv:'
    print args
    """

if len(args)>1:
    logs = args[1:len(args)]
    print 'Parsing '
    print logs

else:
    print 'Error: give me .log file(s) to parse'
    sys.exit()

dfs=[] #list of dataframes of log data
for i in range(len(logs)):
    dfs.append(read_csv(logs[i]))

"""
## Open log_notes.json into dictionary
with open("log_notes.json", "r") as f:
  log_notes = json.loads(f.read())

## Do stuff with data

graph_title = ''
graph_filename = ''
longest_seconds = 0
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
shapes = ['-','--',':','_']

for i in range(len(dfs)):
    ## Make Title
    if i == 0 and len(logs) == 1:
        graph_filename += logs[i]
        graph_title += log_notes[logs[i]]['description']
    elif i != len(logs)-1 and len(logs) >1:
        graph_filename += logs[i]+"_"
        graph_title += log_notes[logs[i]]['description'] +'\n'
    else:
        graph_filename += logs[i]
        graph_title += log_notes[logs[i]]['description']
    ## Analysis
    df = dfs[i]
    total_seconds = len(df.index)
    total_time = time.strftime('%H:%M:%S', time.gmtime(total_seconds))
    if total_seconds > longest_seconds:
        longest_seconds = total_seconds



    ## Add data to log_notes.json
    log_notes[logs[i]]['total_seconds'] = total_seconds
    log_notes[logs[i]]['total_time'] = total_time


    ## Plot Single graph of logs
    styles = [j+shapes[i] for j in colors]
    if i == 0:
        ax = df.plot(figsize=(8,6), style = styles)

    else:
        df.plot(ax=ax, style = styles)

if longest_seconds <=60:
    tick_spacing = 2 #2 seconds
elif longest_seconds <= 1800:
    tick_spacing = 60 #1 minute
elif longest_seconds <= 3600:
    tick_spacing = 300 #5 minutes
elif longest_seconds <= 7200:
    tick_spacing = 900 #15 minutes
else:
    tick_spacing = 3600 #1 hour

graph_title = graph_filename+'\n'+graph_title
plt.title(graph_title)
plt.xlabel('Time (s): '+ time.strftime('%H:%M:%S', time.gmtime(longest_seconds)))
plt.ylabel('Temperature (C)')
plt.xticks(np.arange(tick_spacing,longest_seconds,tick_spacing) )
lgd = plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.savefig(graph_filename+'.png', bbox_extra_artists=(lgd,), bbox_inches='tight')



#Sort dictionary
log_notes=OrderedDict(sorted(log_notes.items(), key=lambda t: t[0]))
#print log_notes

# Save to log_notes.json
with open("log_notes_TEMP.json","w") as f:
    json.dump(log_notes, f, indent = 4)
os.remove("log_notes.json")
os.rename("log_notes_TEMP.json", "log_notes.json")
"""
