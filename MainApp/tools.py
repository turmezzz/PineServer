import sys
import re
import time
import os
import zipfile
import shutil
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from MainApp import detection
from MainApp import statistics
import smtplib
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import collections
import pandas as pd


def send_mail(mail, name):
    addr_from = "messageFromPine@gmail.com"  # Адресат
    addr_to = mail                           # Получатель
    password = ""               # Пароль
    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = 'Look at this dude'  # Тема сообщения

    zip_data = open(name, 'rb').read()
    if not os.path.isfile(name):
        raise Exception('File do not exist!')
    body = '''
    Вам пришла статистика!
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


def is_zip(file):
    pattern = r'.+\.zip'
    match = re.fullmatch(pattern, file)
    return True if match else False


def is_image(file):
    patterns = [r'.+\.jpg', r'.+\.JPG', r'.+\.jpeg', r'.+\.JPEG', r'.+\.png', r'.+\.PNG']
    for pattern in patterns:
        match = re.fullmatch(pattern, file)
        if match:
            return True
    else:
        return False


def get_unique_title():
    box = int(time.time() * 1000)
    return str(box)


def objs_labels():
    path = 'MainApp/static/data/'
    labels_file = 'coco_labels.txt'
    fin = open(path + labels_file, 'r')
    labels = fin.read().split('\n')
    fin.close()
    return labels


def all_threads_done(futures):
    for f in futures:
        if not f.done():
            return False
    else:
        return True


def processing(zip_file, objects_to_detect):
    output_path = 'files/output/'
    zips_path = 'files/zips/'
    pwd = os.path.abspath('.')

    # zip file name without .zip
    # pwd - manage.py

    # making folders
    os.chdir(output_path)
    os.mkdir(zip_file)
    os.chdir(zip_file + '/')
    os.mkdir('in')
    os.mkdir('out')
    os.chdir(pwd)

    # unziping
    zip_ref = zipfile.ZipFile(zips_path + zip_file + '.zip', 'r')
    extract_folder = output_path + zip_file + '/box/'
    zip_ref.extractall(extract_folder)
    zip_ref.close()

    # moving files from extract folder to in folder
    i = 0
    for path, dirs, files in os.walk(extract_folder):
        path += '/'
        if '__MACOSX' in path:
            continue
        for file in files:
            if is_image(file):
                from_dir = path + file
                to_dir = output_path + zip_file + '/in/img_{}.jpg'.format(str(i))
                os.rename(from_dir, to_dir)
                i += 1
    shutil.rmtree(extract_folder)

    # for i, file in enumerate(os.listdir(extract_folder)):
    #     if is_image(file):
    #         from_dir = extract_folder + file
    #         to_dir = output_path + zip_file + '/in/img_{}.jpg'.format(str(i))
    #         os.rename(from_dir, to_dir)
    # shutil.rmtree(extract_folder)

    # detecting object on imgs from in folder
    in_imgs_path = output_path + zip_file + '/in/'
    out_imgs_path = output_path + zip_file + '/out/'
    futures = []
    ex = ThreadPoolExecutor(max_workers=10)
    for file in os.listdir(in_imgs_path):
        img = cv2.cvtColor(np.asarray(cv2.imread(in_imgs_path + file), dtype='uint8'), cv2.COLOR_BGR2RGB)
        futures.append(ex.submit(detection.detection, img, out_imgs_path + file, objects_to_detect))

    while not all_threads_done(futures):
        pass

    detection_results = []
    for f in futures:
        detection_results.append(f.result())
    statistics.max_metric(detection_results, out_imgs_path + 'max_metric.csv')















