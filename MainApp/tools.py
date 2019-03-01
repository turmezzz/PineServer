import re
import time
import smtplib
import os
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML
from email.mime.base import MIMEBase
from email.encoders import encode_base64

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
