import collections
import pandas as pd
import numpy as np
from MainApp import tools


def max_metric(logs: '[[{},{}...]...]', path):
    try:
        counts = collections.Counter()
        for label in tools.objs_labels():
            counts[label] = 0
        for log in logs:
            for arr in log:
                if arr['label'] in counts:
                    counts[arr['label']] += 1
        col = counts.most_common(len(counts.values()))
        gen_max_metric(col, path)
    except Exception():
        print('WRONG FORMAT')


def all_metric(logs: '[[{},{}...]...]', path, names):
    try:
        names_set = set(names)
        counts = {} # names
        for log in logs:
            for arr in log:
                if arr['label'] in names_set:
                    if arr['file_name'] not in counts:
                        counts[arr['file_name']] = {}
                    if arr['label'] not in counts[arr['file_name']]:
                        counts[arr['file_name']][arr['label']] = 0
                    counts[arr['file_name']][arr['label']] += 1
        df = pd.DataFrame(index=[x for x in counts], columns = names)
        for names in counts:
            for label in counts[names]:
                df.loc[names, label] = counts[names][label]
        df.index.name = 'file name'
        df.to_csv(path, encoding='utf-8', sep=';')
    except Exception():
        print('WRONG FORMAT')


# log = [[{'bottomright': {'x': 602, 'y': 585},
#   'confidence': 0.38619694,
#   'label': 'person',
#   'topleft': {'x': 455, 'y': 334},
#   'file_name': 'blabla'},
#  {'bottomright': {'x': 636, 'y': 776},
#   'confidence': 0.28718543,
#   'label': 'person',
#   'topleft': {'x': 563, 'y': 281},
#   'file_name': 'blabla'},
#  {'bottomright': {'x': 623, 'y': 959},
#   'confidence': 0.8782011,
#   'label': 'person',
#   'topleft': {'x': 0, 'y': 207},
#   'file_name': 'blabla'},
#  {'bottomright': {'x': 631, 'y': 959},
#   'confidence': 0.82520235,
#   'label': 'person',
#   'topleft': {'x': 476, 'y': 295},
#   'file_name': 'blabla'},
#  {'bottomright': {'x': 225, 'y': 881},
#   'confidence': 0.11298049,
#   'label': 'chair',
#   'topleft': {'x': 4, 'y': 387},
#   'file_name': 'blabla'}],
#   [{'bottomright': {'x': 602, 'y': 585},
#   'confidence': 0.38619694,
#   'label': 'person',
#   'topleft': {'x': 455, 'y': 334},
#   'file_name': 'blabla1'},
#  {'bottomright': {'x': 636, 'y': 776},
#   'confidence': 0.28718543,
#   'label': 'person',
#   'topleft': {'x': 563, 'y': 281},
#   'file_name': 'blabla1'},
#  {'bottomright': {'x': 623, 'y': 959},
#   'confidence': 0.8782011,
#   'label': 'person',
#   'topleft': {'x': 0, 'y': 207},
#   'file_name': 'blabla1'},
#  {'bottomright': {'x': 631, 'y': 959},
#   'confidence': 0.82520235,
#   'label': 'person',
#   'topleft': {'x': 476, 'y': 295},
#   'file_name': 'blabla1'},
#  {'bottomright': {'x': 225, 'y': 881},
#   'confidence': 0.11298049,
#   'label': 'chair',
#   'topleft': {'x': 4, 'y': 387},
#   'file_name': 'blabla1'}]]
#
# all_metric(log,'all.csv',['person', 'chair'])
# a = {'a':{'a':1, 'b':2}}
# print(a['a'])


def gen_max_metric(counts: '[(),()...]', path):
    arr = []
    for i, count in enumerate(counts):
        if count[1] != 0:
            arr.append(count[1])
        else:
            break
    arr = np.array(arr).reshape(-1, 1)
    count = list([x[0] for x in counts])
    df = pd.DataFrame(arr[: len(arr), 0], index=count[: len(arr)], columns=['count'])
    df.index.name = 'objects'
    df.to_csv(path, encoding='utf-8', sep=';')


def median_metric(logs: '[[{},{}...]...]', path):
    try:
        counts = {}
        for log in logs:
            for arr in log:
                if arr['label'] in counts:
                    counts[arr['label']][0] += 1
                    counts[arr['label']][1] += arr['confidence']
                else:
                    counts[arr['label']] = [1, arr['confidence']]
        gen_median_metric(counts, path)
    except Exception():
        print('WRONG FORMAT')


def gen_median_metric(counts: '[(),()...]', path):
    arr = []
    for ch in counts:
        counts[ch][1] = counts[ch][1] / counts[ch][0] # *counts[ch][0]
        arr.extend(counts[ch])
    arr = np.array(arr).reshape(-1, 2)
    df = pd.DataFrame(arr, index=counts.keys(), columns=['count', 'per'])
    df.sort_values(by=['count'])
    df['per'] = df['per'].map('{:.2f}'.format)
    df['count'] = df['count'].astype(int)
    df.index.name = 'objects'
    df.to_csv(path, encoding='utf-8', sep=';')