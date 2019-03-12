import collections
import pandas as pd
import numpy as np


# def popularity(detection_results, csv_file):
#     cnt = {}


def max_metric(logs: '[[{},{}...]...]', top=3):
    counts = collections.Counter()
    with open('labels.txt', 'r') as f:
        for line in f:
            counts[line.split('\n')[0]] = 0
    for log in logs:
        for arr in log:
            if arr['label'] in counts:
                counts[arr['label']] += 1
    col = counts.most_common(top)
    __gen_maxMetric(col, top)


def __gen_maxMetric(counts: '[(),()...]', top):
    arr = []
    for i, count in enumerate(counts):
        if i >= top:
            break
        arr.append(count[1])
    arr = np.array(arr).reshape(-1, 1)
    count = list(set([x[0] for x in counts]))
    df = pd.DataFrame(arr[:top, 0], index=count[:top], columns=['count'])
    df.index.name = 'objects'
    df.to_csv('MaxMetric.csv', encoding='utf-8')


def median_metric(logs: '[[{},{}...]...]'):
    counts = {}
    for log in logs:
        for arr in log:
            if arr['label'] in counts:
                counts[arr['label']][0] += 1
                counts[arr['label']][1] += arr['confidence']
            else:
                counts[arr['label']] = [1, arr['confidence']]
    __gen_medianMetric(counts)


def __gen_medianMetric(counts: '[(),()...]'):
    arr = []
    for ch in counts:
        counts[ch][1] = counts[ch][1] / counts[ch][0] * counts[ch][0]
        arr.extend(counts[ch])
    arr = np.array(arr).reshape(-1, 2)
    count = list(set([x[0] for x in counts]))
    # print(counts.keys())
    df = pd.DataFrame(arr, index=counts.keys(), columns=['count', 'per'])
    df.index.name = 'objects'
    df.to_csv('MedianMetric.csv', encoding='utf-8')


data = [[
    {
        'bottomright': {'x': 602, 'y': 585},
        'confidence': 0.38619694,
        'label': 'person',
        'topleft': {'x': 455, 'y': 334}
    },
    {
        'bottomright': {'x': 636, 'y': 776},
        'confidence': 0.28718543,
        'label': 'person',
        'topleft': {'x': 563, 'y': 281}
    },
    {
        'bottomright': {'x': 623, 'y': 959},
        'confidence': 0.8782011,
        'label': 'person',
        'topleft': {'x': 0, 'y': 207}
    },
    {
        'bottomright': {'x': 631, 'y': 959},
        'confidence': 0.82520235,
        'label': 'person',
        'topleft': {'x': 476, 'y': 295}
    },
    {
        'bottomright': {'x': 225, 'y': 881},
        'confidence': 0.11298049,
        'label': 'chair',
        'topleft': {'x': 4, 'y': 387}
    }
]]

# max_metric(data, 5)









