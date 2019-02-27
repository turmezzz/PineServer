import re
import time


def is_zip(file_name):
    pattern = r'.+\.zip'
    match = re.fullmatch(pattern, file_name)
    return True if match else False


def get_unique_title():
    box = int(time.time() * 1000)
    return str(box)
