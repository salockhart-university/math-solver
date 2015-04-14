import pandas as pd
import csv
import json
from glob import glob

# Goal is to convert the JSON files into CSV files so that they can be
# easily loaded into the python Pandas data-frame

def convert(x):
    ''' Convert a json string to a flat python dictionary
    which can be passed into Pandas. '''
    ob = json.loads(x)
    for k, v in ob.items():
        if isinstance(v, list):
            ob[k] = ','.join(v)
        elif isinstance(v, dict):
            for kk, vv in v.items():
                ob['%s_%s' % (k, kk)] = vv
            del ob[k]
    return ob

#In the line below, change the path where your .json file is created.
for json_filename in glob('C:\Chahna\Studies\MCS\Natural Language Processing\Project\Amazon Cell Phones\*.json'):

    csv_filename = '%s.csv' % json_filename[:-5]
    print 'Converting %s to %s' % (json_filename, csv_filename)
    df = pd.DataFrame([convert(line) for line in file(json_filename)])
    df.to_csv(csv_filename, encoding='utf-8', index=False)
