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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(mail, subject, text, link=''):
    addr_from = "messageFromPine@gmail.com"  # Адресат
    addr_to = mail                           # Получатель
    password = "Russia_pobeda"               # Пароль
    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = subject  # Тема сообщения

    body = text.format(link)
    body_part = MIMEText(body, 'plain')
    msg.attach(body_part)

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Создаем объект SMTP
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим


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


def processing(zip_file, objects_to_detect, email):
    send_mail(email,
              'Pine received images.',
              'We have received your images. They are processing right now!')

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

    # detecting object on imgs from in folder
    in_user_path = output_path + zip_file + '/in/'
    out_user_path = output_path + zip_file + '/out/'
    futures = []
    ex = ThreadPoolExecutor(max_workers=10)
    for file in os.listdir(in_user_path):
        img = cv2.cvtColor(np.asarray(cv2.imread(in_user_path + file), dtype='uint8'), cv2.COLOR_BGR2RGB)
        futures.append(ex.submit(detection.detection, img, out_user_path + file, objects_to_detect))

    while not all_threads_done(futures):
        pass

    detection_results = []
    for f in futures:
        detection_results.append(f.result())

    statistics.max_metric(detection_results, out_user_path + 'max_metric.csv')
    statistics.all_metric(detection_results, out_user_path + 'all_metrics.csv', objects_to_detect)
    statistics.median_metric(detection_results, out_user_path + 'median_metrics.csv')

    files_to_zip = os.listdir('{}/{}/out/'.format(output_path, zip_file))
    out_zip_file = '{}/{}/out/out.zip'.format(output_path, zip_file)
    zip_ref = zipfile.ZipFile(out_zip_file, 'w')
    for file in files_to_zip:
        zip_ref.write(out_user_path + file, file)
    zip_ref.close()
    domain = '127.0.0.1:8000/'
    link = 'http://{}download_{}'.format(domain, zip_file)
    send_mail(email,
              'Pine detected your images.',
              '''We have processed your pics.
              You can download images and metrics at {}''',
              link)



















