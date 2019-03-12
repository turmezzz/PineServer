import re
import time
import smtplib
import os
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import collections
import pandas as pd
import numpy as np


def max_metric(logs:'[[{},{}...]...]', path):
    try:
        counts = collections.Counter()
        with open('labels.txt', 'r') as f:
            for line in f:
                counts[line.split('\n')[0]] = 0
        for log in logs:
            for arr in log:
                if arr['label'] in counts:
                    counts[arr['label']] += 1
        col = counts.most_common(len(counts.values()))
        gen_maxMetric(col, path)
    except Exception():
        print('WRONG FORMAT')



def gen_maxMetric(counts:'[(),()...]', path):
    arr = []
    for i,count in enumerate(counts):
        if count[1] != 0:
            arr.append(count[1])
    arr = np.array(arr).reshape(-1,1)
    count = list(set([x[0] for x in counts]))
    df = pd.DataFrame(arr[:len(arr),0], index=count[:len(arr)], columns=['count'])
    df.index.name = 'objects'
    df.to_csv(path,encoding='utf-8')


def median_metric(logs:'[[{},{}...]...]', path):
    try:
        counts = {}
        for log in logs:
            for arr in log:
                if arr['label'] in counts:
                    counts[arr['label']][0] += 1
                    counts[arr['label']][1] += arr['confidence']
                else:
                    counts[arr['label']] = [1, arr['confidence']]
        gen_medianMetric(counts, path)
    except Exception():
        print('WRONG FORMAT')

def gen_medianMetric(counts:'[(),()...]', path):
    arr = []
    for ch in counts:
        counts[ch][1] = counts[ch][1]/counts[ch][0] # *counts[ch][0]
        arr.extend(counts[ch])
    arr = np.array(arr).reshape(-1,2)
    df = pd.DataFrame(arr, index=counts.keys(), columns=['count', 'per'])
    df.sort_values(by=['count'])
    df['per'] = df['per'].map('{:.2f}'.format)
    df['count'] = df['count'].astype(int)
    df.index.name = 'objects'
    df.to_csv(path, encoding='utf-8')


log = [[{'bottomright': {'x': 602, 'y': 585},
  'confidence': 0.38619694,
  'label': 'person',
  'topleft': {'x': 455, 'y': 334}},
 {'bottomright': {'x': 636, 'y': 776},
  'confidence': 0.28718543,
  'label': 'person',
  'topleft': {'x': 563, 'y': 281}},
 {'bottomright': {'x': 623, 'y': 959},
  'confidence': 0.8782011,
  'label': 'person',
  'topleft': {'x': 0, 'y': 207}},
 {'bottomright': {'x': 631, 'y': 959},
  'confidence': 0.82520235,
  'label': 'person',
  'topleft': {'x': 476, 'y': 295}},
 {'bottomright': {'x': 225, 'y': 881},
  'confidence': 0.11298049,
  'label': 'chair',
  'topleft': {'x': 4, 'y': 387}}], [{'bottomright': {'x': 602, 'y': 585},
  'confidence': 0.38619694,
  'label': 'person',
  'topleft': {'x': 455, 'y': 334}},
 {'bottomright': {'x': 636, 'y': 776},
  'confidence': 0.28718543,
  'label': 'person',
  'topleft': {'x': 563, 'y': 281}},
 {'bottomright': {'x': 623, 'y': 959},
  'confidence': 0.8782011,
  'label': 'person',
  'topleft': {'x': 0, 'y': 207}},
 {'bottomright': {'x': 631, 'y': 959},
  'confidence': 0.82520235,
  'label': 'person',
  'topleft': {'x': 476, 'y': 295}},
 {'bottomright': {'x': 225, 'y': 881},
  'confidence': 0.11298049,
  'label': 'chair',
  'topleft': {'x': 4, 'y': 387}}]]

max_metric(log, path='./MaxMetric.csv')

def send_mail(mail, name):
    addr_from = "messageFromPine@gmail.com"  # Адресат
    addr_to = mail                           # Получатель
    password = "DanilaGay6969"               # Пароль

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = 'Look at this dude'  # Тема сообщения

    zip_data = open(name, 'rb').read()
    if not os.path.isfile(name):
        raise Exception('File do not exist!')
    body = '''
    A-a-у(тип звук из аськи) пришла статистика!
    Олды тут !?!?!
    '''
    body_part = MIMEText(body, 'plain')
    msg.attach(body_part)
    with open(name, "rb") as attachment:
        part = MIMEBase("application", "rar")
        # part.set_payload(attachment.read()
        part.set_payload(zip_data)
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(name))
        msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Создаем объект SMTP
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим
    return True


def is_zip(file_name):
    pattern = r'.+\.zip'
    match = re.fullmatch(pattern, file_name)
    return True if match else False


def get_unique_title():
    box = int(time.time() * 1000)
    return str(box)
